import sqlite3

NEXT_READING_QUERY = """
SELECT *
FROM Readings
WHERE time_min == ""
ORDER BY original_row ASC
LIMIT 1
"""


def get_next_reading() -> str:
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