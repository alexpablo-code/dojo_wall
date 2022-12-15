from flask_app import app 
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.comment import Comment

@app.route("/")
def login_page():
    if "user_id" in session:
        return redirect("/wall")
    return render_template("login.html") 

@app.route("/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")

    user= User.register_user(request.form)
    print("___USER IN REGIST___", user)

    session['user_id'] = user

    return redirect("/wall")


@app.route("/login", methods=['POST'])
def login():
    user = User.validate_login(request.form)
    if not user:
        return redirect("/")

    session['user_id'] = user.id

    return redirect("wall")

    

@app.route("/wall")
def wall():
    if not "user_id" in session:
        return redirect("/")

    user = User.one_user(session["user_id"])
    all_messages = Message.messages_users_comments()

    return render_template("wall.html", user=user, all_messages=all_messages)


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")
