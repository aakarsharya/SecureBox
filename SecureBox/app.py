from chalice import Chalice
from SecureBox.chalicelib import Database, CURRENT_ENV

app = Chalice(app_name='SecureBox')
app.debug = True
db = Database()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    request = app.current_request.json_body  # payload of check
    authorized = db.open_box(request['box_id'], request['access'])
    return {'Open':authorized}

@app.route('/register', methods=['POST'])
def register():
    pass

