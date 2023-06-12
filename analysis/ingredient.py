# -*- coding:utf-8 -*- 

from os import path
import itertools
import datetime
import pandas as pd
import networkx as nx
from .relation import pointwise_mutual_information
from parser import RecipeJSON


class FoodGraph():
    
    def __init__(self, graph_path=None, recipes_path=None, save_path='data/'):
        """
        Load into memory or build the model (graph)
        
        Args:
            - graph_path (str, optional): Path of the precomputed model file. Path of the precomputed model file. The file is expected to have `.graphml` extension. Defaults to None.
            - recipes_csv_path (str, optional): Path of the file in json format, with the information of the recipes. Defaults to None.
            - save_path (str, optional): If recipes_csv_path is non-null, it indicates the folder where the model will be stored. Defaults to 'data/'.
            
        Raise:
            - ValueError: The path of these files has a null value. The `graph_path` or `recipes_path` parameter must have a value.
            
        """ 
        if graph_path is None and recipes_path is None:
            raise ValueError('Both parameters (graph_path, recipes_csv_path) have null value. Unable to build or load model.')
        elif not graph_path is None:
            self._load_model(graph_path) 
        else: 
            self._build_model(recipes_path, save_path)
            
    def _load_model(self, graph_path):
        """Load a graph, from a file

        Args:
            - graph_path (str, optional): Path of the precomputed model file. The file is expected to have `.graphml` extension.
            
        Raises:
            - FileNotFoundError: If the information in the `graph_path` parameter is not a valid file path.
            - EOFError: If the extension of the `graph_path` file is not 'graphml'.
            
        """  
        if not path.isfile(graph_path):
            raise FileNotFoundError('Path file `' + graph_path + '` does not exist')
        
        _, file_extension = path.splitext(graph_path)
        if file_extension != '.graphml':
            raise EOFError('File defined in the `graph_path` parameter does not have the expected extension (.graphml). Extension found ' + file_extension)

        self.graph = nx.read_graphml(graph_path)   
        
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
        
        # csv = pd.read_csv(fdata, sep='|')
        # n_rows, _ = csv.shape
        # (relationship_belonged, ingredientes) = self._token_by_text(csv)
        data = RecipeJSON(data_path)
        
        self.graph = nx.Graph()
        self._create_nodes(data.get_recipes())
        self._create_edges(data.get_recipes)
        # #todo: annadir aca las aristas ingrediente - receta, poniendo como propiedades, el ingredientes estructurado
                
        if not fdest is None:
            time = datetime.datetime.now()
            fname = 'ingredient_graph_' + time.strftime("%d-%m-%Y %H:%M:%S") + '.graphml'
            fpath = path.join(fdest, fname)
            nx.write_graphml_xml(self.graph, fpath)
        
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
            self.graph.add_node(node_name, **tags)
            
            for ingredient in recipe['ingredientes']:
                node_name = ingredient['nombre']
                tags = dict([
                    ('type', 'ingredient_name'),
                    ('label', node_name)
                ])
                self.graph.add_node(node_name, **tags)
        
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
        """Creates the edges of the graph, associated to the correlation between the ingredients. The edges will have the fields:
            - weight (float): Value that indicates the correlation between the nodes that it joins.
            - type(str): Default to 'ingredient-ingredient correlation'.

        Args:
            recipes (instance of an enumerator function): Recipes list. Each object returned by the iterator is expected to be a dictionary with the fields:
                - nombre (str): Recipe name.
                - ingredientes (list of dict): List of ingredients. Its fields are:
                    - nombre (str): Nombre del ingrediente.
                    - variantes (list of int): List of ingredients that can be substituted. The list contains positions within the `ingredients` list.
        
        """
        relation = dict()
        n_recipes = 0
        
        for recipe in recipes():
            n_recipes += 1
            recipe_name = recipe['nombre']
            
            for ingredient in recipe['ingredientes']:
                ingredient_name = ingredient['nombre']
                if ingredient_name in relation:
                    relation[ingredient_name].add(recipe_name)
                else:
                    relation[ingredient_name] = set([recipe_name])
                    
        for (ingredient1, ingredient2) in itertools.combinations(relation.keys(), 2):
            value = pointwise_mutual_information(ingredient1, ingredient2, relation, n_recipes)
            if not value is None: 
                tags = dict([
                    ('type', 'ingredient-ingredient correlation'),
                    ('value', value),
                    ('weight', value),
                    ('label', 'i-i c: ' + str(value))
                ])
                self.graph.add_edge(ingredient1, ingredient2, **tags)   
    
    def _create_ingredient_substitution_edges(self, recipes):
        pass
    
    def _create_edges_of_belonging(self, recipes):
        pass
    
    
    
    
    
        
        
        
        
        
        
        
        
        
 