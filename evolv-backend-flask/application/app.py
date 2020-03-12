from flask import request, render_template, jsonify, url_for, redirect, g, json
from .models import User, Member, Account, AlchemyEncoder
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token


@app.route('/', methods=['GET'])
def index():
    # return render_template('index.html')
    temp = '''
        <html>
            <head>
                <title>Home Page - Microblog</title>
            </head>
            <body>
                <h1>Hello, ''' +  '''!</h1>
            </body>
        </html>'''
    return temp


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    print('testass')
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@app.route("/crm/api/v1.0/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    print('*****')
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )




# Member Resource Apis
@app.route("/crm/api/v1.0/account/<int:account_id>/member", methods=["POST"])
def create_member(account_id):
    incoming = request.get_json()
    try:
        member = Member(
            email = incoming["email"],
            name=incoming["name"],
            phone=incoming["phone"],
            date_of_birth=incoming["date_of_birth"],
            height=incoming["height"],
            weight=incoming["weight"],
            bmi=incoming["bmi"],
            goal=incoming["goal"],
            address=incoming["address"],
            company=incoming["company"],
            sex=incoming["sex"],
            hometown=incoming["hometown"],
            pref_language=incoming["pref_language"],
            account_id=account_id
        )
        print('*****')
        db.session.add(member)
        try:
            db.session.commit()

            new_member = Member.query.filter_by(email=incoming["email"]).first()

            return jsonify(
                id=new_member.id
            )
        except IntegrityError:
            return jsonify(message="User with that email already exists"), 409

    except Exception as e:
        print(str(e))
        return jsonify(token_is_valid=False), 400


@app.route("/crm/api/v1.0/accounts/<int:account_id>/members", methods=["GET"])
def list_members(account_id):
    try:

        members = Member.query.filter_by(account_id=account_id).all()
        for m in members:
            print(m.email)
        
        ser_members = []
        for m in members:
            ser_members.append(m.as_dict())
        
        return jsonify(
            ser_members
        )
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 400

@app.route("/crm/api/v1.0/accounts/<int:account_id>/members/<int:member_id>", methods=["GET"])
def get_member(account_id, member_id):
    try:
        db.session.commit()

        member = Member.query.filter_by(account_id=account_id, id=member_id).first()

        return jsonify(
            member=member.as_dict()
        )

    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 400


@app.route("/crm/api/v1.0/accounts/<int:account_id>/members/<int:member_id>", methods=["PUT"])
def update_member(account_id, member_id):
    try:
        db.session.commit()

        members = Member.query.filter_by(account_id=account_id, id=member_id).first()

        return jsonify(
            members=members
        )
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409


# Account Apis

@app.route("/crm/api/v1.0/accounts", methods=["POST"])
def create_account():
    incoming = request.get_json()
    print(incoming)
    try:
        account = Account(
            email =incoming["email"],
            name= incoming["name"],
            phone= incoming["phone"],
            password=incoming["password"],
        )
        
        db.session.add(account)
        try:
            db.session.commit()

            new_account = Account.query.filter_by(email=incoming["email"]).first()

            return jsonify(
                id=new_account.id
            )
        except IntegrityError:
            return jsonify(message="Account with that email already exists"), 409

    except Exception as e:
        print(e)
        return jsonify(token_is_valid=False), 400

@app.route("/crm/api/v1.0/accounts/<string:account_id>", methods=["PUT"])
def update_account():
    pass

@app.route("/crm/api/v1.0/accounts/<string:account_id>", methods=["GET"])
def get_account(account_id):
    pass

@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403










