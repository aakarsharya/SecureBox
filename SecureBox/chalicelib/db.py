import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore

dynamodb = boto3.resource('dynamodb')

class Database:
    m_table = dynamodb.Table('ClientData')
    
    def openBox(self, boxID, access):
        try:
            item = self.getItem(boxID)
            if str(access) == item['access_code']:
                return True
            if str(access) in item['orders']:
                self.deleteOrder(boxID, access)
                return True
            return False
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException': # check this error
                return False
            else:
                raise e

    def register(self, boxID, access_code, orders, lock_status, phone_number, email, password):
        item = {
            'box_id': int(boxID),
            'access_code': str(access_code),
            'orders': set(orders),
            'locked': bool(lock_status),
            'phone_number': str(phone_number),
            'email': str(email),
            'password': str(password),
        }
        try:
            self.m_table.put_item(
                Item=item
            )
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                print('This box_id already exists.')
            else:
                raise e
            return False

    def unregister(self, boxID):
        self.m_table.delete_item(
            Key = {'box_id': int(boxID)}
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

    def setEmail(self, boxID, email):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET email = :new_email',
            ExpressionAttributeValues = {':new_email': email}
        )
        
    def getEmail(self, boxID):
        item = self.getItem(int(boxID))
        return item['email']

    def setPhoneNumber(self, boxID, phone_number):
        self.m_table.update_item(
            Key = {'box_id': int(boxID)},
            UpdateExpression = 'SET phone_number = :num',
            ExpressionAttributeValues = {':num': phone_number}
        )

    def getPhoneNumber(self, boxID):
        item = self.getItem(int(boxID))
        return item['phone_number']
