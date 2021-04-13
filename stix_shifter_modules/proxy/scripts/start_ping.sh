cd "$(dirname "$0")"
cd ../../..
FILE_CERT='cert.pem'
export REQUESTS_CA_BUNDLE="`pwd`/$FILE_CERT"

python main.py transmit -d proxy '
{
    "type":"proxy",
    "options": {
        "proxy_host": "localhost",
        "proxy_port": 5000,
        "proxy_cert": true,
        "timeout":60,
        "destination": {
                "connection":{
                "options": {
                    "time_range":5,
                    "result_limit":10000,
                    "timeout":10,
                    "language":"stix"
                },
                "url":"https:\/\/raw.githubusercontent.com\/opencybersecurityalliance\/stix-shifter\/develop\/data\/cybox\/1.json",
                "type":"stix_bundle",
                "help":"https:\/\/www.ibm.com\/support\/knowledgecenter\/SSTDPP_1.1.0\/docs\/scp-core\/data-sources-stix.html"
            },
            "configuration": {
                "auth": {
                    "username":"",
                    "password":""
                }
            }
        }
    }
}' '{}' ping