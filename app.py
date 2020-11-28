import random
from flask import Flask, render_template, request, redirect, url_for, session
from dictionary_parser import gather_full_ingredient_list, gather_ingredient_by_key, gather_meals_by_search, \
    gather_meals_by_category, gather_ingredients_by_meal, gather_meals
from user_handler import user_authentication, username_exists, create_new_user

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
    # Dictionary of recipe names
    recipe_dict = gather_meals()
    # Random key/value from meals.json
    random_key = random.choice(list(recipe_dict.items()))
    # Display name from random_key
    display_name = random_key[1]
    # Entry's list of ingredients via gather_ingredients_by_meal, which uses the key value
    ingredients_dict = gather_ingredients_by_meal(random_key[0])

    return render_template('ingredients.html', recipe_name=display_name, data=ingredients_dict)


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

    for key in ingredient_list:
        ingredients_dict.update(gather_ingredient_by_key(key))

    return render_template('ingredients.html', recipe_name=recipe_name, data=ingredients_dict)


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

    return render_template('ingredients.html', recipe_name=recipe_name, data=ingredients)


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
        print("Session created")

        return redirect(url_for('index', session=session))

    # Add in an error message that username or password was incorrect

    return redirect(url_for('index'))


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
        print("Session created")

        return redirect(url_for('index', session=session))

    # Add in error message that will appear if username already exists

    return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove everything from the session token, then reload index with the login & create user buttons again
    session.permanent = False
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/save_recipe', methods=['GET', 'POST'])
def save_recipe():
    # Need to call a function to save the recipe name variable to the user.json file. If the request is from a generated
    # recipe we will need to add name & ingredients. Not sure how we'll be able to differentiate at this point

    return redirect(url_for('index'))


@app.route('/saved_recipes', methods=['GET', 'POST'])
def saved_recipes():
    # Need a function that parses the user.json for all recipe names and loads a page. Once again will need to think
    # about how we are then loading the ingredients for custom recipes.

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
