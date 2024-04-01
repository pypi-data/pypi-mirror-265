import re
import os
import sys
import numpy
import jieba
import string
import langid
import textstat
import unicodedata
import zhon.hanzi
from collections import Counter
from hanziconv import HanziConv

sys.path.append(os.path.dirname(__file__))

from const import *

TRANSLATION_TABLE_PUNCTUATION_EN = str.maketrans('', '', string.punctuation)
TRANSLATION_TABLE_PUNCTUATION_ZH = str.maketrans('', '', zhon.hanzi.punctuation)

def form_ngrams(sequence, n):
    history = []
    # build the first ngram, yielding only when we have a full ngram
    while n > 1:
        try:
            next_item = next(sequence)
        except StopIteration:
            # no more data, terminate the generator
            return
        history.append(next_item)
        n -= 1

    # yield each ngram we have, then add the next item and repeat
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]

def normalize(
        text: str,
        remove_punct: bool = True,
        lowercase: bool = True,
        nfd_unicode: bool = True,
        white_space: bool = True
) -> str:
    """Normalize the text by lowercasing and removing punctuation."""
    # remove punctuation
    if remove_punct:
        text = text.translate(TRANSLATION_TABLE_PUNCTUATION_EN)
        text = text.translate(TRANSLATION_TABLE_PUNCTUATION_ZH)

    # lowercase
    if lowercase:
        text = text.lower()

    if white_space:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)

    # NFD unicode normalization
    if nfd_unicode:
        text = unicodedata.normalize('NFD', text)

    return text

def split_words(content: str):
    res = []
    for i in content.split():
        en_word = ''
        for j in i:
            if re.match(r'[\u4e00-\u9fff]', j):
                if en_word != '':
                    res.append(en_word)
                    en_word = ''
                res.append(j)
            else:
                en_word = en_word + j
        if en_word == i:
            res.append(i)
    return tuple(res)

def base_rps_frac_chars_in_dupe_ngrams(NGRAM_SIZE, content):
    """Base class for calculating the fraction of characters in duplicate word
    N-grams.

    This operates on the lower-cased, punctuation removed content. The function
    also ensures that characters in overlapping ngrams are only counted once.
    """
    normalized_content = normalize(content)
    normalized_words = split_words(normalized_content)

    if len(normalized_words) < NGRAM_SIZE:
        return 0

    # fetch the ngrams from the document if they exist, otherwise
    # compute them
    doc_n_grams = tuple(form_ngrams(iter(normalized_words), NGRAM_SIZE))

    # keep only ngrams which occur at least twice
    ngram_dupes = {
        ngram for ngram, count in Counter(doc_n_grams).items() if count > 1
    }

    duplicated_grams = numpy.zeros(len(normalized_words), dtype=int)
    i = 0
    for ngram in doc_n_grams:
        if ngram in ngram_dupes:
            duplicated_grams[i: i + NGRAM_SIZE] = 1

        i += 1

    word_lengths = numpy.array(list(map(len, normalized_words)))
    chars_duped = numpy.sum(word_lengths * duplicated_grams)
    total_chars = numpy.sum(word_lengths)

    if total_chars == 0:
        return 0

    score = float(chars_duped / total_chars) * 100
    return score

def common_colon_end(content: str) -> dict:
    """content最后一个字符是冒号."""
    res = {'error_status': False}
    if len(content) <= 0:
        return res
    if content[-1] == ':':
        res['error_status'] = True
        res['error_type'] = ERROR_RULE_COLON_END
        res['error_reason'] = '冒号结尾'
    return res

def common_special_character(content: str) -> dict:
    res = {'error_status': False}
    pattern = r'[�]'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_type"] = ERROR_SPECIAL_CHARACTER
        res['error_reason'] = '特殊符号�'
    return res

def common_bracket_unmatch(content: str) -> dict:
    """检查开闭括号数量是否一致."""
    res = {'error_status': False}
    flag = ''
    if content.count('[') != content.count(']'):
        flag = '[ 和 ]'
    if content.count('{') != content.count('}'):
        flag = '{ 和 }'
    if content.count('【') != content.count('】'):
        flag = '【 和 】'
    if content.count('《') != content.count('》'):
        flag = '《 和 》'
    if flag != '':
        res["error_status"] = True
        res["error_type"] = ERROR_BRACKET_UNMATCH
        res['error_reason'] = '括号数量不匹配： ' + flag
    return res

def common_doc_repeat(content: str) -> dict:
    """检查content内是否有连续重复."""
    res = {'error_status': False}
    repeat_score = base_rps_frac_chars_in_dupe_ngrams(6, content)
    if repeat_score >= 80:
        res["error_status"] = True
        res["error_type"] = ERROR_DOC_REPEAT
        res['error_reason'] = '文本重复度过高： ' + str(repeat_score)
    return res

def common_no_punc(content: str) -> dict:
    """检查content内是否有大段无标点."""
    res = {'error_status': False}
    paragraphs = content.split('\n')
    max_word_count = 0
    for paragraph in paragraphs:
        if len(paragraph) == 0:
            continue
        sentences = re.split(r'[-–.!?,;•、。！？，；·]', paragraph)
        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)
            if word_count > max_word_count:
                max_word_count = word_count
    text_stat_res = textstat.flesch_reading_ease(content)
    if int(max_word_count) > 56 and text_stat_res < 20:
        res["error_status"] = True
        res["error_type"] = ERROR_NO_PUNC
        res['error_reason'] = '段落无标点'
    return res

def common_chaos_zh(content: str) -> dict:
    """检查content内是否有中文乱码."""
    res = {'error_status': False}
    lan = langid.classify(content)[0]
    if lan != 'zh':
        return res
    s = normalize(content)
    pattern = r'[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\n\s]'
    s = re.sub(pattern, '', s)
    s_simplified = HanziConv.toSimplified(s)
    str_len = len(s)
    seg_len = len(list(jieba.cut(s_simplified)))
    num_bytes = len(content.encode('utf-8'))
    tokens_len = int(num_bytes * 0.248)
    if str_len == 0 or seg_len == 0 or tokens_len < 50:
        return res
    if str_len / seg_len <= 1.1:
        res["error_status"] = True
        res["error_type"] = ERROR_CHAOS_ZH
        res['error_reason'] = '中文乱码'
    return res

def common_chaos_en(content: str) -> dict:
    """检查content内是否有英文乱码."""
    res = {'error_status': False}
    lan = langid.classify(content)[0]
    if lan != 'en':
        return res
    s = normalize(content)
    str_len = len(s)
    seg_len = len(list(jieba.cut(s)))
    num_bytes = len(content.encode('utf-8'))
    tokens_len = int(num_bytes * 0.248)
    if str_len == 0 or seg_len == 0 or tokens_len < 50:
        return res
    if str_len / seg_len <= 1.2:
        res["error_status"] = True
        res["error_type"] = ERROR_CHAOS_EN
        res['error_reason'] = '英文乱码'
    return res

def common_chaos_symbol(content: str) -> dict:
    """检查content内是否有大量非正文内容."""
    res = {'error_status': False}
    pattern = r'[0-9a-zA-Z\u4e00-\u9fa5]'
    s = re.sub(pattern, '', content)
    str_len = len(content)
    symbol_len = len(s)
    if str_len == 0 or symbol_len == 0:
        return res
    if symbol_len / str_len > 0.5:
        res["error_status"] = True
        res["error_type"] = ERROR_CHAOS_SYMBOL
        res['error_reason'] = '大量非正文内容'
    return res

def common_language_mixed(content: str) -> dict:
    """检查content内是否有中英文混杂."""
    res = {'error_status': False}
    s = normalize(content)
    en_len = len(re.findall(r'[a-zA-Z]', s))
    zh_len = len(re.findall(r'[\u4e00-\u9fa5]', s))
    count_len = len(s)
    if count_len == 0:
        return res
    if en_len / count_len >= 0.5 and zh_len / count_len >= 0.1:
        res["error_status"] = True
        res["error_type"] = ERROR_LANGUAGE_MIXED
        res['error_reason'] = '中英文混杂'
    return res

def common_enter_continuous(content: str) -> dict:
    """检查content内是否有连续大于8个的回车."""
    res = {'error_status': False}
    pattern = r'\n{8,}|\r{8,}'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_type"] = ERROR_ENTER_CONTINUOUS
        res['error_reason'] = '存在连续8个回车'
    return res

def common_enter_more(content: str) -> dict:
    """检查content内是否有超过25%正文占比的回车."""
    res = {'error_status': False}
    enter_count = content.count('\n')
    count = len(content)
    if count == 0:
        return res
    ratio = enter_count / count * 100
    if ratio >= 25:
        res["error_status"] = True
        res["error_type"] = ERROR_ENTER_MORE
        res['error_reason'] = '回车超过正文25%'
    return res

def common_content_null(content: str) -> dict:
    """检查content内是否为空."""
    res = {'error_status': False}
    count = len(content.strip())
    if count == 0:
        res["error_status"] = True
        res["error_type"] = ERROR_CONTENT_NULL
        res['error_reason'] = '内容为空'
    return res

def common_space_more(content: str) -> dict:
    """检查content内是否有连续500个以上的空格."""
    res = {'error_status': False}
    pattern = r' {500,}'
    matches = re.findall(pattern, content)
    if matches:
        res["error_status"] = True
        res["error_type"] = ERROR_SPACE_MORE
        res['error_reason'] = '存在连续500个空格'
    return res

def common_url_only(content: str) -> dict:
    """检查content内是否只有url."""
    res = {'error_status': False}
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # noqa
    s = re.sub(pattern, '', content)
    count = len(s.strip())
    if count == 0:
        res["error_status"] = True
        res["error_type"] = ERROR_URL_ONLY
        res['error_reason'] = '内容只有url'
    return res

def common_word_stuck(content: str) -> dict:
    """检查content内是否有英文单词黏连."""
    res = {'error_status': False}
    words = re.findall(r'[a-zA-Z]+', content)
    max_word_len = 0
    for word in words:
        if len(word) > max_word_len:
            max_word_len = len(word)
    if max_word_len > 45:
        res["error_status"] = True
        res["error_type"] = ERROR_WORD_STUCK
        res['error_reason'] = '英文单词黏连'
    return res