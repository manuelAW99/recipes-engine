import pandas as pd
import ingredient_parser as ip
import logging, pprint as pp
from yaml import safe_load, safe_dump
from json import load, dump
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from pathlib import Path

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

from translate import Translator
translator = Translator(to_lang='es')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

convert_units = {
    'tsp.': 'teaspoon',
    'c.': 'cup',
    'tbsp.': 'tablespoon',
    'pkg.': 'package',
    'kg.': 'kilogram',
    'g.': 'gram',
    'ml.': 'milliliter',
    'l.': 'liter',
    'oz.': 'ounce',
    'lb.': 'pound',
    'pt.': 'pint',
    'qt.': 'quart',
    'gal.': 'gallon',
}

abbreviation = set(convert_units.keys())
units = {}

trans_ingredients = {}

def parse(sentence: str) -> str:
    sentence = sentence.lower()
    current_word = ""
    for char in sentence:
        if char == " " or char == '(' or char == ')' or char == ',':
            if current_word in abbreviation:
                sentence = sentence.replace(current_word, convert_units[current_word])
            current_word = ""
        else:
            current_word += char
    return sentence

def translate(word: str, dictionary: dict) -> str:
    words = [sentence.strip() for sentence in word.lower().split(';')]
    trans_words = [sentence.strip() for sentence in translator.translate(word).lower().split(';')]
    
    for w, tw in zip(words, trans_words):
        if tw: dictionary[w] = tw
        else: dictionary[w] = w
    
    return dictionary

def load_csv(csv: str, column: str) -> list:
    df = pd.read_csv(
        filepath_or_buffer=csv,
        sep=',',
        header=0,
        )
    
    col = df[column]
    return col

def parse_ingredients(csv: str) -> list:
    ingredients = load_csv(csv, 'ingredients')

    # Create a list of ingredients
    ingredients_list = [eval(i) for i in ingredients]
    
    # Parse the ingredients with ingredient_parser
    recipes = len(ingredients_list)
    parsed_ingredients = [0]*recipes
    for i, ing in enumerate(ingredients_list):
        current_recipe = [0]*len(ing)
        for j, sentence in enumerate(ing):
            sentence = parse(sentence)
            current_recipe[j] = ip.parse_ingredient(sentence)
            # current_recipe[j]['unit'] = translate(current_recipe[j]['unit'], units)
            current_recipe[j]['ingredient'] = stemmer.stem(current_recipe[j])
        parsed_ingredients[i] = current_recipe
        
        logger.info(f'Parsed {((i+1)*100)/recipes}% recipes')
    
    safe_dump(parsed_ingredients, open(file='parsed_ingredients.yml', mode='w'))
    return parsed_ingredients
    

# load all the files of a path
def load_files(path: str) -> list:
    files = []
    for file in Path(path).iterdir():
        if file.is_file():
            files.append(file)
    return files

def create_ingredients_set(ingredients: list, save: bool = False) -> set:
    ingredient_set = set([])
    for i, ing in enumerate(ingredients):
        for ingredient in eval(ing):
            if ingredient[:4] == 'http':
                continue
            for char in ingredient:
                if char in string.punctuation:
                    if char == '-':
                        ingredient = ingredient.replace(char, ' ')
                    elif char == '/':
                        ingredient = ingredient.replace(char, ' ')
                    else: ingredient = ingredient.replace(char, '')
            ingredient = ingredient.lower()
            ingredient_set.add(stemmer.stem(ingredient.strip()))
        if i % 2000 == 0:
            logger.info(f'{((i+1)*100)/len(ingredients)}% ingredients')
    if save: 
        safe_dump(list(ingredient_set), open(file='ingredients_set.yml', mode='w'))
    return ingredient_set

def group_ingredients(ingredients: set, size: int = 20, save: bool = False) -> list:
    ingredients_list = []
    current_str = ""
    for i, ing in enumerate(ingredients):
        if (i+1)%size == 0:
            ingredients_list.append(current_str)
            current_str = ""
        if i == len(ingredients):
            current_str+=ing
            ingredients_list.append(current_str)
            break
        else: 
            current_str+=f"{ing}; "
    if save:
        safe_dump(ingredients_list, open(file="group_ingredients.yml", mode="w"))
    return ingredients_list

def translate_ingredients(csv: str) -> list:    
    if Path('ingredients_set.yml').exists():
        ingredients_set = safe_load(open(file='ingredients_set.yml', mode='r'))
    else: 
        # ingredients_column = load_csv(csv, 'NER')
        # recipes = safe_load(open('parsed_ingredients.yml'))
        ingredients = []
        all_recipes = load_files(path='parsed_data/')
        # open a json file
        for file in all_recipes:
            file_open = load(open(file=file, mode='r'))
            for recipe in file_open:
                for ing in recipe['ingredients']:
                    ingredients.append(ing['name'])
            
        # ingredients_column = [ing['name'] for ing in recipes]
        ingredients_set = create_ingredients_set(ingredients, save=True)
    ingredients_groups = group_ingredients(ingredients_set)
    
    for i, group in enumerate(ingredients_groups):
        translate(group, trans_ingredients)
        logger.info(f'Translate {((i+1)*100)/len(ingredients_groups)}% ingredients')
        safe_dump(trans_ingredients, open(file='translate_ing.yml', mode='w'))

def main(args=None):
    # pi = parse_csv('RecipeNLG_dataset.csv')
    translate_ingredients(csv='RecipeNLG_dataset.csv')
    
    
if __name__ == '__main__':
    main()
