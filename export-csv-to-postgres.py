import json
import csv

import psycopg2

INSERT_STATEMENT = '''
INSERT INTO Readings (
    passage,
    time_min,
    week,
    original_row
) VALUES (
    %(passage)s,
    %(time_min)s,
    %(week)s,
    %(original_row)s
)'''


connection_parameters = None
with open('connection-parameters.secret.json') as auth_info_file:
    connection_parameters = json.load(auth_info_file)
db = psycopg2.connect(**connection_parameters)
cursor = db.cursor()
sql_statements = None
with open('postgres-schema.sql') as schema_file:
    sql_statements = schema_file.read().split(';')

for statement in [s.strip() for s in sql_statements if len(s) > 0]:
    cursor.execute(statement)

with open('reading-tracker.csv') as csv_file:
    csv_data = csv.DictReader(csv_file)
    current_week = None
    for row_number, data in enumerate(csv_data):
        # Spreadsheet uses merged cells in Dates column; account for that
        if data['Dates']:
            current_week = data['Dates']
        time_spent = data['Time spent (m)']
        if len(time_spent) == 0:
            time_spent = None
        insert_dict = {
            'passage': data['Passages'],
            'time_min': time_spent,
            'week': current_week,
            'original_row': row_number + 2
        }
        cursor.execute(INSERT_STATEMENT, insert_dict)
db.commit()
cursor.close()
db.close()
