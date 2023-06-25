from json import dump

recipes_file = open("raw_data/classes_Recipes5k.txt", "r")
recipes = recipes_file.readlines()

ingredients_file = open("raw_data/ingredients_Recipes5k.txt", "r")
ingredients = ingredients_file.readlines()

ingredients_simpl_file = open("raw_data/ingredients_simplified_Recipes5k.txt", "r")
ingredients_simpl = ingredients_simpl_file.readlines()

recipes_file.close()
ingredients_file.close()
ingredients_simpl_file.close()

recipes_with_ing = {}
for rs, ing, ings in zip(recipes, ingredients, ingredients_simpl):
    recipes_with_ing[rs.replace("\n", "").lower()] = {
        "ingredients_extended": [{"name": i.replace("\n", "").replace("_", " "), "variants": []} for i in ing.split(",")],
        "ingredients": [{"name": i.replace("\n", "").replace("_", " "), "variants": []} for i in ings.split(",")]
    }
    
dump(recipes_with_ing, open("parsed_data/recipes.json", "w"))