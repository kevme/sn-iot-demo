#!/usr/bin/env python3

import requests;
from requests.auth import HTTPBasicAuth
import time
import random
import datetime


windSpeed = random.randint(435,450)
motorSpeed = random.randint(40,50)
windSpeed2 = random.randint(435,450)
motorSpeed2 = random.randint(40,50)
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
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(windSpeed)+'''}
]
}'''

resp = requests.post(url, data=data, headers=headers, auth=('iot_demo', 'SNIoT1234'))

data2 = '''{"seriesRef":
{"subject":"1a8ed349dba46b00c58f7a6eaf9619e1",
"table":"x_snc_ma_maint_u_cmdb_ci_machine",
"metric":"motor_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(motorSpeed)+'''}
]
}'''

resp = requests.post(url, data=data2, headers=headers, auth=('iot_demo', 'SNIoT1234'))

data = '''{"seriesRef":
{"subject":"2b1b9c15db686b00c58f7a6eaf9619aa",
"table":"x_snc_ma_maint_u_cmdb_ci_machine",
"metric":"wind_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(windSpeed2)+'''}
]
}'''

resp = requests.post(url, data=data, headers=headers, auth=('iot_demo', 'SNIoT1234'))

data2 = '''{"seriesRef":
{"subject":"2b1b9c15db686b00c58f7a6eaf9619aa",
"table":"x_snc_ma_maint_u_cmdb_ci_machine",
"metric":"motor_speed"},
"values":[
{"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(motorSpeed2)+'''}
]
}'''

resp = requests.post(url, data=data2, headers=headers, auth=('iot_demo', 'SNIoT1234'))

print(resp.status_code)
print(resp.text)
