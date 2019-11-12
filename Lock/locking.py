import RPi.GPIO as GPIO
import Keypad
import json
import time

# keypad global variables
ROWS = 4
COLS = 4
keys = ['1', '2', '3', 'A',
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D']
rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]

# LED global variables
RED_LED = 33
GREEN_LED = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)


def inputAccessCode():
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
    keypad.setDebounceTime(50)
    access_code = ''
    key = ''
    while(key != '*'):
        key = keypad.getKey()
        if (key != keypad.NULL and key != '*'):
            access_code += key
    return access_code

def turnOnLights(correct):
    if (correct == True):
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(GREEN_LED, GPIO.LOW)
    else:
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(RED_LED, GPIO.LOW)

    
if __name__ == '__main__':
    print('Program is starting...')
    try:
        turnOnLights(False)
        time.sleep(2)
        turnOnLights(True)
        code = inputAccessCode()
        print("Your code is " + code)
    except KeyboardInterrupt:
        GPIO.cleanup()
