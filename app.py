from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(__name__)

# Replace with your Spoonacular API key
API_KEY = "eca09c6bac4145bd9cf91b73fbdcbc28"

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = ''
    recipes = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
    else:
        search_query = request.args.get('search_query', '')

    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)

    return render_template('foodindex.html', recipes=recipes, search_query=search_query)

def search_recipes(query):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['results']
    except requests.RequestException:
        return []

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    except requests.RequestException:
        return 'Recipe not found', 404

if __name__ == '__main__':
    app.run(debug=True)
