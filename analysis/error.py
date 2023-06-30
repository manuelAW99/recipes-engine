# -*- coding:utf-8 -*- 


class IngredientNotFoundError(Exception):
    """Raised when a certain ingredient does not appear in the graph
    """
    pass

class RecipeNotFoundError(Exception):
    """Raised when a certain recipe does not appear in the graph
    """
    pass