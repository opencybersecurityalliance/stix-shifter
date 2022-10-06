import mysql.connector
from mysql.connector import errorcode


class APIClient():

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.user = auth.get('username')
        self.password = auth.get('password')
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.host = connection.get("host")
        self.database = connection.get("database")
        self.table = connection['options'].get("table")
        self.port = connection.get("port")
        self.auth_plugin = 'mysql_native_password'

    def ping_data_source(self):
        # Pings the data source
        response = {"code": 200, "message": "All Good!"}
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, 
                                          host=self.host, database=self.database, 
                                          port=self.port, auth_plugin=self.auth_plugin)  

        except mysql.connector.Error as err:
            response["code"] = err.errno

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                response["message"] = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                response["message"] = "Database does not exist"
            else:
                response["message"] = err
        else:
            cnx.close()
        return response

    def run_search(self, query, start=0, rows=0):
        # Return the search results. Results must be in JSON format before translating into STIX 
        response = {"code": 200, "message": "All Good!", "result": []}

        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, 
                                          database=self.database, port=self.port, auth_plugin=self.auth_plugin)
            cursor = cnx.cursor()
            column_query = "SHOW COLUMNS FROM %s" % self.table 
            cursor.execute(column_query)
            column_collection = cursor.fetchall()
            column_list = []

            for tuple in column_collection:
                column_list.append(tuple[0])
            # Uncomment to see data on newly populated table
            # query = "select * from {} limit 1".format(self.table)

            cursor.execute(query)  
            result_collection = cursor.fetchall()
            results_list = []
            row_count = int(rows)

            # Put table data in JSON format
            for index, tuple in enumerate(result_collection):
                if index < int(start):
                    continue
                if row_count < 1:
                    break
                results_object = {}
                for index, datum in enumerate(tuple):
                    results_object[column_list[index]] = datum
                results_list.append(results_object)
                row_count -= 1

            response["result"] = results_list

        except mysql.connector.Error as err:
            response["code"] = err.errno
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                response["message"] = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                response["message"] = "Database does not exist"
            else:
                response["message"] = err
        else:
            cnx.close()
        return response
