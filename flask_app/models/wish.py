from re import U
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

db = "wish_schema"

class Wish:
    def __init__( self , data ):
        self.id = data['id']
        self.wish = data['wish']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.wisher_first_name = data['first_name']
        self.wisher_last_name = data['last_name']

        self.users = []
        self.likes = 0

    @classmethod
    def save_wish(cls,data):
        query = """
        INSERT INTO wishes (wish, description, user_id)
        VALUES (%(wish)s, %(description)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_wish(cls, data):
        query = """
        UPDATE wishes
        SET wish=%(wish)s, description=%(description)s
        WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one_wish(cls,data):
        query = """
        SELECT * FROM wishes
        WHERE id = %(id)s;"""
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return results[0]
        # run into a KeyError if I return (cls(results[0]))

    @classmethod
    def get_all_wishes(cls):
        query = """
        SELECT * FROM wishes
        JOIN users ON users.id = wishes.user_id;"""
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_all_wishes_by_one_poster(cls, data):
        query = """
        SELECT * FROM wishes
        LEFT JOIN users ON users.id = wishes.user_id
        WHERE wishes.user_id = %(user_id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        all_wishes = []
        for wish in results:
            all_wishes.append(cls(wish))
        return all_wishes

    @classmethod
    def destroy_wish(cls,data):
        query = "DELETE FROM wishes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_wish(wish):
        is_valid = True
        if len(wish['wish']) < 1:
            is_valid = False
            flash("Please make a wish.","wish")
        if len(wish['description']) < 1:
            is_valid = False
            flash("Please enter a description.","wish")
        return is_valid

    @classmethod
    def non_granted_wishes(cls,data):
        query = """
        SELECT * FROM users
        WHERE users.id NOT IN ( SELECT user_id FROM likes
        WHERE wish_id = %(id)s );"""
        users = []
        results = connectToMySQL(db).query_db(query,data)
        for row in results:
            users.append(row)
        return users

    @classmethod
    def grant_wish(cls,data):
        query = "INSERT INTO likes (user_id, wish_id) VALUES (%(user_id)s, %(wish_id)s);"
        return connectToMySQL(db).query_db(query,data);

    # @classmethod
    # def get_all_wishes_and_likes(cls):
    #     query = """
    #     SELECT * FROM wishes;"""
    #     # JOIN users ON users.id = user_has_wishes.user_id
    #     # LEFT JOIN user_has_wishes ON wishes.id = user_has_wishes.wish_id;"""
    #     results = connectToMySQL(db).query_db(query)
    #     wishes = []
    #     for wish in results:
    #         current_wish = {
    #             'id' : wish['id'],
    #             'wish' : wish['wish'],
    #             'description' : wish['description'],
    #             'created_at' : wish['created_at'],
    #             'updated_at' : wish['updated_at'],
    #             'user_id' : wish['user_id'],
    #         }
    #         if len(wishes) == 0:
    #             wishes.append(cls(current_wish))
    #         else:
    #             last_wish = wishes[len(wishes)-1]
    #             if last_wish.id != current_wish['id']:
    #                 wishes.append(cls(current_wish))
    #         last_wish = wishes[len(wishes)-1]
    #         last_wish.likes+=1
    #     return wishes

    # @classmethod
    # def like_wish(cls, data):
    #     query = """
    #     INSERT INTO likes (user_id, wish_id)
    #     VALUES (%(user_id)s, %(wish_id)s);"""
    #     return connectToMySQL(db).query_db(query,data)

