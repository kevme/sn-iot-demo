import sys
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from simple_pid import PID
import atexit
import requests;
from requests.auth import HTTPBasicAuth
import datetime



#Motor setup
motor1=24
motor2=23
motorSpeed = 18
currentSpeed = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)
GPIO.setup(motorSpeed, GPIO.OUT)
GPIO.output(motor1, GPIO.LOW)
GPIO.output(motor2, GPIO.LOW)
speedControl=GPIO.PWM(motorSpeed,100)
speedControl.start(currentSpeed)

#Anemo setup
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 2

#PID setup
pid = PID(1, 0.1, 0.05, setpoint=440)
pid.sample_time = 1
pid.output_limits = (30, 90)

#Switch Setup
switch1 = 17
GPIO.setup(switch1, GPIO.IN,GPIO.PUD_UP)



#exit
def exitProgram():
    GPIO.cleanup()
    print("EXIT")

atexit.register(exitProgram)

def startMotor():
    GPIO.output(motor1, GPIO.HIGH)
    print("Starting motor...")

def stopMotor():
    GPIO.output(motor1, GPIO.LOW)
    print("Stopping motor...")

#Calculate when one minute passed
oldEpoche = time.time()

def minutePassed():
    global oldEpoche
    currentEpoche = time.time()
    if (currentEpoche - oldEpoche >=60):
        oldEpoche = currentEpoche
        return True

    return False

#variables for while loop
switch1On = False
pid.auto_mode = False

lowestValue = 450
windAvg = 450
windValueArray = []
motorValueArray = []
numberOfReadings = 20

headers = {'Content-Type': 'application/json'}
url = 'https://kmet05demo.service-now.com/api/now/v1/clotho/put'

def mean(valueArray):
    return float(sum(valueArray)) / max(len(valueArray),1)

while(1):
    if GPIO.input(switch1) == GPIO.HIGH and switch1On == False:
        print("switch 1 on")
        switch1On = True
        startMotor()
        pid.auto_mode = True

    if GPIO.input(switch1) == GPIO.LOW and switch1On == True:
        print("switch 1 off")
        switch1On = False
        pid.auto_mode = False
        stopMotor()

    if switch1On == True:
        value = adc.read_adc(0, gain=GAIN)
        windValueArray.append(value)
        windAvg = mean(windValueArray)

        if len(windValueArray) == numberOfReadings:
            windValueArray.pop(0)


        control = pid(value)
        motorValueArray.append(control)
        motorAvg = mean(motorValueArray)
        if len(motorValueArray) == numberOfReadings:
            motorValueArray.pop(0)
        speedControl.ChangeDutyCycle(control)

    if minutePassed():
        print("Wind: "+str(windAvg))
        print("Motor: "+str(motorAvg))
        print("Minute passed")
        currentDateTime = datetime.datetime.now().replace(microsecond=0).isoformat()
        windData = '''{"seriesRef":
            {"subject":"1a8ed349dba46b00c58f7a6eaf9619e1",
                    "table":"x_snc_ma_maint_u_cmdb_ci_machine",
                    "metric":"wind_speed"},
            "values":[
                    {"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(windAvg)+'''}
                    ]
            }'''
        resp = requests.post(url, data=windData, headers=headers, auth=('iot_demo', 'SNIoT1234'))

        windData = '''{"seriesRef":
            {"subject":"1a8ed349dba46b00c58f7a6eaf9619e1",
                    "table":"x_snc_ma_maint_u_cmdb_ci_machine",
                    "metric":"motor_speed"},
            "values":[
                    {"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(motorAvg)+'''}
                    ]
            }'''
        resp = requests.post(url, data=windData, headers=headers, auth=('iot_demo', 'SNIoT1234'))

    time.sleep(0.5)
