from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "login_and_registration"
    # db should = your schema

    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe_created = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (f_name, l_name, email, password) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        return cls(results[0])

    @ staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(
            "login_and_registration").query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['f_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['l_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['con_pass']:
            flash("Passwords don't match", "register")
        return is_valid

    # @classmethod
    # def get_user_by_email(cls, data):
    #     query = "SELECT * from users LEFT JOIN recipes ON users.id = recipes.users_id WHERE users.email = %(email)s"
    #     results = connectToMySQL(
    #         "login_and_registration").query_db(query, data)
    #     this_user_recipe = cls(results[0])
    #     for row in results:
    #         recipe_data = {
    #             "id": row['recipes.id'],
    #             "name": row['recipes.name'],
    #             "under_thirty": row["recipes.under_thirty"],
    #             "instructions": row["recipes.instructions"],
    #             "date_made": row["recipes.date_made"],
    #             "created_at": row["burgers.created_at"],
    #             "updated_at": row["burgers.updated_at"]
    #         }
    #         this_user_recipe.recipes.append(Recipe(recipe_data))
    #     return this_user_recipe
