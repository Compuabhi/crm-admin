from index import db, bcrypt
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None


class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(50))
    created_at = db.Column(db.Integer())
    updated_at = db.Column(db.Integer())
    order_id = db.Column(db.Integer())
    plan_id = db.Column(db.Integer())
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    bmi = db.Column(db.String(50))
    goal = db.Column(db.String(50))
    address = db.Column(db.String(50))
    company = db.Column(db.String(50))
    sex = db.Column(db.String(50))
    hometown = db.Column(db.String(50))
    pref_language = db.Column(db.String(50))
    account_id = db.Column(db.Integer())


    @staticmethod
    def get_member_with_email(email):
        member = Member.query.filter_by(email=email).first()
        if member :
            return member
        else:
            return None

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Prospect(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(50))
    created_at = db.Column(db.Integer())
    updated_at = db.Column(db.Integer())
    goal = db.Column(db.String(50))
    address = db.Column(db.String(50))
    company = db.Column(db.String(50))
    sex = db.Column(db.String(50))
    hometown = db.Column(db.String(50))
    pref_language = db.Column(db.String(50))

class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __init__(self, email, password, name, phone):
        self.email = email
        self.password = Account.hashed_password(password)
        self.name = name
        self.phone = phone
        

    @staticmethod
    def hashed_password(password):
        print('**************')
        return bcrypt.generate_password_hash(password)





class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)