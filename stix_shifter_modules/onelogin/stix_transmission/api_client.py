from onelogin.api.client import OneLoginClient


class APIClient():

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.client = OneLoginClient(auth.get('clientId'), auth.get('clientSecret'), connection['region'])

    def generate_token(self):
        """To generate the Token"""
        self.client.get_access_token()
        return self.response_handler()

    def run_search(self, quary_expr, range_end=None):
        """get the response from onelogin endpoints
        :param quary_expr: str, search_id
        :param range_end: int,length value
        :return: response, json object"""
        token = self.client.get_access_token()
        if token and self.client.error is None:
            events = self.client.get_events(quary_expr, max_results=range_end)
        return self.response_handler(events)

    def response_handler(self, data=None):
        if data is None:
            data = []
        response = dict()
        response["code"] = self.client.error
        if self.client.error is None:
            response.update({"code": 200, "data": data})
        elif self.client.error == 500 and "local variable 'data' referenced before assignment" in self.client.error_description:
            response.update({"code": 200, "data": []})
        else:
            response["message"] = self.client.error_description
        return response
