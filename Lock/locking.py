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
redLED = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redLED, GPIO.OUT)

def inputAccessCode():
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
    keypad.setDebounceTime(50)
    count = 0
    access_code = ''
    while(count < 4):
        key = keypad.getKey()
        if (key != keypad.NULL):
            count += 1
            access_code += key
    return access_code

def turnOnLights(correct):
    if (correct == False):
        GPIO.output(redLED, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(redLED, GPIO.LOW)

    

if __name__ == '__main__':
    print('Program is starting...')
    try:
        turnOnLights(False)
        code = inputAccessCode()
        print("Your code is " + code)
    except KeyboardInterrupt:
        GPIO.cleanup()
