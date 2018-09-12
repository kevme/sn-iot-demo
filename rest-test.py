#!/usr/bin/env python3

import requests;
from requests.auth import HTTPBasicAuth
import time
import random
import datetime


randomNumber = random.randint(40,60)
print(randomNumber)
currentDateTime = datetime.datetime.now().replace(microsecond=0).isoformat()
#ms = int(round(time.time() * 1000))
print(currentDateTime)
headers = {'Content-Type': 'application/json'}
url = 'https://kmet05demo.service-now.com/api/now/v1/clotho/put'


data = '''{"seriesRef":
{"subject":"4e7874a8dbe8e700c58f7a6eaf9619c7",
"table":"u_cmdb_ci_machinery",
"metric":"u_motor_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(randomNumber)+'''}
]
}'''

resp = requests.post(url, data=data, headers=headers, auth=('iot_demo', 'SNIoT1234'))

print(resp.status_code)
print(resp.text)
