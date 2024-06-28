import os
from flask import jsonify, request, current_app, Flask
from functools import wraps
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)
app.config.from_object(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    pfp = db.Column(db.LargeBinary, nullable=True)
    desc = db.Column(db.Text, nullable=True)
    writings = db.relationship('Writing', backref="creator", lazy=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, 
                    username=self.username,
                    email=self.email)

class Writing(db.Model):
    __tablename__ = "writings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    text=self.text)

CORS(app, resources={r'/*': {'origins': '*'}})

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

@app.route('/', methods=['GET'])
def home():
    writings = Writing.query.all()
    auth = False
    return jsonify({"writings": writings, "user_info": auth}), 201

@app.route('/search/<text>', methods=["GET"])
def search(text):
    writings = Writing.query.all()
    users = User.query.all()
    searchedWritings = []
    searchedUsers = []
    for writing in writings:
        if text.lower() in writing["title"].lower():
            searchedWritings += writing
    for user in users:
        if text.lower() in user["username"].lower():
            searchedUsers += user
    return jsonify({"writings": searchedWritings, "users": searchedUsers}), 201

@app.route('/users/<username>', methods=["GET", "POST"])
def profile(username):
    if request.method == "GET":
        user = db.one_or_404(db.select(User).filter_by(username=username))
        return jsonify(user)
    else:
        user = User.query.filter_by(username=username).first()
        data = request.get_json()
        setattr(user, 'pfp', data["pfp"])
        setattr(user, 'desc', data["desc"])
        db.session.commit()

@app.route('/users/<username>/<id>', methods=["GET", "POST"])
def writing(username, id):
    if request.method == "GET":
        user = db.one_or_404(db.select(User).filter_by(username=username))
        try:
            writing = db.one_or_404(db.select(Writing).filter_by(
                creator_id=user.id,
                id=id,
            ))
            return jsonify(writing)
        except:
            return jsonify("No such user found")
    else:
        writing = Writing.query.filter_by(id=id).first()
        data = request.get_json()
        setattr(writing, 'title', data['title'])
        setattr(writing, 'text', data['text'])
        db.session.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user.email,
        'iat':datetime.now(),
        'exp': datetime.now() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('UTF-8') })

@app.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    writing = Writing(title=data['title'], text=data['text'])
    db.session.add(writing)
    db.session.commit()
    return jsonify(writing.to_dict()), 201

if __name__ == '__main__':
    app.run()