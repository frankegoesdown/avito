# coding=utf-8
from collections import Counter
from decimal import Decimal
import itertools
import os
import re
import string

from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords

from config import CHEATS, COUNT_FREQUENT_WORDS


result_to_insert = []


def detect_cheat(word):
    """Detect latin symbols in cyrillic text"""
    cheats = list(itertools.chain.from_iterable([c.findall(word) for c in CHEATS]))
    if len(cheats):
        return True, improve_word(cheats, word)
    else:
        return False, word


def detect_cheat_in_text(text):
    """Detect cheats in text"""
    new_text = []
    is_cheat = False
    for word in text:
        is_cheated_word, recovery_token = detect_cheat(word)
        if is_cheated_word:
            is_cheat = True
            new_text.append(recovery_token)
    stop_words = set(stopwords.words('russian'))

    st = RussianStemmer()

    new_text = [word for word in new_text if (word not in stop_words)]
    return is_cheat, [st.stem(word) for word in new_text]


def improve_word(cheats, word):
    """Replace latin symbols to cyrillic in broken word"""
    for cheat in cheats:
        word = word.replace(cheat, cheat.translate(dict((ord(a), ord(b)) for a, b in zip('aeopyxc', u'аеорухс'))))
    return word


def parse_file(path):
    """Parse file for find cheating in text and calculate advego"""
    with open(path, 'r') as f:
        filename = os.path.basename(f.name)
        data = f.read().decode('utf-8')
        is_cheat, text = detect_cheat_in_text(split_file_data(re.compile(u'[^a-zA-Zа-яА-Я0-9-_]+').split(data)))
    advego = calculate_advego(data)
    result_to_insert.append((filename, str(advego), str(is_cheat)))


def split_file_data(data):
    """Split string into words and skip all non-leters words return list of lowercase words"""
    return [word.lower() for word in data if (word not in string.punctuation and len(word))]


def calculate_advego(text):
    """Calculate advego for text"""
    if not len(text):
        return 0
    else:
        count = Counter(text)
        common_count = 0
        for el in count.most_common(COUNT_FREQUENT_WORDS):
            common_count += el[1]
        return Decimal(common_count) / Decimal(len(text))
