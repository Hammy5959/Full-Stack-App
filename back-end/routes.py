from app import app, db
from flask import request, jsonify
from models import User


@app.route("/api/signup", methods=["GET"])
def signup():
    users = User.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result)


@app.route("/api/signup", methods=["POST"])
def signupPost():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Username already exists!"}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"message": "Invalid email or password!"}), 401

    return jsonify({"message": "Login Successfully!"}), 201


@app.route("/api/delete", methods=["DELETE"])
def delete():
    records = User.query.order_by(User.id).limit(5).all()

    if not records:
        return jsonify({"message": "No record found!"}), 401
    for record in records:
        db.session.delete(record)

        db.session.commit()
        return jsonify({"message": "Users deleted successfully!"}), 201
