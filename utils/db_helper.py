import sqlite3

from utils.config import logger, DB_PATH


def create_db():
    """Create db if it doesn't exists"""
    con = sqlite3.connect(DB_PATH)
    try:
        with con:
            cur = con.cursor()
            cur.executescript("""
                CREATE TABLE IF NOT EXISTS advego (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    "filename" TEXT NOT NULL,
                    "coef" REAL NOT NULL,
                    "is_cheat" BOOL NOT NULL
                );
            """)
        logger.info("DB was created successfully")
    except con.Error as err:
        logger.exception(err.message)


def insert_to_db(rows):
    """Write rows into db"""
    con = sqlite3.connect(DB_PATH)
    try:
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO advego ('filename', 'coef', 'is_cheat') VALUES (?, ?, ?)", (rows))
        logger.info("Data insert successfully")
    except con.Error as err:
        logger.exception(err.message)


def clear_db():
    """Clear all rows in db"""
    con = sqlite3.connect(DB_PATH)
    try:
        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM advego;')
        logger.info("All rows was successfully deleted")
    except con.Error as err:
        logger.exception(err.message)
