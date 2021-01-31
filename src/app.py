
import os
import time
import hmac
import hashlib
from flask_api import status
# from req import RequestPerformer
from sel import get_source
from flask import Flask, request, redirect, url_for

app = Flask("requestProxy")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# set timezone:
os.environ['TZ'] = 'Europe/Berlin'
time.tzset()

# reqp = RequestPerformer()

SIGN_KEY = "1coqC2xfB9vXRQSeSE0"
VALID_REQ_KEY = "SVptAacLFg"

@app.route("/")
def default():
    return "alive", status.HTTP_200_OK

def verify(sendReqKey, url, sendSignature):
    if sendReqKey == VALID_REQ_KEY:
        reqString = " ".join([url, sendReqKey])
        signature = hmac.new(bytes(SIGN_KEY , 'latin-1'), msg = bytes(reqString , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
        validString = " ".join([url, VALID_REQ_KEY])
        VALID_SIGNATURE = hmac.new(bytes(SIGN_KEY , 'latin-1'), msg = bytes(validString , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
        if signature == VALID_SIGNATURE:
            print("access granted")
            return True
    return False

@app.route("/proxy")
def proxy():
    url = request.args.get('url')
    key = request.args.get('reqKey')
    signature = request.args.get('signature')
    if verify(key, url, signature):
        # html, code = reqp.getHtml(url)
        # if code >= 400 and code < 500:
        #     html, code = reqp.getHtml(url)
        # print(code)
        html = get_source(url)
        print(html)
        return html, status.HTTP_200_OK
    return "your request does not seem to be signed correctly", status.HTTP_401_UNAUTHORIZED

if __name__ == '__main__':
	app.run()
