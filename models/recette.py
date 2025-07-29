from typing import List
from models.ingredient import Ingredient

class Recette:
    """Modèle représentant une recette culinaire complète"""
    
    def __init__(self, nom: str, ingredients: List[Ingredient], 
                 instructions: List[str], temps_preparation: int, 
                 difficulte: str, type_plat: str):
        """
        Initialise une nouvelle recette
        :param nom: Nom de la recette
        :param ingredients: Liste des ingrédients
        :param instructions: Étapes de préparation
        :param temps_preparation: Temps total en minutes
        :param difficulte: Niveau de difficulté
        :param type_plat: Catégorie (Entrée, Plat principal, Dessert)
        """
        self.nom = nom
        self.ingredients = ingredients
        self.instructions = instructions
        self.temps_preparation = temps_preparation
        self.difficulte = difficulte
        self.type_plat = type_plat
    
    def to_dict(self) -> dict:
        """Convertit la recette en dictionnaire pour le JSON"""
        return {
            "nom": self.nom,
            "ingredients": [ing.to_dict() for ing in self.ingredients],
            "instructions": self.instructions,
            "temps_preparation": self.temps_preparation,
            "difficulte": self.difficulte,
            "type_plat": self.type_plat
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crée une Recette à partir d'un dictionnaire"""
        ingredients = [Ingredient.from_dict(ing) for ing in data["ingredients"]]
        return cls(
            data["nom"],
            ingredients,
            data["instructions"],
            data["temps_preparation"],
            data["difficulte"],
            data["type_plat"]
        )