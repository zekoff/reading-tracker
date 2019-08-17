import sqlite3
import csv

INSERT_STATEMENT = '''
INSERT INTO Readings (
    passage,
    time_min,
    week,
    original_row
) VALUES (
    :passage,
    :time_min,
    :week,
    :original_row
)'''

# Set up SQLite database to receive data
db = sqlite3.connect('reading-tracker.db')
with open('schema.sql') as schema_file:
    db.executescript(schema_file.read())
    db.commit()

# Pull from spreadsheet into database
with open('reading-tracker.csv') as csv_file:
    csv_data = csv.DictReader(csv_file)
    cursor = db.cursor()
    current_week = None
    for row_number, data in enumerate(csv_data):
        # Spreadsheet uses merged cells in Dates column; account for that
        if data['Dates']:
            current_week = data['Dates']
        insert_dict = {
            'passage': data['Passages'],
            'time_min': data['Time spent (m)'],
            'week': current_week,
            'original_row': row_number + 2
        }
        cursor.execute(INSERT_STATEMENT, insert_dict)
    db.commit()

db.close()