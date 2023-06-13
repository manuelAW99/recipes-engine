# -*- coding:utf-8 -*- 
#!/usr/bin/env python

from analysis import IngredientGraph
from tmp_create import create_recipes_and_save_csv

# create_recipes_and_save_csv(n_recipe=50, minimum_amount_of_ingredients=5, maximum_amount_of_ingredients=7, fname='crazy_recipes')

info = IngredientGraph()
# info.build_model('data/crazy_recipes.csv', 'data')
info.load_model('data/ingredient_graph_05-06-2023 16:16:33.graphml')

# print(nx.k_nearest_neighbors(info.graph))



# import networkx as nx

# G = nx.Graph()

# G.add_edge("a", "b", weight=0.6)
# G.add_edge("a", "c", weight=0.2)
# G.add_edge("c", "d", weight=0.1)
# G.add_edge("c", "e", weight=0.7)
# G.add_edge("c", "f", weight=0.9)
# G.add_edge("a", "d", weight=0.3)

# nx.write_graphml_lxml(G, "data/fourpath.graphml")