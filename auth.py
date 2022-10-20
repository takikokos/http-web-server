from flask_httpauth import HTTPBasicAuth
from sqlalchemy import select
from werkzeug.security import check_password_hash

from models import User
from app import db


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login, password):
    users = db.session.execute(select(User).where(User.login == login)).first()
    if users and check_password_hash(users[0].password, password):
        return users[0]
    return False
