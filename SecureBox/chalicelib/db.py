import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore

dynamodb = boto3.resource('dynamodb')

class Database:
    m_table = dynamodb.Table('ClientData')
    m_size = 0
    #def authenticate(self, boxID):


    def register(self, boxID, phone_number, email, password, orders, access_code, lock_status):
        item = {
            'box_id': boxID,
            'access_code': access_code,
            'email': email,
            'orders': orders,
            'password': access_code,
            'phone_number': phone_number,
            'locked': lock_status
        }
        try:
            self.m_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(box_id)'
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                print('This box_id already exists.')

    def deleteItem(self, boxID):
        self.m_table.delete_item(
            Key = {'box_id':boxID}
        )
    
    def addOrder(self, boxID, tracking_id):
        self.m_table.update_item(
            Key = {'box_id':boxID},
            UpdateExpression = 'ADD orders :new_order',
            ExpressionAttributeValues = {':new_order': {tracking_id}}
        )
    
    def deleteOrder(self, boxID, tracking_id):
        self.m_table.update_item(
            Key = {'box_id':boxID},
            UpdateExpression = 'DELETE orders :order',
            ExpressionAttributeValues = {':order': {tracking_id}}
        )

    def setLockStatus(self, boxID, lockStatus):
        self.m_table.update_item(
            Key = {'box_id': boxID},
            UpdateExpression = 'SET locked = :status',
            ExpressionAttributeValues = {':status': lockStatus}
        )

    def setAccessCode(self, boxID, access_code):
        self.m_table.update_item(
            Key = {'box_id': boxID},
            UpdateExpression = 'SET access_code = :code',
            ExpressionAttributeValues = {':code': access_code}
        )

    def getItem(self, boxID):
        item = self.m_table.get_item(
            Key={'box_id':boxID}
        )
        return item['Item']

    def getLockStatus(self, boxID):
        item = self.getItem(boxID)
        return item['locked']

db = Database()