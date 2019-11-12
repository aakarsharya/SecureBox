import RPi.GPIO as GPIO
import Keypad
import json

ROWS = 4
COLS = 4
keys = ['1', '2', '3', 'A',
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D']
rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]

def loop():
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


                   
if __name__ == '__main__':
    print('Program is starting...')
    try:
        code = loop()
        print("Your code is " + code)
    except KeyboardInterrupt:
        GPIO.cleanup()
