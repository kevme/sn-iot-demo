import sys
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO


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
speedControl=GPIO.PWM(motorSpeed,1000)
speedControl.start(currentSpeed)

#Anemo setup
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 2


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
        print(value)
        x='z'

    elif x=='e':
        GPIO.cleanup()
        print("Exit")
        break
