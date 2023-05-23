from XypClient import Service
from env import KEY_PATH
from env import REGNUM
import time


def CallXYPService(OTPNumber):
    params = {  
        'auth': {
                'citizen': {
                    'certFingerprint': None,
                    'regnum': REGNUM,
                    'signature': None,
                    'appAuthToken': None,
                    'authAppName': None,                
                    'civilId': None,
                    'fingerprint': b'*** NO ACCESS ***',
                    'otp': OTPNumber,
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
            'regnum': REGNUM,
        }
    citizen = Service('https://xyp.gov.mn/citizen-1.5.0/ws?WSDL', str(int(time.time())) , pkey_path=KEY_PATH)
    citizen.dump('WS100101_getCitizenIDCardInfo', params)

def OTPservice():
    params = {  
        'auth': {
                'citizen': {
                    'certFingerprint': None,
                    'regnum': REGNUM,
                    'signature': None,
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
            'regnum': REGNUM,
            'jsonWSList': "[{\"ws\":\"WS100101_getCitizenIDCardInfo\"}]",
            'isSms': 1,
            'isApp': 0,
            'isEmail': 0,
            'isKiosk': 0,
            'phoneNum': 0,
        }
    citizen = Service('https://xyp.gov.mn/meta-1.5.0/ws?WSDL', str(int(time.time())) , pkey_path=KEY_PATH)
    citizen.dump('WS100008_registerOTPRequest', params)
    print("-----------------------------------------------------------")
    print("-----------------------------------------------------------")
    OTPMessageNumber = int(input("Иргэнд ирсэн OTP кодыг оруулна уу: "))
    CallXYPService(OTPMessageNumber)
    
    
if __name__ == "__main__":
    OTPservice()
    