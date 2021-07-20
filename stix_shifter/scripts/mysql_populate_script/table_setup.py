import mysql.connector
from mysql.connector import errorcode
import json
import csv


class TableSetup():

    def __init__(self, connection_params, table, data_file):
        self.connection_params = json.loads(connection_params)
        self.table = table
        self.csv_reader = csv.reader(data_file, delimiter=',')
        self.csv_rows = []
        self.fields_list = []
        self.data_types_list = []

    def __get_db_connection(self):
        return mysql.connector.connect(user=self.connection_params["user"], password=self.connection_params["password"], 
                                       host=self.connection_params["host"], database=self.connection_params["database"], 
                                       port=3306, auth_plugin='mysql_native_password')

    def __handle_error(self, err):
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    def drop_table(self):
        try:
            cnx = self.__get_db_connection()
            cursor = cnx.cursor()
            sql = "DROP TABLE IF EXISTS {}".format(self.table)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()

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
            print("Creating table with the following fields: {}".format(self.fields_list))
            sql = "CREATE TABLE {} {};".format(self.table, fields_and_type)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            self.__handle_error(err)
        else:
            cnx.close()

    def populate_table(self):
        try:
            cnx = self.__get_db_connection()
            cursor = cnx.cursor()
            print("Populating table with data")
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