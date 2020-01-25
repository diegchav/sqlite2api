import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert data from a sqlite db table into an API endpoint.')
    parser.add_argument('db_file_name', help='Name of the sqlite database file to connect to (must be in the same directory as this script)')
    parser.add_argument('db_table_name', help='Name of the sqlite table to read from')
    parser.add_argument('api_endpoint', help='API endpoint to insert into')
    parser.parse_args()
