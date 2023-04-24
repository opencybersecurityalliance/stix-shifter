import sys
from table_setup import TableSetup


def main():
    # Connection to the database in the form of '{"host": "<host>", "database": "<database>", "user": "<user>", "password": "<password>"}'
    connection = sys.argv[1]
    # Name of the target database. If the databse already exists it will be dropped and recreated.
    database = sys.argv[2]
    # Name of table you wish to create and populate
    table = sys.argv[3]
    # CSV file containing field names in the first row, data types in the second row, and associated data in subsequent rows.
    data_file = open('data.csv')

    table_setup = TableSetup(connection, database, table, data_file)
    table_setup.create_database()
    table_setup.drop_table()
    table_setup.create_table()
    table_setup.populate_table()


if __name__ == "__main__":
    main()
