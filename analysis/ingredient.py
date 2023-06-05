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
        """Carga un modelo de grafo

        Args:
            model_file (str): Path of the precomputed model file. The file is expected to have `.graphml` extension.
            
        """  
        raise NotImplementedError('')    
        
        
    def build_model(self, fdata, fdest = None):
        """Construct the relationship graph between the ingredients. Two ingredients are related if they appear in the same recipe.

        Args:
            fdata (str): CSV file path, which contains the information to build the relationship graph. The file is expected to have the columns:
                - recipe (str) Indicates the name of the recipe
                - ner (list of str) Indicates recipe ingredients
                
            fdest (str): Folder path to store the model. If it does not have a defined value, the file will not be created; otherwise, the file will be created with the extension `.graphml` and with name `ingredient_graph`, concatenated from the date the file was created. Defaults to None.
            
        Raises:
            FileNotFoundError: Si la información del parametro `fdata` no es una ruta de un fichero válido.
            EOFError: Si la extensión del fichero `fdata` no es 'csv'.
            NotADirectoryError: Si la información del parametro `fdata` no es una ruta de una carpeta válida.
            
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
        relationship_belonged = self._token_by_text(csv)
        
        self.graph = nx.Graph()
        
        for (ingredient1, ingredient2) in itertools.combinations(relationship_belonged.keys(), 2):
            value = pointwise_mutual_information(ingredient1, ingredient2, relationship_belonged, n_rows)
            if not value is None: 
                self.graph.add_edge(ingredient1, ingredient2, weight=value)
                
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
            dict(str, set): Diccionario ingredientes - conjunto de recetas en el que aparece
            
        """
        relation = dict()
        
        n_rows, _ = data.shape
        for i in range(n_rows):
            row = data.iloc[i]
            recipe_name = row['recipe']
            
            for ingredient in row['ner'][1:-2].replace("'", '').split(', '):
                if ingredient in relation:
                    relation[ingredient].add(recipe_name)
                else:
                    relation[ingredient] = set([recipe_name])
                    
        return relation
    
    
        
        
        
        
        
        
        
        
        
 