from flask import Flask, render_template, request, redirect, url_for
from dictionary_parser import gather_full_ingredient_list, gather_ingredient_by_key, gather_meals_by_category, gather_ingredients_by_meal

app = Flask(__name__)

# Render homepage/index
@app.route('/')
def index():
    return render_template('index.html')

# Render recipe-search
@app.route('/recipe_search', methods=["GET", "POST"])
def show_results():
    recipe_list = gather_meals()
    for recipe in recipe_list:
        if recipe[0][0] is request.form["recipename"]:
            ingredients_list = {}
            for ingredient in recipe[6]:
                 ingredients_list = update(ingredient)
            return render_template('ingredients.html', recipe_name=recipename, data=ingredients_list)

# Render lucky
@app.route('/lucky')
def random():
    size = 0
    recipe_list = gather_meals()
    for recipe in recipe_list:
        size = size + 1
    random_recipe = recipe_list[randrang(size+1)]
    random_name = recipe_list[0][0]
    ingredients_list = {}
    for ingredient in random_recipe[6]:
        ingredient_list = update(ingredient)
    return render_template('lucky.html', recipe_name=random_name, data=ingredient_list)

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
