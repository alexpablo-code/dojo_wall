from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import comment
from flask_app import app
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.t_-]+@[a-zA_Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)


class Message:
    DB = "dojo_wall"

    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

        self.comments = []

    @classmethod
    def create_message(cls, message_data):
        data = {
            "message": message_data['message'],
            "user_id": session['user_id']
        }

        query = """
                INSERT INTO messages (message,  user_id, created_at, updated_at)
                VALUES (%(message)s,%(user_id)s, NOW(), NOW());
                """
        return connectToMySQL(cls.DB).query_db(query,data)
        

    @classmethod
    def get_all_messages(cls):
        query = """
                SELECT * FROM messages 
                JOIN users
                ON messages.user_id = users.id
                ORDER BY  messages.created_at DESC;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        all_messages = []

        for row in results:

            message = cls(row)

            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            message.creator = user.User(user_data)

            all_messages.append(message)

        return all_messages


    @classmethod
    def messages_users_comments(cls):
        query = """
                SELECT * FROM messages 
                JOIN users
                ON messages.user_id = users.id
                ORDER BY  messages.created_at DESC;
                """

        results = connectToMySQL(cls.DB).query_db(query)
        all_messages = []

        for row in results:
            message = cls(row)

            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            message.creator = user.User(user_data)

            # We are now getting all the comments that are associatied with each message with each user that creatd them 
            comment_data ={
                "message_id": row['id']
            }
            comment_query = """
                            SELECT * FROM comments
                            JOIN users
                            ON comments.user_id = users.id
                            WHERE comments.message_id = %(message_id)s 
                            ORDER BY comments.created_at DESC;
                            """
            comment_results = connectToMySQL(cls.DB).query_db(comment_query, comment_data)

            for comment_row in comment_results:
                comment_of_msg = comment.Comment(comment_row)

                comment_creator_data= {
                    "id": comment_row['users.id'],
                    "first_name": comment_row['first_name'],
                    "last_name": comment_row['last_name'],
                    "email": comment_row['email'],
                    "password": comment_row['password'],
                    "created_at": comment_row['users.created_at'],
                    "updated_at": comment_row['users.updated_at']
                }

                comment_of_msg.creator = user.User(comment_creator_data)

                message.comments.append(comment_of_msg)

            all_messages.append(message)

        return all_messages


    @classmethod 
    def delete(cls, message_data):
        data = {
            "id": message_data['id']
        }
        query = """
                DELETE FROM messages
                WHERE id = %(id)s;
                """

        return connectToMySQL(cls.DB).query_db(query,data)


    @staticmethod
    def validate_message(message_data):
        is_valid = True

        if not message_data['message']:
            flash("Post content must not be blank", "messages")
            is_valid = False

        return is_valid

