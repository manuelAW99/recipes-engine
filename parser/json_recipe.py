# -*- coding:utf-8 -*- 

import json
from os import path

class RecipeJSON:
    """
    Class oriented to the extraction of the data from the JSON file, with the information of the recipes
    """    
    
    def __init__(self, pfile):
        """
        Args:
            pfile (str): Path of the JSON file with the definition of the recipes.
            
        """
        if pfile is None: 
            raise ValueError('')
        elif not path.isfile(pfile):
            raise FileNotFoundError('')
        else: 
            with open(pfile, 'r', encoding='utf8', errors='ignore') as f:
                self.recipes = json.load(f)
                
    # def ingredients_name(self):
    #     """Returns the list of all ingredients

    #     Returns:
    #         list od str: List of ingredients
            
    #     """
    #     ingredients = set()
    #     for data in self.recipes.values():
    #         for ing in data['ingredientes']:
    #             ingredients.add(ing['nombre'])
        
    #     return list(ingredients)
    
    # def recipes_name(self):
    #     """Returns the name of all recipes

    #     Returns:
    #         list od str: List of ingredients
            
    #     """
    #     return [d['nombre'] for d in self.recipes.values()]
    
    def get_recipes(self):
        """Returns the recipes

        Yields:
            dict: The fields are: 
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
            
        """        
        for recipe in self.recipes.values():
            yield recipe
    
    # def 




