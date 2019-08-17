import os
import sqlite3
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

NEXT_READING_QUERY = """
SELECT *
FROM Readings
WHERE time_min=NULL
ORDER BY original_row ASC
LIMIT 1
"""


def get_next_reading() -> str:
    cursor = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
    cursor.execute(NEXT_READING_QUERY)
    result = cursor.fetchall()
    cursor.close()
    cursor.connection.close()
    if len(result) != 1:
        return "Reading plan complete!"
    return result[0][1]

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
