import os
import sqlite3
import logging
import psycopg2
import datetime

DATABASE_URL = os.environ['DATABASE_URL']

NEXT_READING_QUERY = """
SELECT *
FROM Readings2020
WHERE completed is null
ORDER BY reading_day ASC
LIMIT 1
"""

UPDATE_READING_STATEMENT = """
UPDATE Readings2020
SET completed=%(completed)s
WHERE id=%(id)s
"""

def complete_reading():
    id, _, _ = get_next_reading()
    cursor = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
    success = False
    try:
        cursor.execute(UPDATE_READING_STATEMENT, {
            'id': id,
            'completed': datetime.datetime.now()
        })
        success = True
    except Exception as ex:
        logging.error(ex)
    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()
    if not success:
        raise Exception('Error updating row in DB with completed reading')

def get_next_reading() -> tuple:
    """Return next unread passage from postgres
    
    Returns:
        tuple -- 3-tuple containing:
            int (id)
            str (passage)
            str (dates)
    """
    cursor = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
    cursor.execute(NEXT_READING_QUERY)
    result = cursor.fetchall()
    cursor.close()
    cursor.connection.close()
    if len(result) != 1:
        return None, "Reading plan complete!", ""
    dates = " to ".join([result[0][4], result[0][5]])
    return int(result[0][0]), result[0][1], dates
