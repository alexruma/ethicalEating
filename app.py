import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dictionary_parser import *
from user_handler import *

app = Flask(__name__)

app.secret_key = "secret_key_string"


# Render homepage/index
@app.route('/')
def index():
    return render_template('index.html')


# Render recipe-search
@app.route('/recipe_search', methods=["GET", "POST"])
def recipe_search():
    return render_template('recipe_search.html')


# Render recipe-search results
@app.route('/recipe_search_results', methods=["GET", "POST"])
def show_results():
    search_val = request.form["search-val"]
    result_dict = gather_meals_by_search(search_val)

    return render_template('recipes.html', category="Relevant", data=result_dict)


@app.route('/lucky', methods=["GET", "POST"])
def random_recipe():
    recipe_dict = gather_meals()
    random_key = random.choice(list(recipe_dict.items()))
    display_name = random_key[1]
    ingredients_dict = gather_ingredients_by_meal(random_key[0])

    return render_template('ingredients.html', meal_key=random_key[0], recipe_name=display_name, data=ingredients_dict)


# Render create-recipe
@app.route('/create_recipe', methods=["GET", "POST"])
def create_recipe():
    full_ingredient_list = gather_full_ingredient_list()

    return render_template('create_recipe.html', data=full_ingredient_list)


# new_recipe function from create_recipe page which renders ingredient list page
@app.route("/new_recipe", methods=["POST"])
def new_recipe():
    recipe_name = request.form["recipe_name"]
    ingredient_list = request.form.getlist('checkbox')
    ingredients_dict = {}

    # create a key in case user saves it
    if session['logged_in']:
        meal_key = recipe_name.replace(" ", "") + "." + session["username"]
    else:
        meal_key = recipe_name.replace(" ", "") + ".guest"

    for key in ingredient_list:
        ingredients_dict.update(gather_ingredient_by_key(key))

    return render_template('ingredients.html', meal_key=meal_key, recipe_name=recipe_name, data=ingredients_dict)


# Handle POST request from selecting meal on index page. Will redirect to appropriate recipe list page.
@app.route("/recipe_list", methods=["POST"])
def recipe_list():
    meal_category = request.form['submit']
    print(meal_category)

    return redirect(url_for("recipes", meal_category=meal_category))


# Render list_of_recipes
@app.route("/<meal_category>/", methods=["GET", "POST"])
def recipes(meal_category):
    meal_dict = gather_meals_by_category(meal_category)
    print(meal_dict)

    return render_template('recipes.html', category=meal_category, data=meal_dict)


@app.route("/recipe_ingredients", methods=["GET"])
def recipe_ingredients():
    key = request.args['meal']
    recipe_name = request.args['name']
    ingredients = gather_ingredients_by_meal(key)

    return render_template('ingredients.html', meal_key=key, recipe_name=recipe_name, data=ingredients)


@app.route("/custom_recipe_ingredients", methods=["GET"])
def custom_recipe_ingredients():
    key = request.args['meal']
    recipe_name = request.args['name']
    ingredients = load_custom_recipe_ingredients(session["username"], key)

    return render_template('ingredients.html', meal_key=key, recipe_name=recipe_name, data=ingredients)


@app.route("/display_info", methods=["POST"])
def display_info():
    ingredient_key = request.form['ingredient_key']
    info_type = request.form['info_type']
    ingredient_name = gather_ingredient_by_key(ingredient_key)[ingredient_key]

    # Work if requesting ethical issues.
    if info_type == "1":
        issues_list = gather_ingredient_issues_by_key(ingredient_key)
        issue_display_list = []

        # Append the display text of each issue with a value of 1 into issue_display_list.
        for issue in issues_list:
            if issue["value"] == 1:
                issue_display_list.append(issue["text"])

        print(issue_display_list)

        return jsonify('', render_template('display_info.html', display_info=issue_display_list,
                                           headline="Possible Ethical Issues for " + ingredient_name))

    # Work if requesting alternatives.
    else:
        alternatives_list = gather_ingredient_alternatives_by_key(ingredient_key)

        return jsonify('', render_template('display_info.html', display_info=alternatives_list,
                                           headline="Possible Alternative Ingredients for " + ingredient_name))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if request.form['submit_button'] == 'create':
        return redirect(url_for("create_user", username=username, password=password))

    if user_authentication(username, password):
        session.permanent = True
        session['logged_in'] = True
        session["username"] = username
        session["saved_recipes"] = load_saved_recipes(username)
        session["custom_saved_recipes"] = load_custom_saved_recipes(username)

        # Create a unified dictionary list
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])
        print("Session created")

        return redirect(request.referrer)

    # Add in an error message that username or password was incorrect

    return redirect(request.referrer)


@app.route('/create', methods=["GET", "POST"])
def create_user():
    username = request.args.get("username")
    password = request.args.get("password")

    print("In Create User")
    print(username)
    print(password)

    if not username_exists(username):
        create_new_user(username, password)
        session.permanent = True
        session['logged_in'] = True
        session["username"] = username
        session["saved_recipes"] = load_saved_recipes(username)
        session["custom_saved_recipes"] = load_custom_saved_recipes(username)

        # Create a unified dictionary list
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])
        print("Session created")

        return redirect(request.referrer)

    # Add in error message that will appear if username already exists

    return redirect(request.referrer)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove everything from the session token, then reload index with the login & create user buttons again
    session.permanent = False
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(request.referrer)


@app.route('/save_recipe', methods=['GET', 'POST'])
def save_recipe():
    key = request.form['meal_key']
    recipe_name = request.form['meal']
    username = session["username"]

    if recipe_exists(key):
        save_user_recipe(username, key, recipe_name)
        session["saved_recipes"] = load_saved_recipes(username)

        # Create a unified dictionary list of recipes
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])

        return redirect(request.referrer)

    else:
        ingredients = request.form['ingredients']
        save_user_custom_recipe(username, key, recipe_name, ingredients)
        session["custom_saved_recipes"] = load_custom_saved_recipes(username)

        # Create a unified dictionary list of recipes
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])
        ingredients = load_custom_recipe_ingredients(session["username"], key)

        return render_template('ingredients.html', meal_key=key, recipe_name=recipe_name, data=ingredients)


@app.route('/unsave_recipe', methods=['GET', 'POST'])
def unsave_recipe():
    key = request.form['meal_key']
    name = request.form['meal']
    username = session["username"]

    if recipe_exists(key):
        remove_recipe(username, key)
        session["saved_recipes"] = load_saved_recipes(username)

        # Create a unified dictionary list of recipes
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])

        return redirect(request.referrer)

    else:
        ingredients = load_custom_recipe_ingredients(session["username"], key)

        remove_custom_recipe(username, key)
        session["custom_saved_recipes"] = load_custom_saved_recipes(username)

        # Create a unified dictionary list of recipes
        session["recipes"] = {}
        session["recipes"].update(session["saved_recipes"])
        session["recipes"].update(session["custom_saved_recipes"])

        return render_template('ingredients.html', meal_key=key, recipe_name=name, data=ingredients)


@app.route('/saved_recipes', methods=['GET', 'POST'])
def saved_recipes():
    return render_template('saved_recipes.html')


if __name__ == "__main__":
    app.run(debug=True)
