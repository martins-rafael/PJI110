import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    rg = db.Column(db.String)
    cpf = db.Column(db.String)
    address = db.Column(db.String)
    birth = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, email, password, rg=None, cpf=None, address=None, birth=None, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.rg = rg
        self.cpf = cpf
        self.address = address
        self.birth = birth
        self.is_admin = is_admin


def init_defaults():
    if Member.query.first() is None:
        member = Member(name='admin', email='admin@email.com',
                        password=generate_password_hash('admin'), is_admin=True)
        db.session.add(member)
        db.session.commit()

    pass
