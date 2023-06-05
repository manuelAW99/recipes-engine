# -*- coding:utf-8 -*- 

from os import path
import itertools
import datetime
import pandas as pd
import networkx as nx
from .relation import pointwise_mutual_information


class IngredientGraph():
    
    def __init__(self, model_file = None):
        """
        Args:
            model_file (str, optional): Path of the precomputed model file. Path of the precomputed model file. The file is expected to have `.graphml` extension. Defaults to None.
            
        """ 
        if model_file is None:
            self.graph = None
        else:
            self.graph = self.load_model(model_file) 
            
            
    def load_model(self, model_file):
        """Load a graph, from a file

        Args:
            model_file (str): Path of the precomputed model file. The file is expected to have `.graphml` extension.
            
        Raises:
            FileNotFoundError: If the information in the `model_file` parameter is not a valid file path.
            EOFError: If the extension of the `model_file` file is not 'graphml'.
            
        """  
        if not path.isfile(model_file):
            raise FileNotFoundError('Path file `' + model_file + '` does not exist')
        
        _, file_extension = path.splitext(model_file)
        if file_extension != '.graphml':
            raise EOFError('File defined in the `model_file` parameter does not have the expected extension (.graphml). Extension found ' + file_extension)

        self.graph = nx.read_graphml(model_file)   
        
        
    def build_model(self, fdata, fdest = None):
        """Construct the relationship graph between the ingredients. Two ingredients are related if they appear in the same recipe.

        Args:
            fdata (str): CSV file path, which contains the information to build the relationship graph. The file is expected to have the columns:
                - recipe (str) Indicates the name of the recipe
                - ner (list of str) Indicates recipe ingredients
                
            fdest (str): Folder path to store the model. If it does not have a defined value, the file will not be created; otherwise, the file will be created with the extension `.graphml` and with name `ingredient_graph`, concatenated from the date the file was created. Defaults to None.
            
        Raises:
            FileNotFoundError: If the information in the `fdata` parameter is not a valid file path.
            EOFError: If the extension of the `model_file` file is not 'csv'.
            NotADirectoryError: If the data in the `fdata` parameter is not a valid folder path.
            
        """        
        if not path.isfile(fdata):
            raise FileNotFoundError('Path file `' + fdata + '` does not exist')
        
        _, file_extension = path.splitext(fdata)
        if file_extension != '.csv':
            raise EOFError('File defined in the `fdata` parameter does not have the expected extension (.csv). Extension found ' + file_extension)
        
        if not (fdest is None or path.isdir(fdest)):
            raise NotADirectoryError('Path folder `' + fdest + '` does not exist')
        
        csv = pd.read_csv(fdata, sep='|')
        n_rows, _ = csv.shape
        (relationship_belonged, ingredientes) = self._token_by_text(csv)
        
        self.graph = nx.Graph()
        self._create_nodes(ingredientes, dict([('type', 'ingredient')]))
        self._create_edges(relationship_belonged, n_rows)
                
        if not fdest is None:
            time = datetime.datetime.now()
            fname = 'ingredient_graph_' + time.strftime("%d-%m-%Y %H:%M:%S") + '.graphml'
            fpath = path.join(fdest, fname)
            nx.write_graphml_xml(self.graph, fpath)
        
        
    def _token_by_text(self, data):
        """Build the list of ingredients by recipes

        Args:
            data (pandas.core.frame.DataFrame): Recipe information.

        Returns:
            (dict(str, set), set): 
                Dictionary ingredients - set of recipes in which it appears and,
                Set of all ingredients.
            
        """
        relation = dict()
        ingredients = set()
        
        n_rows, _ = data.shape
        for i in range(n_rows):
            row = data.iloc[i]
            recipe_name = row['recipe']
            
            for ingredient in row['ner'][1:-2].replace("'", '').split(', '):
                ingredients.add(ingredient)
                
                if ingredient in relation:
                    relation[ingredient].add(recipe_name)
                else:
                    relation[ingredient] = set([recipe_name])
                    
        return (relation, ingredients)
    
    def _create_nodes(self, nodes, tags):
        """Create the graph nodes

        Args:
            nodes (list of str): Node list.
            tags (dict): Dictionary with node properties.
            
        """
        for node_name in nodes:
            self.graph.add_node(node_name, **tags)        
        
    def _create_edges(self, relation, n_recipes):
        """Create the graph edges

        Args:
            relation (dict(str, list of str)): Dictionary ingredients - set of recipes in which it appears.
            n_recipes (int): Total recipes.
            
        """     
        for (ingredient1, ingredient2) in itertools.combinations(relation.keys(), 2):
            value = pointwise_mutual_information(ingredient1, ingredient2, relation, n_recipes)
            if not value is None: 
                self.graph.add_edge(ingredient1, ingredient2, weight=value)   
    
    
    
    
    
        
        
        
        
        
        
        
        
        
 