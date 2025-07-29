"""
Package des modèles de données

Contient :
- ingredient.py : Modèle d'ingrédient
- recette.py : Modèle de recette
- base_connaissances.py : Base de données des recettes
"""

from .ingredient import Ingredient
from .recette import Recette
from .base_connaissances import BaseConnaissances

__all__ = ['Ingredient', 'Recette', 'BaseConnaissances']