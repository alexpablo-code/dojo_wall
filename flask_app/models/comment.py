from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, message 
from flask_app import app 
from flask import flash, session

class Comment:
    DB = "dojo_wall"

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.post = None 


    @classmethod
    def create_comment(cls, comment_data):
        data = {
            "comment": comment_data['comment'],
            "user_id": session['user_id'],
            "message_id": comment_data['message_id']
        }

        query = """
                INSERT INTO comments (comment, user_id, message_id, created_at, updated_at)
                VALUES (%(comment)s,%(user_id)s,%(message_id)s, NOW(), NOW());
                """

        return connectToMySQL(cls.DB).query_db(query,data)


    @classmethod
    def all_comments(cls):
        query = """
                SELECT * FROM comments
                JOIN users
                ON comments.user_id = users.id
                ORDER BY comments.created_at;
                """

        results = connectToMySQL(cls.DB).query_db(query)

        all_comments = []

        for row in results:
            comment = cls(row)

            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            comment.creator = user.User(user_data)

            all_comments.append(comment)

        return all_comments


    # @classmethod
    # def comments_of_message(cls, message_id):
    #     data = {
    #         "message_id": message_id
    #     }

    #     query = """
    #             SELECT * FROM comments
    #             JOIN users
    #             ON comments.user_id = users.id
    #             WHERE comments.message_id = %(message_id)s;
    #             """

    #     results = connectToMySQL(cls.DB).query_db(query)

    #     for row in results:

    #         comment = cls(row)

    #         data = {
    #             ""
    #         }

