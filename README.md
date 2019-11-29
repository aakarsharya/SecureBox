# SecureBox

## SecureBox Website
[Homepage](https://aakarsharya.github.io/SecureBox/)
The SecureBox homepage is used to authenticate the user, who can then access and set personal information including:
- Orders/Add Order
- Get Box Status (locked/unlocked)
- Reset Access Code
- Register (for new users) 

## Installation (if you have a Rasberry Pi)
First, clone the repository to your Desktop.
```bash
git clone https://github.com/aakarsharya/SecureBox.git
```
Then, clone these Freenove libraries to you Desktop from this [link](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi) and copy the following files into the box directory. This libraries are used by the box's keypad, lights, and LCD display.
```bash
git clone https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi.git
cp ~/Desktop/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/Code/Python_Code/22.1.1_MatrixKeypad/Keypad.py ~/Desktop/SecureBox/box
cp ~/Desktop/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/Code/Python_Code/20.1.1_I2CLCD1602/Adafruit_LCD1602.py ~/Desktop/SecureBox/box
cp ~/Desktop/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/Code/Python_Code/20.1.1_I2CLCD1602/PCF8574.py ~/Desktop/SecureBox/box
```

## Hardware Setup

## Running the program
To run the program, simply enter the following command into your Rasberry Pi's terminal from the box directory using the following commands.
```bash
cd ~/Desktop/SecureBox/box
python box.py
```
Follow the instructions displayed on the LCD Display.

## Tech Stack
### Backend
Python
AWS APIGateway
AWS Lambda
AWS DynamoDB
Chalice

### Frontend
Javscript
HTML
CSS

## How it Works
1. RasberryPi -> Gateway -> Lambda -> DynamoDB:		Provide Lock Status, check access code, 
2. Website S3 -> Gateway -> Lambda -> DynamoDB		Get Lock Status, Register user, update order info

Lambda:
- functions used by website:
	- authenticate_website()			// through password + email
	- register()				
	- deleteUser()				
	- addOrder()				
	- deleteOrder()						// month after order is entered or manually
	- getLockStatus()			
	- setPassword()				
	- setEmail()				
	- setPhoneNumber()			
- functions used by RasberryPi:	
	- authenticate_pi()					// through access_code + box_id
	- deleteOrder()						// when tracking_id is entered 
	- setLockStatus()			
	- setAccessCode()			
	- getPhoneNumber()			
	- getEmail()				
	
RasberryPi:
- unlock()						
- lock()						
- notifyUser() 							// text user when box is unlocked, then locked (order has arrived)
- inputAccessCode()						// unlock if access code matches code in database
- inputTrackingID()						// unlock if tracking_id exists in orders[]
- resetAccessCode()				
- wait20seconds()						// time for delivery man to drop off package in box

Website:
- Login/Register						// Using Amazon Cognito user pools
- View my Orders + Box Status			// refresh button to check current box lock status 
- Edit My Profile 						// change phone number, email, password, access_code.

TODO:
- Create functions to call REST API from RasberryPi				// November 15
- RasberryPi program hardware									// November 15
- Test RasberryPi read/write to database + texting feature		// November 17
- Website UI 											        // November 24
- Test Website read/write to database 							// December 1
- Make box + locking servo motors								// December 6
- Test AWS Gateway -> Lambda and cleanup front-end				// December 19

Bugs:
- Website input invalid box id (add try catch for key error in app.py/db.py)
- add helper text in text fields
