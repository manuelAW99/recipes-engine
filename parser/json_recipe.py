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
                
    def get_recipes(self):
        """Returns the recipes

        Yields:
            dict: The fields are: 
                - name (str): Recipe name.
                - ingredients (list of dict): List of ingredients. Its fields are:
                    - name (str): Ingredient name.
                    - variants (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
                - ingredients_simplified (list of dict): List of standardized/simplified ingredients. Its fields are:
                    - name (str): Ingredient name.
                    - variants (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
            
        """        
        for key, value in self.recipes.items():
            restructured = dict()
            restructured['name'] = key
            restructured.update(value)
            
            yield restructured
    

