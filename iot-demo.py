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
pid.sample_time = 2
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

oldEpoche = time.time()

def minutePassed():
    global oldEpoche
    currentEpoche = time.time()
    if (currentEpoche - oldEpoche >=60):
        oldEpoche = currentEpoche
        return True

    return False

switch1On = False
pid.auto_mode = False

lowestValue = 450
avg = 450
valueArray = []
numberOfReadings = 20

headers = {'Content-Type': 'application/json'}
url = 'https://kmet05demo.service-now.com/api/now/v1/clotho/put'

def mean(valueArray):
    return float(sum(valueArray)) / max(len(valueArray),1)

while(1):
    #x=input()
    x='z'
    
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


    if x=='f':
        startMotor()
        x='z'

    elif x=='s':
        stopMotor()
        x='z'

    elif x=='u':
        if currentSpeed < 95:
            currentSpeed = currentSpeed + 5

        speedControl.ChangeDutyCycle(currentSpeed)
        print("Speed:" +str(currentSpeed))
        x='z'

    elif x=='d':
        if currentSpeed > 20:
            currentSpeed = currentSpeed - 5

        speedControl.ChangeDutyCycle(currentSpeed)
        print("Speed:" +str(currentSpeed))
        x='z'

    elif x=='r':
        value = adc.read_adc(0, gain=GAIN)

        control = pid(value)
        print("Windspeed: "+str(value))
        print("Control: "+str(control))
        x='z'

    elif x=='e':
        GPIO.cleanup()
        print("Exit")
        break
    
    
    if switch1On == True:
        value = adc.read_adc(0, gain=GAIN)
        valueArray.append(value)
        avg = mean(valueArray)
        
        if len(valueArray) == numberOfReadings:
            valueArray.pop(0)

        
        control = pid(value)
        speedControl.ChangeDutyCycle(control)
    
    if minutePassed():
        print(avg)
        print("Minute passed")
        currentDateTime = datetime.datetime.now().replace(microsecond=0).isoformat()
        data = '''{"seriesRef":
            {"subject":"4e7874a8dbe8e700c58f7a6eaf9619c7",
                    "table":"u_cmdb_ci_machinery",
                    "metric":"u_motor_speed"},
            "values":[
                    {"timestamp":"'''+str(currentDateTime)+'''Z", "value":'''+str(avg)+'''}
                    ]
            }'''
        resp = requests.post(url, data=data, headers=headers, auth=('iot_demo', 'SNIoT1234'))

    time.sleep(0.5)
