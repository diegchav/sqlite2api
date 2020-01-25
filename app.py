import argparse
import json
import requests
import sqlite3
import sys

def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]

    return d

def connect_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        return conn
    except sqlite3.OperationalError as e:
        sys.exit(e) 

def get_records(conn, db_table):
    try:
        records = conn.execute('SELECT * FROM {}'.format(db_table)).fetchall()
        return records
    except sqlite3.OperationalError as e:
        sys.exit(e)

def insert_data(api_endpoint, records):
    total_records = 0  # Number of records inserted
    headers = { 'Content-type': 'application/json' }
    for record in records:
        record.pop('id')  # Ignore 'id' column from table records
        try:
            r = requests.post(url=api_endpoint, data=json.dumps(record), headers=headers)
            if r.status_code == 200:
                total_records += 1
            else:
                r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            break

    print('Inserted records: {}'.format(total_records))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert data from a sqlite db table into an API endpoint.')
    parser.add_argument('db_file_name', help='Name of the sqlite database file to connect to (must be in the same directory as this script)')
    parser.add_argument('db_table_name', help='Name of the sqlite table to read from')
    parser.add_argument('api_endpoint', help='API endpoint to insert into')
    args = parser.parse_args()

    conn = connect_db(args.db_file_name)
    records = get_records(conn, args.db_table_name)
    insert_data(args.api_endpoint, records)
