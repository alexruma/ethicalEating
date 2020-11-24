from flask import Flask, render_template, request, redirect, url_for
from dictionary_parser import gather_full_ingredient_list, gather_ingredient_by_key, gather_meals
from random import randrange
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
    size = len(recipe_list)
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
        print(key)
        ingredients_dict.update(gather_ingredient_by_key(key))

    return render_template('ingredients.html', recipe_name=recipe_name, data=ingredients_dict)


if __name__ == "__main__":
    app.run(debug=True)
