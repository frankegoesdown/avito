from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import os

from utils.config import TEXT_FILES_PATH, logger
from utils.db_helper import clear_db, create_db, insert_to_db
from utils.exception import TxtDirectoryException
from utils.service import parse_file, result_to_insert


def run():
    logger.info("Start")
    create_db()
    clear_db()
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        try:
            file_list = [os.path.join(TEXT_FILES_PATH, f) for f in os.listdir(TEXT_FILES_PATH) if f.endswith(".txt")]
        except OSError as err:
            logger.exception("Can't find txt files")
            raise TxtDirectoryException(str(err))
        for f in file_list:
            executor.submit(parse_file, f)

    insert_to_db(result_to_insert)
    logger.info("Finish")
