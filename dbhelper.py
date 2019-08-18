import os
import sqlite3
import logging
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

NEXT_READING_QUERY = """
SELECT *
FROM Readings
WHERE time_min is null
ORDER BY original_row ASC
LIMIT 1
"""

UPDATE_READING_STATEMENT = """
UPDATE Readings
SET time_min=%(time_spent)s
WHERE id=%(id)s
"""

def complete_reading(time_spent: int):
    id, _, _ = get_next_reading()
    cursor = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
    success = False
    try:
        cursor.execute(UPDATE_READING_STATEMENT, {
            'id': id,
            'time_spent': time_spent
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
            str (week)
    """
    cursor = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
    cursor.execute(NEXT_READING_QUERY)
    result = cursor.fetchall()
    cursor.close()
    cursor.connection.close()
    if len(result) != 1:
        return "Reading plan complete!"
    return int(result[0][0]), result[0][1], result[0][3]

def get_next_reading_sqlite() -> str:
    """Fetch next unread passage from the database.

    Returns:
        str -- next unread passage on reading plan
    """
    cursor = sqlite3.connect('reading-tracker.db').cursor()
    result = cursor.execute(NEXT_READING_QUERY).fetchall()
    cursor.close()
    cursor.connection.close()
    if len(result) != 1:
        return "Reading plan complete!"
    return result[0][1]


if __name__ == '__main__':
    print(get_next_reading())
