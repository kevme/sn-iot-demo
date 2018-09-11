import sys
import time
import RPi.GPIO as GPIO


input=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True: # Run forever
    if GPIO.input(input) == GPIO.HIGH:
        print("Button was pushed!")
