from chalice import Chalice
from chalicelib import Database, CURRENT_ENV

app = Chalice(app_name='SecureBox')
app.debug = True

Database = {'1010': '123-456', '1234': '456-789', '2244': '888-777'} # box_id, tracking_id

@app.route('/', methods=['POST'])
def authenticate():
    request = app.current_request.json_body
    try:
        exists = request['tracking_id'] == Database[request['box_id']]
        if (exists):
            return {'value': 'success'}
        else:
            return {'value': 'failure'}
    except KeyError:
        return {'value': False}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
