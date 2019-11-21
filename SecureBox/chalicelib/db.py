import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore
import os
from twilio.rest import Client
#from chalicelib.env import AUTH_TOKEN, ACCOUNT_SID, TWILIO_NUM
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
        item = self.getItem(boxID)
        if str(access) == item['access_code']:
            return True
        if str(access) in item['orders']:
            self.textUser(item['phone_number'], access, item['username'])
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
            return True

    def unregister(self, boxID):
        self.m_table.delete_item(
            Key = {'box_id': int(boxID)}
        )
    
    def textUser(self, phoneNumber, trackingID, username):
        client.messages.create(
            to=phoneNumber,
            from_=TWILIO_NUM,
            body='Hey ' + username + '! Your order with tracking ID: ' + trackingID + ' has arrived. \nIt is safe with SecureBox!'
        )
    
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
        item = self.getItem(boxID)
        return item['orders']

    def getItem(self, boxID):
        item = self.m_table.get_item(
            Key={'box_id': int(boxID)}
        )
        return item['Item']

    def setLockStatus(self, boxID, lockStatus):
        self.m_table.update_item(
            Key = {'box_id': boxID},
            UpdateExpression = 'SET locked = :status',
            ExpressionAttributeValues = {':status': lockStatus}
        )
    
    def getLockStatus(self, boxID):
        item = self.getItem(int(boxID))
        return item['locked']

    def setAccessCode(self, boxID, access_code):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET access_code = :code',
            ExpressionAttributeValues = {':code': access_code}
        )
    
    def getAccessCode(self, boxID):
        item = self.getItem(int(boxID))
        return item['access_code']

    def setUsername(self, boxID, username):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET username = :username',
            ExpressionAttributeValues = {':username': username}
        )
        
    def getUsername(self, boxID):
        item = self.getItem(int(boxID))
        return item['username']

    def setPhoneNumber(self, boxID, phone_number):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET phone_number = :num',
            ExpressionAttributeValues = {':num': phone_number}
        )

    def getPhoneNumber(self, boxID):
        item = self.getItem(int(boxID))
        return item['phone_number']

