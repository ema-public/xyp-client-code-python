from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA 

class XypSign:
    def __init__(self, KeyPath):
        self.KeyPath = KeyPath
    
    def __GetPrivKey(self):
        with open(self.KeyPath, "rb") as keyfile:
            return RSA.importKey(keyfile.read())
    
    def __toBeSigned(self, accessToken, timestamp):
        return {
            'accessToken' : accessToken,
            'timeStamp' : timestamp,
        }
    
    def __buildParam(self, toBeSigned):        
        print(toBeSigned['accessToken'] + '.' + toBeSigned['timeStamp'])
        return toBeSigned['accessToken'] + '.' + toBeSigned['timeStamp']
            
    def sign(self, accessToken, timestamp):
        toBeSigned = self.__toBeSigned(accessToken, timestamp)
        digest = SHA256.new()
        digest.update(self.__buildParam(toBeSigned).encode('utf8'))
        pkey = self.__GetPrivKey()
        signature = b64encode(PKCS1_v1_5.new(pkey).sign(digest))
        return toBeSigned, signature
    
