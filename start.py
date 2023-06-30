# -*- coding:utf-8 -*- 
#!/usr/bin/env python



from analysis import FoodGraph
from tmp_create import create_recipes_and_save_csv
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Creating graphs ...")
info = FoodGraph(recipes_path='data/recipes.json')
logging.info("Graphs created")