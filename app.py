from flask import Flask, render_template, request, redirect, url_for
from dictionary_parser import gather_full_ingredient_list, gather_ingredient_by_key, gather_meals_by_search, gather_meals_by_category,  gather_ingredients_by_meal

app = Flask(__name__)

# Render homepage/index
@app.route('/')
def index():
    return render_template('index.html')

# Render recipe-search
@app.route('/test-search', methods=["GET", "POST"])
def recipe_search():
    return render_template('recipe_search.html')

# Render recipe-search results
@app.route('/recipe_search_results', methods=["GET", "POST"])
def show_results():
    search_val = request.form["search-val"]
    result_dict = gather_meals_by_search(search_val)
    
    return render_template('recipes.html', category="Relevant", data=result_dict)

# Render lucky
@app.route('/lucky', methods = ["GET", "POST"])
def random():
    # Dictionary of recipe names
    recipe_dict = gather_meals()
    # Random key/value from meals.json
    random_key = random.choice(list(recipe_dict.items()))
    # Display name from random_key
    display_name = random_key[1]
    # Entry's list of ingredients via gather_ingredients_by_meal, which uses the key value
    ingredients_dict = gather_ingredients_by_meal(random_key[0])

    #Render with correct data
    return render_template('lucky.html', recipe_name=display_name, data=ingredients_dict)

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


if __name__ == "__main__":
    app.run(debug=True)
