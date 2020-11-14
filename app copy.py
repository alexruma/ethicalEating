
import os
from json_handler import JSONHandler
from dictionary_parser import gather_full_ingredient_list
from flask import Flask, render_template, request, redirect, url_for
#from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = 'alex'

# toolbar = DebugToolbarExtension(app)


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
    if request.method == "POST":
        
        # Contains name entered in form name input.
        recipe_name = request.form["recipe_name"]
       
        # Populate list of checked ingrednients
        ingredient_list =[]
        for key in request.form:
            if request.form[key]:
                ingredient_list.append(request.form[key])

        print(ingredient_list)
        return redirect(url_for("new_recipe", new_recipe_name = recipe_name, ingredients = ingredient_list))
    return render_template('create-recipe.html')

# Render page with user created recipe
@app.route("/<new_recipe_name>/<ingredients>" , methods=["GET", "POST"])
def new_recipe(new_recipe_name, ingredients):
    testDate = request.data
    return render_template('new_recipe.html', recipe_name = new_recipe_name, recipe_ingredients = ingredients)

@app.route("/test")
def test():
    ingredients = gather_full_ingredient_list()
    return render_template("test.html", len = len(ingredients), ingredients = ingredients) 


if __name__ == "__main__":
    app.run(debug = True)