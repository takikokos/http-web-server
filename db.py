from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    login = Column(String(30))
    password = Column(String)

    files = relationship(
        "File", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User({self.id=}, {self.login=}, {self.password=})"


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="files")

    def __repr__(self):
        return f"File({self.id=}, {self.hash=}, {self.user_id=})"


if __name__ == "__main__":
    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session


    engine = create_engine("sqlite:///sqlite.db", echo=True, future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        test_user = User(
            login="Test",
            password="123",
            files=[
                File(name="123", hash="123hash"),
                File(name="456", hash="456hash")
            ],
        )
        session.add(test_user)
        session.commit()

    with Session(engine) as session:
        stmt = select(User).where(User.login == "Test")
        for user in session.scalars(stmt):
            print(user, user.files)
