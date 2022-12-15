from flask_app import app 
from flask import render_template, redirect, request, session
from flask_app.models.comment import Comment


@app.route("/create-comment", methods=['POST'])
def create_comment():
    if "user_id" not in session:
        return redirect("/")

    print(request.form)

    Comment.create_comment(request.form)

    return redirect("/wall")