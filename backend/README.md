# SecureBox

Communication:
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
