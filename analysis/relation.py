# -*- coding:utf-8 -*- 

from math import log


def pointwise_mutual_information(x, y, relation, n_docs, n_decimal_digits = 6):
        """Calculate the relationship between two tokens
        
        Pointwise Mutual Information is calculated in as
            PMI = log2[ P(x, y) / P(x)P(y) ]
        where
            x, y - tokens
            P - Probability function
            P(x, y) = (number of documents containing x and y) / (number of documents)
            P(x) = (number of documents containing x) / (number of documents)
            P(y) = (number of documents containing y) / (number of documents)
        
        then
            PMI = (Lxy * L) / (La * Lb)
        where
            Lxy = number of documents containing x and y
            L = number of documents
            La = number of documents containing x
            Lb = number of documents containing y
            
        Args:
            x (str): Token.
            y (str): Token.
            relation (dict(str, list of str)): Dictionary of relations.
            n_docs (int): Total number of documents.
            n_decimal_digits (int): Number of decimal digits, to approximate.

        Returns:
            float or None: Numerical value, if the values are related
            
        """
        text_x = relation[x]
        text_y = relation[y]
        
        Lxy = len(text_x.intersection(text_y))
        Lx = len(text_x)
        Ly = len(text_y)
        
        return None \
            if Lxy == 0 or Lx == 0 or Ly == 0 \
            else round(log((Lxy * n_docs) / (Lx * Ly), 2), 6)