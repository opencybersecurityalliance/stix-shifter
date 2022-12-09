import mysql.connector
from mysql.connector import errorcode
import json
import csv

PORT = 3306

class TableSetup():

    def __init__(self, connection_params, database, table, data_file):
        connection_params = json.loads(connection_params)
        self.user = connection_params["user"]
        self.password = connection_params["password"]
        self.host = connection_params["host"]
        self.database = database
        self.table = table
        self.csv_reader = csv.reader(data_file, delimiter=',')
        self.csv_rows = []
        self.fields_list = []
        self.data_types_list = []

    def __get_sql_connection(self):
        return mysql.connector.connect(user=self.user, password=self.password, 
                                       host=self.host,  port=PORT, auth_plugin='mysql_native_password')

    def __get_db_connection(self):
        return mysql.connector.connect(user=self.user, password=self.password, 
                                       host=self.host, database=self.database, 
                                       port=PORT, auth_plugin='mysql_native_password')

    def __handle_error(self, err):
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    def create_database(self):
        print("Creating database: {}".format(self.database))
        try:
            cnx = self.__get_sql_connection()
            cursor = cnx.cursor()
            sql = "DROP DATABASE IF EXISTS {}".format(self.database)
            cursor.execute(sql)
            sql = "CREATE DATABASE {}".format(self.database)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()
            print("{} created".format(self.database))


    def drop_table(self):
        print("Dropping table: {}".format(self.table))
        try:
            cnx = self.__get_db_connection()
            cursor = cnx.cursor()
            sql = "DROP TABLE IF EXISTS {}".format(self.table)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()
            print("{} dropped".format(self.table))

    def create_table(self):
        try:
            for row in self.csv_reader:
                self.csv_rows.append(row)
            cnx = self.__get_db_connection()
            cursor = cnx.cursor()
            self.fields_list = self.csv_rows[0]
            self.data_types_list = self.csv_rows[1]

            fields_and_type = "("
            for index, field in enumerate(self.fields_list):
                fields_and_type += "{} {}, ".format(field, self.data_types_list[index])
            fields_and_type = fields_and_type[:-2]
            fields_and_type += ")"
            print("Creating {} with the following fields: {}".format(self.table, self.fields_list))
            sql = "CREATE TABLE {} {};".format(self.table, fields_and_type)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()

    def populate_table(self):
        print("Populating {} with data".format(self.table))
        try:
            cnx = self.__get_db_connection()
            cursor = cnx.cursor()
            sql_insert_parameters = ("%s," * len(self.fields_list))[:-1]
            for index, row in enumerate(self.csv_rows):
                if index < 2:
                    continue
                sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table, ", ".join(self.fields_list), sql_insert_parameters)
                value_tuple = tuple(row)
                cursor.execute(sql, value_tuple)
                cnx.commit()
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()