import RPi.GPIO as GPIO
import Keypad
import time
import requests
import json

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime

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

# LCD setup
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
mcp.output(3,1)     # turn on LCD backlight
lcd.begin(16,2)     # set number of LCD lines and columns

# API calls
url = 'https://habnjhheq5.execute-api.us-east-2.amazonaws.com/secureBox-api/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Box ID
BOX_ID = 123456

def inputKeys():
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
    lcd.message("Enter access code or tracking ID followed by *")
    time.sleep(2)
    lcd.clear()
    keypad.setDebounceTime(50)
    key = ''
    code = ''
    while(key != '*'):
        key = keypad.getKey()
        if (key != keypad.NULL and key != '*'):
            code += key
    lcd.message("You entered: " + code)
    time.sleep(2)
    lcd.clear()
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
    if (response['Open']):
        lcd.message("SUCCESS!")
        time.sleep(1)
        lcd.clear()
    else:
        lcd.message("INCORRECT CODE/ID")
        time.sleep(1)
        lcd.clear()

if __name__ == '__main__':
    print('Program is starting...')
    try:
        authenticate()
    except KeyboardInterrupt:
        GPIO.cleanup()
