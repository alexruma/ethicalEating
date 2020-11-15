from flask import Flask, render_template, request, redirect, url_for
from dictionary_parser import gather_full_ingredient_list, gather_ingredient_by_key, gather_meals_by_category, gather_meals_dict_by_category, gather_ingredients_by_meal
app = Flask(__name__)

# Render homepage/index
@app.route('/')
def index():
    return render_template('index.html')

# Render recipe-search
@app.route('/recipe_search')
def recipe_search():
    return render_template('recipe_search.html')


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
        print(key)
        ingredients_dict.update(gather_ingredient_by_key(key))

    return render_template('ingredients.html', recipe_name=recipe_name, data=ingredients_dict)

# Handle POST request from selecting meal on index page. Will redirect to approriate recipe list page.
@app.route("/recipes_direct", methods=["POST"])
def recipe_list_direct():

    meal_name = request.form['submit']
    print(meal_name)

    return redirect(url_for("recipes", meal_name = meal_name))

# Render list_of_recipes
@app.route("/<meal_name>/" , methods=["GET", "POST"])
def recipes(meal_name):
    print(meal_name)
    meal_dict = gather_meals_dict_by_category(meal_name)
   
    print(meal_dict)
  

    return render_template('recipes.html', meal_name = meal_name, meal_dict = meal_dict)

# Handle GET request from selecting meal on recipes.html and render ingredients.
@app.route("/recipe_display", methods=["GET"])
def recipe_display():

    key = request.args['meal']
    recipe_name = request.args['name']

    ingredients = gather_ingredients_by_meal(key)
    print(ingredients)

    return render_template('recipe_display.html', ingredients = ingredients, recipe_name = recipe_name)

if __name__ == "__main__":
    app.run(debug=True)
