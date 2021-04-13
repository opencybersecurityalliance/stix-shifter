cd "$(dirname "$0")"
cd ../../..
pwd
FILE_CERT='cert.pem'
FILE_KEY='key.pem'
# export REQUESTS_CA_BUNDLE="`pwd`/$FILE_CERT"

if [ ! \( -f $FILE_CERT -a -f $FILE_KEY \) ]; then
    echo "File not found!"
    openssl req -x509 -newkey rsa:4096 -nodes -out $FILE_CERT -keyout $FILE_KEY -days 365 -subj /CN=localhost
fi

python main.py host '' "127.0.0.1:5000" $FILE_CERT $FILE_KEY