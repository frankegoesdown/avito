# coding=utf-8
import os
import logging
import re

# logger
logging.basicConfig(filename="log.txt", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# constants
ROOT_PATH = os.path.abspath(os.curdir)
DB_PATH = os.path.join(ROOT_PATH, 'advego.db')
TEXT_FILES_PATH = os.path.join(ROOT_PATH, 'text_files')
COUNT_FREQUENT_WORDS = 5

CHEATS = [
    re.compile(u'[а-я0-9-_]+([aeyopxc]+)'),
    re.compile(u'^([aeyopxc]+)[а-я0-9-_]+')
]
