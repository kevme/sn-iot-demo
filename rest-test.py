#!/usr/bin/env python3

import requests;
from requests.auth import HTTPBasicAuth
import time
import random
import datetime


randomNumber = random.randint(435,450)
random2 = random.randint(40,50)
print(randomNumber)
currentDateTime = datetime.datetime.now().replace(microsecond=0).isoformat()
#ms = int(round(time.time() * 1000))
print(currentDateTime)
headers = {'Content-Type': 'application/json'}
url = 'https://kmet05demo.service-now.com/api/now/v1/clotho/put'


data = '''{"seriesRef":
{"subject":"1a8ed349dba46b00c58f7a6eaf9619e1",
"table":"x_snc_ma_maint_u_cmdb_ci_machine",
"metric":"wind_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(randomNumber)+'''}
]
}'''

resp = requests.post(url, data=data, headers=headers, auth=('iot_demo', 'SNIoT1234'))

data2 = '''{"seriesRef":
{"subject":"1a8ed349dba46b00c58f7a6eaf9619e1",
"table":"x_snc_ma_maint_u_cmdb_ci_machine",
"metric":"motor_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(random2)+'''}
]
}'''

resp = requests.post(url, data=data2, headers=headers, auth=('iot_demo', 'SNIoT1234'))

print(resp.status_code)
print(resp.text)
