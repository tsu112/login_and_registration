from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    db = "login_and_registration"
    # db should = your schema

    def __init__(self, data):
        self.id = data['id']
        self.names = data['names']
        self.descriptions = data['descriptions']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (names, descriptions, instructions, under_thirty, users_id) VALUES (%(names)s, %(descriptions)s, %(instructions)s, %(under_thirty)s, %(users_id)s)"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM recipes WHERE users_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        list = []
        for row in results:
            list.append(cls(row))
        return list

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        this_recipe = cls(results[0])
        return this_recipe

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET names= %(names)s, descriptions= %(descriptions)s, instructions= %(instructions)s, instructions= %(instructions)s, under_thirty= %(under_thirty)s, date_made= %(date_made)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET (names, descriptions, instructions, under_thirty) VALUES (%(names)s, %(descriptions)s, %(instructions)s, %(under_thirty)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @ staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['names']) < 3:
            flash("Name has to be 3 characters long!", "recipe")
            is_valid = False
        if len(recipe['descriptions']) < 3:
            flash("Description has to be 3 characters long!", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions has to be 3 characters long!", "recipe")
            is_valid = False
        if len(recipe['date_made']) == "":
            flash("Must enter date", "recipe")
            is_valid = False

        return is_valid
