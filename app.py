from flask import Flask, jsonify, request, url_for 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku 
import os 

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(500))
    short_bio = db.Column(db.String(500))

    def __init__(self, name, image, short_bio):
        self.name = name
        self.image = image
        self.short_bio = short_bio

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "image","short_bio")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/") #homepage
def greeting():
    return "<h1>Social app API</h1>" 

@app.route("/users",methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/user/<id>",methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route("/add-user" , methods=["POST"])
def add_user():
    name = request.json["name"]
    image = request.json["image"]
    short_bio = request.json["short_bio"]

    new_user = User(name, image, short_bio)

    db.session.add(new_user)
    db.session.commit()

    return jsonify("USER CREATED")

@app.route("/user/<id>", methods=["DELETE"])  
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify("USER DELETED")


@app.route("/user/<id>", methods=["PUT"])  
def update_user(id):
    user = User.query.get(id)
    
    new_name = request.json["name"]
    new_short_bio = request.json["short_bio"]

    user.name = new_name
    user.short_bio = new_short_bio

    db.session.commit()

    return user_schema.jsonify(user)


if __name__ =="__main__":
    app.debug = True
    app.run()