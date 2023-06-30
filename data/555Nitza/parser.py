from json import load, dump
from pprint import pprint
from translate import Translator
translator = Translator(from_lang='es', to_lang='en')

recipes: dict = load(open("raw_data/recipes.json", "r"))

ingredients_set: set = set()
recipes_set: set = set([recipe for recipe in recipes])

for recipe in recipes:
    for ingredient in recipes[recipe]["ingredientes"]:
        ingredients_set.add(ingredient["nombre"])

def group_to_trans(name: str, words: set, size: int = 20, save: bool = False) -> list:
    words_list = []
    current_str = ""
    for i, w in enumerate(words):
        current_str+=w
        if i%size == 0 and i!=0:
            words_list.append(current_str)
            current_str = ""
        elif i == len(words)-1:
            words_list.append(current_str)
        else: 
            current_str+="; "
    if save:
        dump(words_list, open(file=f"group_{name}.json", mode="w"))
    return words_list

# groups_ing = group_to_trans("ingredients", ingredients_set, size=20)
# gropus_rec = group_to_trans("recipes", recipes_set, size=10)

def translate(word: str, dictionary: dict) -> str:
    words = [sentence.strip() for sentence in word.lower().split(';')]
    trans_words = [sentence.strip() for sentence in translator.translate(word).lower().split(';')]
    
    for w, tw in zip(words, trans_words):
        if tw: dictionary[w] = tw
        else: dictionary[w] = w
    
    return dictionary

def translate_group(name: str, sentences: set, save: bool = False):
    dictionary = {}
    for sentence in sentences:
        translate(sentence, dictionary)
    if save:
        dump(dictionary, open(file=f"trans_{name}.json", mode="w"))

# translate_group("recipes", gropus_rec, save=True) 
# translate_group("ingredients", groups_ing, save=True)

translate_ing = load(open("parsed_data/trans_ingredients.json", "r"))
translate_rec = load(open("parsed_data/trans_recipes.json", "r"))

new_recipes: dict = {}

for recipe in recipes:
    new_name = translate_rec[recipe.lower()]
    new_recipes[new_name] = {"ingredients": [], "ingredients_extended": []}
    for ingredient in recipes[recipe]["ingredientes"]:
        new_ing_name = translate_ing[ingredient["nombre"]]
        new_recipes[new_name]["ingredients"].append({"name": new_ing_name, "variants": ingredient["variantes"]})
        
dump(new_recipes, open(file=f"recipes.json", mode="w"))