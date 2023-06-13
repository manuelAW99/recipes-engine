# -*- coding:utf-8 -*- 

from os import path
import itertools
import datetime
import pandas as pd
import networkx as nx
from .relation import pointwise_mutual_information
from parser import RecipeJSON


INGREDIENT_SUBSTITUTION_GRAPH_FILE = 'ingredient_substitution_graph.graphml'
INGREDIENT_CORRELATION_GRAPH_FILE = 'ingredient_correlation_graph.graphml'
RECIPE_INGREDIENT_RELATIONSHIP_GRAPH_FILE = 'recipe_ingredient_relationship_graph.graphml'


class FoodGraph():
    
    def __init__(self, graphs_path=None, recipes_path=None, save_path='data/'):
        """
        Load into memory or build the model (graph)
        
        Args:
            - graphs_path (str, optional): Path of the folder that contains the graphs. The `ingredient_substitution_graph.graphml`, `ingredient_correlation_graph.graphml` and `recipe_ingredient_relationship_graph.graphml` files are expected to exist inside the folder. Defaults to None.
            - recipes_csv_path (str, optional): Path of the file in json format, with the information of the recipes. Defaults to None.
            - save_path (str, optional): If recipes_csv_path is non-null, it indicates the folder where the model will be stored. Defaults to 'data/'.
            
        Raise:
            - ValueError: The path of these files has a null value. The `graphs_path` or `recipes_path` parameter must have a value.
            
        """ 
        if graphs_path is None and recipes_path is None:
            raise ValueError('Both parameters (graphs_path, recipes_csv_path) have null value. Unable to build or load model.')
        elif not graphs_path is None:
            self._load_model(graphs_path) 
        else: 
            self._build_model(recipes_path, save_path)
            
            
    def _load_model(self, graphs_path):
        """Load graphs from a containing folder

        Args:
            - graphs_path (str): Path of the folder that contains the graphs. The `ingredient_substitution_graph.graphml`, `ingredient_correlation_graph.graphml` and `recipe_ingredient_relationship_graph.graphml` files are expected to exist inside the folder.
            
        Raises:
            - NotADirectoryError: If the folder path (parameter) does not exist.
            - FileNotFoundError: If any expected file is not found, inside the defined folder.
            
        """  
        if not path.isdir(graphs_path):
            raise NotADirectoryError('Path folder `' + graphs_path + '` does not exist.')
        
        file = path.join(graphs_path, INGREDIENT_SUBSTITUTION_GRAPH_FILE)
        if not path.isfile(file):
            raise FileNotFoundError('Cannot find `' + INGREDIENT_SUBSTITUTION_GRAPH_FILE + '` file, inside `' + graphs_path + '`.')
        else:
            self.ingredient_substitution_graph = nx.read_graphml(file) 
            
        file = path.join(graphs_path, INGREDIENT_CORRELATION_GRAPH_FILE)
        if not path.isfile(file):
            raise FileNotFoundError('Cannot find `' + INGREDIENT_CORRELATION_GRAPH_FILE + '` file, inside `' + graphs_path + '`.')
        else:
            self.ingredient_correlation_graph = nx.read_graphml(file)
            
        file = path.join(graphs_path, RECIPE_INGREDIENT_RELATIONSHIP_GRAPH_FILE)
        if not path.isfile(file):
            raise FileNotFoundError('Cannot find `' + RECIPE_INGREDIENT_RELATIONSHIP_GRAPH_FILE + '` file, inside `' + graphs_path + '`.')
        else:
            self.recipe_ingredient_relationship_graph = nx.read_graphml(file)
        
        
    def _build_model(self, data_path, fdest = None):
        """Construct the relationship graph between the ingredients. Two ingredients are related if they appear in the same recipe.

        Args:
            - data_path (str): JSON file path, which contains the information to build the relationship graph. The file is expected to have the columns:
                - recipe (str) Indicates the name of the recipe
                - ner (list of str) Indicates recipe ingredients
                
            - fdest (str): Folder path to store the model. If it does not have a defined value, the file will not be created; otherwise, the file will be created with the extension `.graphml` and with name `ingredient_graph`, concatenated from the date the file was created. Defaults to None.
            
        Raises:
            - FileNotFoundError: If the information in the `data_path` parameter is not a valid file path.
            - EOFError: If the extension of the `model_file` file is not 'csv'.
            - NotADirectoryError: If the data in the `data_path` parameter is not a valid folder path.
            
        """     
        if not path.isfile(data_path):
            raise FileNotFoundError('Path file `' + data_path + '` does not exist')
        
        _, file_extension = path.splitext(data_path)
        if file_extension != '.json':
            raise EOFError('File defined in the `data_path` parameter does not have the expected extension (.json). Extension found ' + file_extension)
        
        if not (fdest is None or path.isdir(fdest)):
            raise NotADirectoryError('Path folder `' + fdest + '` does not exist')
        
        data = RecipeJSON(data_path)
        
        self.ingredient_substitution_graph = nx.Graph()
        self.ingredient_correlation_graph = nx.Graph()
        self.recipe_ingredient_relationship_graph = nx.Graph()
        
        self._create_nodes(data.get_recipes())
        self._create_edges(data.get_recipes)
                
        if not fdest is None:
            nx.write_graphml_xml(self.ingredient_substitution_graph, path.join(fdest, INGREDIENT_SUBSTITUTION_GRAPH_FILE))
            nx.write_graphml_xml(self.ingredient_correlation_graph, path.join(fdest, INGREDIENT_CORRELATION_GRAPH_FILE))
            nx.write_graphml_xml(self.recipe_ingredient_relationship_graph, path.join(fdest, RECIPE_INGREDIENT_RELATIONSHIP_GRAPH_FILE))
            
            
    def _create_nodes(self, recipes):
        """Create the graph nodes

        Args:
            recipes (list of dict): Recipes list.
            
        """
        for recipe in recipes:
            node_name = recipe['nombre']
            tags = dict([
                ('type', 'recipe_name'),
                ('label', node_name)
            ])
            self.recipe_ingredient_relationship_graph.add_node(node_name, **tags)
            
            self.ingredient_substitution_graph
            self.ingredient_correlation_graph
            self.recipe_ingredient_relationship_graph
            
            for ingredient in recipe['ingredientes']:
                node_name = ingredient['nombre']
                tags = dict([
                    ('type', 'ingredient_name'),
                    ('label', node_name)
                ])
                self.ingredient_substitution_graph.add_node(node_name, **tags)
                self.ingredient_correlation_graph.add_node(node_name, **tags)
                self.recipe_ingredient_relationship_graph.add_node(node_name, **tags)
        
        
    def _create_edges(self, recipes):
        """Create the graph edges

        Args:
            recipes (instance of an enumerator function): Recipes list. Each object returned by the iterator is expected to be a dictionary with the fields:
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list. 
            
        """
        self._create_correlation_edges_of_ingredients(recipes)
        self._create_ingredient_substitution_edges(recipes)
        self._create_edges_of_belonging(recipes)
        
    
    def _create_correlation_edges_of_ingredients(self, recipes):
        """Creates the edges of the graph, associated to the correlation between the ingredients.

        Args:
            recipes (instance of an enumerator function): Recipes list. Each object returned by the iterator is expected to be a dictionary with the fields:
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
        
        """
        relation = dict()
        n_recipes = 0
        
        # Build a comfortable structure for work. ingredient -> recipes in which it appears
        for recipe in recipes():
            n_recipes += 1
            recipe_name = recipe['nombre']
            
            for ingredient in recipe['ingredientes']:
                ingredient_name = ingredient['nombre']
                if ingredient_name in relation:
                    relation[ingredient_name].add(recipe_name)
                else:
                    relation[ingredient_name] = set([recipe_name])
                    
        # Establish the edges (relationship) between the pairs of ingredients
        for (ingredient1, ingredient2) in itertools.combinations(relation.keys(), 2):
            value = pointwise_mutual_information(ingredient1, ingredient2, relation, n_recipes)

            # Ignore the value=None, since it means that the pair of ingredients never appear in the same recipe
            if not value is None: 
                tags = dict([
                    ('type', 'ingredient-ingredient correlation'),
                    ('value', value),
                    ('weight', value),
                    ('label', 'i-i c: ' + str(value))
                ])
                self.ingredient_correlation_graph.add_edge(ingredient1, ingredient2, **tags)   
 
 
    def _create_ingredient_substitution_edges(self, recipes):
        """Create the edges of the graph, to establish the ingredient substitution relationship

        Args:
            Args:
            recipes (instance of an enumerator function): Recipes list. Each object returned by the iterator is expected to be a dictionary with the fields:
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
            
        """        
        relations = []
        
        # Extract the relations, according to the recipes
        for recipe in recipes():
            ingredients = [ingredient for ingredient in recipe['ingredientes']]
            mark = [True for _ in range(len(ingredients))]
            
            for i in range(len(mark)): 
                substitutions = ingredients[i]['variantes']
                
                if mark[i] and len(substitutions) > 0:
                    
                    # Extract substitution relationships within the recipe
                    relations.append(set())

                    for j in [i] + ingredients[i]['variantes']:
                        mark[j] = False
                        relations[-1].add(ingredients[j]['nombre'])
                        
        #todo: Analizar si sería beneficioso eliminar los duplicados. Se pudiese hacer algo como: si una relación ya existe, aumentaré el peso de la arista q existe entre ambos nodos, para indicar un mayor valor entre ellos.
        # Remove duplicate relationships
        relations = [relation for i, relation in enumerate(relations) \
            if not relation in relations[i+1:]]
        
        # Establish the edges (relationship) between the pairs of ingredients
        for relation in relations:
            for (ingredient1, ingredient2) in itertools.combinations(relation, 2):
                value = 1
                tags = dict([
                    ('type', 'ingredient-ingredient substitution'),
                    ('weight', value),
                    ('label', 'i-i s: ' + str(value))
                ])
                self.ingredient_substitution_graph.add_edge(ingredient1, ingredient2, **tags)   
            
    
    def _create_edges_of_belonging(self, recipes):
        """Creates the edges of the graph, which relates the recipes with the ingredients that make it up

        Args:
            recipes (instance of an enumerator function): Recipes list. Each object returned by the iterator is expected to be a dictionary with the fields:
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
            
        """  
        for recipe in recipes(): 
            recipe_name = recipe['nombre']
            
            for ingredient in recipe['ingredientes']:
                ingredient_name = ingredient['nombre']
                
                #todo: ver si las propiedades de los nodos y las aristas, serán en español o inglés
                tags = dict(filter(lambda elem: elem[0] in ['opcional', 'cantidad', 'unidad', 'forma'], ingredient.items()))
                
                #todo: analizar si poner peso contante a todas las aristas
                tags['weight'] = 1
                #todo: analizar si ponerle label a la arista y qué ponerle
                
                self.recipe_ingredient_relationship_graph.add_edge(recipe_name, ingredient_name, **tags) 
            
    
    
    
    
    
        
        
        
        
        
        
        
        
        
 