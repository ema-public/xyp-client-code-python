# -*- coding: utf-8 -*-
import websocket
import json
from requests import Session
from XypClient import Service
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from env import KEY_PATH
from env import REGNUM
from env import WEBSOCKETURL
try:
    import thread
except ImportError:
    import _thread as thread
import time


timestamp = ""

"""
string мэдээллийг X509Certificate болгож хөрвүүлэх
@param cert_base64 сертификатын мэдээлэл
@returns {module:crypto.X509Certificate}

@author unenbat
@since 2023-05-23
"""
def parse_certificate(cert_base64):
    cert_bytes = base64.b64decode(cert_base64)
    cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
    return cert

"""
сертификатын мэдээллээс сериал дугаарыг олж авах
@param cert_base64
@returns {string}

@author unenbat
@since 2023-05-23
"""
def get_serial_number(cert_base64):
    cert = parse_certificate(cert_base64)
    serial_number = cert.serial_number
    return serial_number.to_bytes((serial_number.bit_length() + 7) // 8, 'big').hex()

"""
esign client программаас мэдээлэл хүлээж авах, өгөгдсөн мэдээллээр ХУР-ын сервис дуудах
@param message esign client программаас ирж буй мэдээлэл

@author unenbat
@since 2023-05-23
"""
def on_message(ws, message):
    sign = json.loads(message)
    params = {  
        'auth': {
                'citizen': {
                    'certFingerprint': get_serial_number(sign['certificate']),
                    'regnum': REGNUM,
                    'signature': sign['signature'],
                    'appAuthToken': None,
                    'authAppName': None,                
                    'civilId': None,
                    'fingerprint': b'*** NO ACCESS ***',
                    'otp': 0,
                },
                'operator': {
                    'appAuthToken': None,
                    'authAppName': None,
                    'certFingerprint': None,
                    'civilId': None,
                    'fingerprint': b'*** NO ACCESS ***',
                    'otp': 0,
                    'regnum': None,
                    'signature': None
                }
            },
            'regnum': REGNUM
        }
    citizen = Service('https://xyp.gov.mn/citizen-1.5.0/ws?WSDL', timestamp, pkey_path=KEY_PATH)
    citizen.dump('WS100101_getCitizenIDCardInfo', params)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

"""
esign client программыг ашиглаж regnum.timestamp мэдээллийг тоон гарын үсгээр баталгаажуулах хүсэлт явуулах

@author unenbat
@since 2023-05-23
"""
def on_open(ws):
    def run(*args):
        dataSign = REGNUM + "." + timestamp
        x =  '{"type":"e457cb50ed64bde0","data":"'+dataSign+'"}'
        time.sleep(1)
        ws.send(x)
        time.sleep(1)
        result = ws.recv()
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    timestamp = str(int(time.time()))
    ws = websocket.WebSocketApp(WEBSOCKETURL,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()