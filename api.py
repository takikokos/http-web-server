from hashlib import sha256
from pathlib import Path

from flask import request, send_from_directory
from sqlalchemy import select
from werkzeug.security import safe_join

from app import app, db
from auth import auth
from models import File


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

    if filename.exists():
        return 'File with such name already exists', 400

    filename.parent.mkdir(parents=True, exist_ok=True)
    file.save(filename)
    
    db_file = File(
        origin_name=file.filename,
        hash=filename_hash,
        user_id=auth.current_user().id
    )
    db.session.add(db_file)
    db.session.commit()

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

    db_file = db.session.execute(select(File).where(File.hash == filepath.name)).first()[0]
    if db_file.user_id != auth.current_user().id:
        return "Forbidden", 403

    filepath.unlink()
    db.session.delete(db_file)
    db.session.commit()

    return 'Deleted', 200
