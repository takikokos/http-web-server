from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path('store')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 Mb
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"

db.init_app(app)
