from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.message import Message 

@app.route("/create-message", methods=['POST'])
def create_message():
    if not Message.validate_message(request.form):
        return redirect("/wall")

    Message.create_message(request.form)

    return redirect("/wall")

@app.route("/delete-message", methods=['POST'])
def delete_message():
    print(request.form)
    Message.delete(request.form)


    return redirect("/wall")
