import json
import csv

import psycopg2

INSERT_STATEMENT = '''
INSERT INTO Readings2020 (
    passage,
    reading_day,
    week,
    start_day,
    end_day
) VALUES (
    %(passage)s,
    %(reading_day)s,
    %(week)s,
    %(start_day)s,
    %(end_day)s
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

with open('2020-bible-reading-input-data.csv') as csv_file:
    csv_data = csv.DictReader(csv_file)
    for row_number, data in enumerate(csv_data):
        insert_dict = {
            'passage': data['Passages'],
            'reading_day': data['Reading Day'],
            'week': data['Week'],
            'start_day': data['Start Date'],
            'end_day': data['End Date']
        }
        cursor.execute(INSERT_STATEMENT, insert_dict)
db.commit()
cursor.close()
db.close()
