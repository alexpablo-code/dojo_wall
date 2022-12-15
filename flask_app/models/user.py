from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.t_-]+@[a-zA_Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

class User:
    DB = "dojo_wall"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.messages = []


    @classmethod 
    def register_user(cls, user_data):
        data = {
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": bcrypt.generate_password_hash(user_data['password'])
        }
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW());
                """

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def one_user(cls, user_id):
        data = {
            "id": user_id
        }
        query = """
                SELECT * FROM users 
                WHERE id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)

        return cls(results[0])
    
    
    
    
    @classmethod
    def select_by_email(cls,email):
        data ={
            "email": email
        }

        query = """
                SELECT * FROM users 
                WHERE email = %(email)s;
                """

        results = connectToMySQL(cls.DB).query_db(query,data)

        if not results:
            return False

        return cls(results[0])


    @staticmethod
    def validate_user(user_data):
        is_valid = True 
        user_in_db = User.select_by_email(user_data['email'])

        if len(user_data['first_name']) <= 2 or user_data['first_name'].isalpha() is False:
            flash("First name must be at least 2 characters long.", "register")
            is_valid = False

        if not user_data['last_name'].isalpha() or len(user_data['last_name']) <=2:
            flash("Last name must be at least 2 characters long.", "register")
            is_valid = False

        if not user_data['email'] or EMAIL_REGEX.match(user_data['email']) is False:
            flash("Invalid email address", "register")
            is_valid = False

        if user_in_db:
            flash("User already exists", "register")
            is_valid = False

        if len(user_data['password']) < 8 or len(user_data['confirm_password']) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid = False

        elif not user_data['password'] == user_data['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user_data):
        is_valid = True
        user_in_db = User.select_by_email(user_data['email'])

        if not user_data['email'] or user_data['password'] is False:
            flash("Email/password required", "login")
            is_valid = False

        elif not user_in_db:
            flash("Invalid email/password", "login")
            is_valid = False

        elif not bcrypt.check_password_hash(user_in_db.password, user_data['password']):
            flash("Invalid email/password", "login")
            is_valid = False

        if is_valid:
            return user_in_db

        return is_valid
