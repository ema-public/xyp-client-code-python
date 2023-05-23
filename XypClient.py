# -- coding: utf-8 --
from collections.abc import Mapping
#//
import zeep, base64
from zeep import Client
from zeep.transports import Transport
from XypSign import XypSign
from requests import Session
import urllib3
from env import ACCESS_TOKEN

"""
ХУР Төрийн Мэдээлэл Солилцооны системээс сервис дуудах 

@author unenbat
@since 2023-05-23
"""
class Service():
    def __init__(self, wsdl, timestamp, pkey_path=None):
        print("timestamp: ", timestamp)
        self.__accessToken = ACCESS_TOKEN
        self.__toBeSigned, self.__signature = XypSign(pkey_path).sign(self.__accessToken, timestamp)
        self.__signature = self.__signature
        urllib3.disable_warnings()
        session = Session()
        session.verify = False
        transport = zeep.Transport(session=session)
    
        self.client = zeep.Client(wsdl, transport=transport)
        self.client.transport.session.headers.update({
            'accessToken': self.__accessToken,
            'timeStamp' : timestamp,
            'signature' : self.__signature
        })
    
    def deep_convert_unicode(self, key, layer):
    
        to_ret = layer
    
        if isinstance(layer, bytes) and (key == 'image' or key == 'driverPic'):
            to_ret = base64.b64encode(layer)
    
        try:
            for key, value in to_ret.items():
                to_ret[key] = self.deep_convert_unicode(key, value)
        except AttributeError:
            pass
        return to_ret
        
    def deep_convert_dict(self,  layer):
    
        to_ret = layer
    
        if isinstance(layer, bytes):
            to_ret = dict(layer)
    
        try:
            for key, value in to_ret.items():
                to_ret[key] = self.deep_convert_dict(value)
        except AttributeError:
            pass
        return to_ret
    
    def dump(self, operation, params=None):
        try:
            if params:
                response = self.client.service[operation](params)
                print(response)
            else:
                print(self.client.service[operation]())
        except Exception as e:
            print( operation, str(e))
    
