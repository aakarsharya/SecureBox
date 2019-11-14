import RPi.GPIO as GPIO
import Keypad
import time
import requests
import json

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

# API calls
url = 'https://habnjhheq5.execute-api.us-east-2.amazonaws.com/secureBox-api/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Box ID
BOX_ID = 123456

def inputKeys():
    """
    print('Enter * for access_code, # for tracking_id')
    
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
    keypad.setDebounceTime(50)
    parameter = ''
    code = ''
    key = ''
    while (key != '#' and key != '*'):
        key = keypad.getKey()    
    if (key == '*'):
        parameter = "access_code"
    elif (key == '#'):
        parameter = "tracking_id"
    """
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
    print("Enter access code or tracking ID followed by *")
    keypad.setDebounceTime(50)
    key = ''
    while(key != '*'):
        key = keypad.getKey()
        if (key != keypad.NULL and key != '*'):
            code += key
    return code

def turnOnLights(correct):
    if (correct == True):
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(GREEN_LED, GPIO.LOW)
    else:
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(RED_LED, GPIO.LOW)

def authenticate():
    data = {'box_id': BOX_ID, 'code': inputKeys()}
    response = requests.post(url+'authenticate', json=data, headers=headers).json()
    turnOnLights(response['Open'])

if __name__ == '__main__':
    print('Program is starting...')
    try:
        authenticate()
    except KeyboardInterrupt:
        GPIO.cleanup()
