from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash  # use Flask-Bcrypt for passwordss?

from app import db


class User(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=False)

    files = relationship(
        "File", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User({self.id=}, {self.login=}, {self.password=})"


class File(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    origin_name = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="files")

    def __repr__(self):
        return f"File({self.id=}, {self.hash=}, {self.user_id=})"


if __name__ == "__main__":
    from sqlalchemy.orm import Session
    from app import app

    with app.app_context():
        db.create_all()

        with Session(db.engine) as session:
            test_user_1 = User(
                login="test",
                password=generate_password_hash("pass"),

            )
            test_user_2 = User(
                login="user",
                password=generate_password_hash("pass"),

            )
            session.add_all([test_user_1, test_user_2])
            session.commit()
