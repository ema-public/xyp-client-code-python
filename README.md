# xyp-client-code-python
Төрийн мэдээлэл солилцооны ХУР системийн хэрэглэгчийн жишээ кодыг Python хэл дээр бэлтгэв.

## Шаардлага
    Python 3.9.13

    cat requirements.txt
    
    appdirs==1.4.3
    cached-property==1.3.1
    certifi==2017.7.27.1
    chardet==3.0.4
    defusedxml==0.5.0
    idna==2.6
    isodate==0.6.0
    lxml==4.1.1
    pytz==2017.3
    requests==2.18.4
    requests-toolbelt==0.8.0
    six==1.11.0
    urllib3==1.22
    zeep==4.2.1
    pycrypto==2.6.1
    
    $ pip install -r requirements.tx

[env.py](./env.py) файлд шаардлагатай мэдээллийг бөглөх. Үүнд:
```python
#ҮДТ - өөс олгогдсон accessToken мэдээлэл
ACCESS_TOKEN="123143d2f8ae93b24a47c6d31241"
#ҮДТ өөс олгогдсон openVPN key-ийн мэдээллийг агуулж буй файлын зам.
KEY_PATH="mykey.key"
#Иргэний регистрийн дугаар
REGNUM="XX00000000"
#Тоон гарын үсэг зурах client программын  local дээр ажиллаж буй хаяг. 
#ESIGN CLIENT программын хувьд тогтмол "127.0.0.1:97001" байна.
WEBSOCKETURL="ws://127.0.0.1:59001"
```
[mykey.key](./mykey.key) файлд ҮДТ өөс олгогдсон openVPN key-ийн мэдээллийг хуулна.

ESIGN клиент програм (Win 7, 8, 10 64 бит) [татах](https://ra.datacenter.gov.mn/software/installer).
## Сервис дуудах
Иргэнийг тоон гарын үсгээр баталгаажуулан дуудахдаа [DigitalSignatureApprove.py](./DigitalSignatureApprove.py) кодыг ажиллуулна.
```bash
python DigitalSignatureApprove.py
```
Иргэнийг OTP кодоор баталгаажуулан дуудахдаа [OTPApprove.py](./OTPApprove.py) кодыг ажиллуулна.
```bash
python OTPApprove.py
``` 