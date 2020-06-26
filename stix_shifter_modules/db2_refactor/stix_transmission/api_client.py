import ibm_db

class DB2Client():

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')

        try:
            self.client = ibm_db.pconnect(
                "DATABASE=" + "bigsql" +
                ";HOSTNAME=" + connection.get("host", "") +
                ";PORT=" + connection.get("port", "31490") +
                ";UID=" + self.auth.get("username") +
                ";PWD=" + self.auth.get("password"),
                "", "")

        except Exception as e:
            print("EXCEPTION in DB2Client", e)
            raise e

        self.state = ibm_db.active(self.client)

    def ping_data_source(self):
        # Pings the data source
        if self.state:
            return {"code": 200, "success": True}
        return {"code": 400, "success": False}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
