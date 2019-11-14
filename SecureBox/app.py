from chalice import Chalice
from chalicelib import Database
import json

app = Chalice(app_name='SecureBox')
app.debug = True
db = Database()

@app.route('/authenticateUser', methods=['POST'])
def authenticateUser():
    request = app.current_request.json_body  # payload of check
    authorized = db.open_box(request['box_id'], request['access_code'])
    return {'Open': request}

@app.route('/register', methods=['POST'])
def register():
    request = app.current_request.json_body
    registered = db.register(request['box_id'], request['access_code'], request['orders'], request['locked'], 
                request['phone_number'], request['email'], request['password'])
    return {'Registered': registered}

@app.route('/addOrder', methods=['POST'])
def addOrder():
    request = app.current_request.json_body
    db.addOrder(request['box_id'], request['tracking_id'])

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

@app.route('/setEmail', methods=['POST'])
def setEmail():
    request = app.current_request.json_body
    db.setEmail(request['box_id'], request['email'])

@app.route('/getEmail', methods=['POST'])
def getEmail():
    request = app.current_request.json_body
    email = db.getEmail(request['box_id'])
    return {'email': email}

@app.route('/setPhoneNumber', methods=['POST'])
def setPhoneNumber():
    request = app.current_request.json_body
    db.setPhoneNumber(request['box_id'], request['phone_number'])

@app.route('/getPhoneNumber', methods=['POST'])
def getPhoneNumber():
    request = app.current_request.json_body
    phone_number = db.getPhoneNumber(request['box_id'])
    return {'phone_number': phone_number}


