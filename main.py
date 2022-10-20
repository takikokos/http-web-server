from hashlib import sha256
from pathlib import Path

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash # use Flask-Bcrypt?


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path('store')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 Mb

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
    if 'file' not in request.files:
        return "No file part in post request", 400
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    filename_hash = sha256(file.filename.encode()).hexdigest()
    filename = app.config['UPLOAD_FOLDER'] / filename_hash[:2] / filename_hash
    filename.parent.mkdir(parents=True, exist_ok=True)
    file.save(filename)

    return filename_hash


@app.route('/', methods = ['DELETE'])
def delete_file():
    return {'data': 'DELETE'}


if __name__ == '__main__':
    app.run(debug=True)
