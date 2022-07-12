import aiomysql
from pymysql.err import DatabaseError


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

    async def ping_data_source(self):
        # Pings the data source
        response = {"code": 200, "message": "All Good!"}
        try:
            pool = await aiomysql.create_pool(host=self.host, port=self.port,
                                            user=self.user, password=self.password,
                                            db=self.database)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 42;")
                    (r,) = await cur.fetchone()
                    assert r == 42

            pool.close()
            await pool.wait_closed()
        except DatabaseError as err:
            response["code"] = int(err.args[0])
            response["message"] = err
        except Exception as err:
            response["code"] = 'unknown'
            response["message"] = err

        return response

    async def run_search(self, query, start=0, rows=0):
        # Return the search results. Results must be in JSON format before translating into STIX 
        response = {"code": 200, "message": "All Good!", "result": []}

        try:
            pool = await aiomysql.create_pool(host=self.host, port=self.port,
                                            user=self.user, password=self.password,
                                            db=self.database)
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    column_query = "SHOW COLUMNS FROM %s" % self.table 
                    await cursor.execute(column_query)
                    column_collection = await cursor.fetchall()
                    column_list = []

                    for row in column_collection:
                        column_list.append(row[0])
                    # Uncomment to see data on newly populated table
                    # query = "select * from {} limit 1".format(self.table)

                    await cursor.execute(query)  
                    result_collection = await cursor.fetchall()
                    results_list = []

                    # Put table data in JSON format
                    for tuple in result_collection:
                        results_object = {}
                        for index, datum in enumerate(tuple):
                            results_object[column_list[index]] = datum
                        results_list.append(results_object)

                    response["result"] = results_list

            pool.close()
            await pool.wait_closed()
        except DatabaseError as err:
            response["code"] = int(err.args[0])
            response["message"] = err
        except Exception as err:
            response["code"] = 'unknown'
            response["message"] = err

        return response
