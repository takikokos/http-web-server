from hashlib import sha256
from pathlib import Path

from flask import request, send_from_directory
from werkzeug.security import safe_join

from app import app
from auth import auth


@app.route('/<filename>', methods = ['GET'])
def get_file(filename):
    folder = safe_join(app.config["UPLOAD_FOLDER"], filename[:2])
    return send_from_directory(folder, filename)


@app.route('/', methods = ['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return "No file part in post request", 400
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    filename_hash = sha256(file.filename.encode()).hexdigest()
    # we use hash instead of origin filename so 
    # we can safely join the full path + no need to validate the extension
    filename = app.config['UPLOAD_FOLDER'] / filename_hash[:2] / filename_hash
    filename.parent.mkdir(parents=True, exist_ok=True)
    file.save(filename)

    return filename_hash, 201


@app.route('/<filename>', methods = ['DELETE'])
@auth.login_required
def delete_file(filename):
    filepath = safe_join(app.config["UPLOAD_FOLDER"], filename[:2], filename)

    if not filepath:
        return 'Incorrect filename', 400
    filepath = Path(filepath)

    if not filepath.exists() or not filepath.is_file():
        return 'File not found', 404

    filepath.unlink()
    return 'Deleted', 200
