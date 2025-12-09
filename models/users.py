from db import db


class Users(db.Model):
    __tablename__ = "__users__"

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)
    role=db.Column(db.Enum('Admin','Student','Head'), nullable=False)