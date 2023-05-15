from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper

DATA = {
            "code": 200,
           "data": [
            {
                "report": {
                "success": True,
                "full": {
                    "ip": "203.190.254.239",
                    "count": 0,
                    "attacks": 0,
                    "lastseen": "None",
                    "firstseen": "None",
                    "updated": "None",
                    "comment": "None",
                    "threatfeedscount": 7
                }
            },
            }
           ]
    }

class http_struct:
    def __init__(self):
        self.content = ""
        self.headers = ""
        self.status_code = 0

HTTP_RESPONSE = http_struct()
HTTP_RESPONSE.content = bytearray(b'{"ip":{"number":"101.81.5.6","count":null,"attacks":null,"maxdate":null,"mindate":null,"updated":null,"comment":null,"maxrisk":null,"asabusecontact":"anti-spam@ns.chinanet.cn.net","as":4812,"asname":"CHINANET-SH-AP China Telecom Group","ascountry":"CN","assize":11671552,"network":"101.80.0.0\\/13"}}')
HTTP_RESPONSE.status_code = 200

DATA_TRANS = ResponseWrapper(HTTP_RESPONSE)