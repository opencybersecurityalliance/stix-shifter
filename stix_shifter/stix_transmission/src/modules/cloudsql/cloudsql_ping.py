from ..base.base_ping import BasePing


class CloudSQLPing(BasePing):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        jobs_df = self.api_client.get_jobs()

        return_obj = dict()

        if jobs_df is not None:
            return_obj['success'] = True
        else:
            return_obj['success'] = False
            return_obj['error'] = "Ping failed"
        return return_obj
