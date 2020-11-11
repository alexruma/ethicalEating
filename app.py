from flask import Flask, render_template, request, redirect, url_for
from dictionary_parser import gather_full_ingredient_list
app = Flask(__name__)


# Render homepage/index
@app.route('/')
def index():
    return render_template('index.html')

# Render meal-search
@app.route('/meal_search')
def meal_search():
    return render_template('meal-search.html')


# Render create-recipe
@app.route('/create_recipe', methods=["GET", "POST"])
def create_recipe():
    ingredient_list = gather_full_ingredient_list()

    if request.method == "POST":
        # Contains name entered in form name input.
        recipe_name = request.form["recipe_name"]
        
        # Populate list of checked ingredients
        ingredient_list = []
        for key in request.form:
            if request.form[key]:
                ingredient_list.append(request.form[key])

        return redirect(url_for("new_recipe", new_recipe_name = recipe_name, ingredients = ingredient_list))
    return render_template('create-recipe.html', data=ingredient_list)

# Render page with user created recipe
@app.route("/<new_recipe_name>/<ingredients>")
def new_recipe(new_recipe_name, ingredients):
    return render_template('new_recipe.html', recipe_name = new_recipe_name, recipe_ingredients = ingredients)

if __name__ == "__main__":
    app.run(debug = True)
