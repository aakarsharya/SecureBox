from chalice import Chalice
from chalicelib import Database
import json

app = Chalice(app_name='SecureBox')
app.debug = True
db = Database()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    request = app.current_request.json_body    
    authorized = db.openBox(request['box_id'], request['code'])
    return {'Open': authorized}

@app.route('/register', methods=['POST'])
def register():
    request = app.current_request.json_body
    registered = db.register(request['box_id'], request['access_code'], request['phone_number'], request['username'])
    return {"Registered": registered}

@app.route('/addOrder', methods=['POST'])
def addOrder():
    request = app.current_request.json_body
    db.addOrder(request['box_id'], request['tracking_id'])
    return {'Added': True}

@app.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    request = app.current_request.json_body
    db.deleteOrder(request['box_id'], request['tracking_id'])

@app.route('/unregister', methods=['POST'])
def unregister():
    request = app.current_request.json_body
    db.unregister(request['box_id'])

@app.route('/setLockStatus', methods=['POST'])
def setLockStatus():
    request = app.current_request.json_body
    db.setLockStatus(request['box_id'], request['locked'])

@app.route('/getLockStatus', methods=['POST'])
def getLockStatus():
    request = app.current_request.json_body
    lock_status = db.getLockStatus(request['box_id'])
    return {'locked': lock_status}

@app.route('/setUsername', methods=['POST'])
def setUsername():
    request = app.current_request.json_body
    db.setUsername(request['box_id'], request['username'])

@app.route('/getUsername', methods=['POST'])
def getUsername():
    request = app.current_request.json_body
    username = db.getUsername(request['box_id'])
    return {'username': username}

@app.route('/setPhoneNumber', methods=['POST'])
def setPhoneNumber():
    request = app.current_request.json_body
    db.setPhoneNumber(request['box_id'], request['phone_number'])

@app.route('/getPhoneNumber', methods=['POST'])
def getPhoneNumber():
    request = app.current_request.json_body
    phone_number = db.getPhoneNumber(request['box_id'])
    return {'phone_number': phone_number}

@app.route('/setAccessCode', methods=['POST'])
def setPhoneNumber():
    request = app.current_request.json_body
    db.setAccessCode(request['box_id'], request['access_code'])

@app.route('/viewOrders', methods=['POST'])
def viewOrders():
    request = app.current_request.json_body
    orders = db.getOrders(request['box_id'])
    return {"Orders": list(orders)}


