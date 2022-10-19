from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash  


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "test": generate_password_hash("pass"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/', methods = ['GET'])
def get_file():
    return {'data': 'get'}
  

@app.route('/', methods = ['POST'])
@auth.login_required
def upload_file():
    return {'data': 'post'}


@app.route('/', methods = ['DELETE'])
def delete_file():
    return {'data': 'DELETE'}
  
  
if __name__ == '__main__':
    app.run(debug=True)
