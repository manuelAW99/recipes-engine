from json import load, dump

full_recipes = load(open("555Nitza/parsed_data/recipes.json"))
recipes5k = load(open("5KRecipes/parsed_data/recipes.json"))

for key, value in recipes5k.items():
    if key not in full_recipes:
        full_recipes[key] = value

dump(full_recipes, open("recipes.json", "w"))