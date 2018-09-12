import sys
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from simple_pid import PID


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
pid = PID(1, 0.1, 0.05, setpoint=450)
pid.sample_time = 1
pid.output_limits = (30, 90)


def startMotor():
    GPIO.output(motor1, GPIO.HIGH)
    print("Starting motor...")

def stopMotor():
    GPIO.output(motor1, GPIO.LOW)
    print("Stopping motor...")


while(1):
    x=input()

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
