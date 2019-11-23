import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUM")

# DynamoDB
dynamodb = boto3.resource('dynamodb')

# Twilio API setup
client = Client(ACCOUNT_SID, AUTH_TOKEN)

class Database:
    m_table = dynamodb.Table('ClientData')

    def openBox(self, boxID, access):
        item, exists = self.getItem(boxID)
        if exists:
            if str(access) == item['access_code']:
                return True
            if str(access) in item['orders']:
                self.textUser(item['phone_number'], item['username'], trackingID=access)
                self.deleteOrder(boxID, access)
                return True
        return False

    def register(self, boxID, access_code, phone_number, username):
        response = self.m_table.query(
            KeyConditionExpression=Key('box_id').eq(int(boxID))
        )
        try:
            if (boxID == response['Items'][0]['box_id']):
                return False
        except IndexError:
            item = {
                'box_id': int(boxID),
                'access_code': str(access_code),
                'locked': True,
                'phone_number': str(phone_number),
                'username': str(username)
            }
            self.m_table.put_item(
                Item=item
            )       
            self.textUser(phone_number, username, trackingID=None, event='register') 
            return True

    def unregister(self, boxID):
        self.m_table.delete_item(
            Key = {'box_id': int(boxID)}
        )
    
    def textUser(self, phoneNumber, username, trackingID, event='authenticate'):
        if event == 'register':
            try:
                client.messages.create(
                    to=phoneNumber,
                    from_=TWILIO_NUM,
                    body='Hey ' + username + '! Thanks for registering with SecureBox. Add a new order from the home page!'
                )
            except TwilioRestException:
                print('add number to twilio account')
        else:
            try: 
                client.messages.create(
                    to=phoneNumber,
                    from_=TWILIO_NUM,
                    body='Hey ' + username + '! Your order with tracking ID: ' + trackingID + ' has arrived. \nIt is safe with SecureBox!'
                )
            except TwilioRestException:
                print('add phone number to twilio account')

    
    def addOrder(self, boxID, tracking_id):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'ADD orders :new_order',
            ExpressionAttributeValues = {':new_order': {tracking_id}}
        )
    
    def deleteOrder(self, boxID, tracking_id):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'DELETE orders :order',
            ExpressionAttributeValues = {':order': {tracking_id}}
        )

    def getOrders(self, boxID):
        item, exists = self.getItem(boxID)
        if exists:
            try:
                return item['orders']
            except KeyError:
                return {'no orders.'}
        return {'invalid box ID.'}

    def getItem(self, boxID):
        try:
            item = self.m_table.get_item(
                Key={'box_id': int(boxID)}
            )
            return item['Item'], True
        except KeyError:
            return 'invalid box ID.', False

    def setLockStatus(self, boxID, lockStatus):
        self.m_table.update_item(
            Key = {'box_id': boxID},
            UpdateExpression = 'SET locked = :status',
            ExpressionAttributeValues = {':status': lockStatus}
        )
    
    def getLockStatus(self, boxID):
        item, exists = self.getItem(int(boxID))
        if exists:
            return item['locked']
        return 'invalid box ID.'

    def setAccessCode(self, boxID, access_code):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET access_code = :code',
            ExpressionAttributeValues = {':code': access_code}
        )
    
    def getAccessCode(self, boxID):
        item, exists = self.getItem(int(boxID))
        if exists:
            return item['access_code']
        return 'invalid box ID.'

    def setUsername(self, boxID, username):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET username = :username',
            ExpressionAttributeValues = {':username': username}
        )
        
    def getUsername(self, boxID):
        item, exists = self.getItem(int(boxID))
        if exists:
            return item['username']
        return 'invalid box ID.'

    def setPhoneNumber(self, boxID, phone_number):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET phone_number = :num',
            ExpressionAttributeValues = {':num': phone_number}
        )

    def getPhoneNumber(self, boxID):
        item, exists = self.getItem(int(boxID))
        if exists:
            return item['phone_number']
        return 'invalid box ID.'