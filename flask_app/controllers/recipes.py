from flask import render_template, redirect, request, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.controllers.users import User
from flask_app.models.recipe import Recipe

from flask import flash
bcrypt = Bcrypt(app)


@app.route('/recipes/create', methods=['POST'])
def recipes_create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new_recipe')
    data = {
        "users_id": session["user_id"],
        "names": request.form['names'],
        "descriptions": request.form['descriptions'],
        "instructions": request.form['instructions'],
        "under_thirty": int(request.form['under_thirty']),
        "date_made": request.form['date_made'],
    }
    Recipe.create(data)
    return redirect("/dashboard")


@app.route('/new_recipe')
def new_recipe_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }
    user = User.get_one(data)
    recipe = Recipe.get_all(data)
    return render_template("new_recipes.html", user=user, recipe=recipe)


@ app.route("/recipes_edit/<int:num>")
def edit_recipe(num):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": num
    }
    this_recipes = Recipe.get_one(data)
    return render_template("edit_recipes.html", recipe=this_recipes)


@ app.route("/recipes/update", methods=["POST"])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes_edit')
    data = {
        "names": request.form['names'],
        "descriptions": request.form['descriptions'],
        "instructions": request.form['instructions'],
        "under_thirty": int(request.form['under_thirty']),
        "date_made": request.form['date_made'],
    }
    Recipe.update(data)
    return redirect("/dashboard")


@ app.route("/recipes_show/<int:num>")
def show_recipe(num):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": num
    }
    user_data = {
        "id": session['user_id']
    }
    recipes = Recipe.get_one(data)
    user = user_data
    return render_template("show_recipes.html", recipe=recipes, user=user)


@ app.route("/recipes_delete/<int:num>")
def delete_recipe(num):
    data = {
        "id": num
    }
    Recipe.delete(data)
    return redirect("/dashboard")
