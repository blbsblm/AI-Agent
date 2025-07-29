from typing import List
from models.recette import Recette
from services.data_manager import DataManager
from models.ingredient import Ingredient

class BaseConnaissances:
    """Base de connaissances des recettes culinaires"""
    
    def __init__(self):
        """Initialise avec les recettes par défaut ou depuis JSON"""
        self.data_manager = DataManager()
        self.recettes = self._charger_recettes()
        print(f"Debug: {len(self.recettes)} recettes chargées dans BaseConnaissances")
    
    def _charger_recettes(self) -> List[Recette]:
        """Charge les recettes depuis JSON ou initialise les valeurs par défaut"""
        try:
            donnees = self.data_manager.charger_recettes()
            if not donnees or len(donnees) < 8:  # Reset if fewer than 8 recipes
                print(f"Debug: {len(donnees) if donnees else 0} recettes trouvées dans recettes.json, réinitialisation des recettes par défaut")
                return self._initialiser_recettes_defaut()
            recettes = [Recette.from_dict(d) for d in donnees]
            print(f"Debug: {len(recettes)} recettes chargées depuis recettes.json")
            return recettes
        except Exception as e:
            print(f"Debug: Erreur lors du chargement de recettes.json: {str(e)}, initialisation des recettes par défaut")
            return self._initialiser_recettes_defaut()
    
    def _initialiser_recettes_defaut(self) -> List[Recette]:
        """Retourne les recettes par défaut si la base est vide"""
        recettes_defaut = [
            Recette(
                nom="Pasta Carbonara",
                ingredients=[
                    Ingredient("pâtes", 300, "g"),
                    Ingredient("œufs", 3, "pièces"),
                    Ingredient("bacon", 150, "g"),
                    Ingredient("parmesan", 50, "g")
                ],
                instructions=[
                    "Faire cuire les pâtes dans l'eau bouillante salée",
                    "Faire revenir le bacon dans une poêle",
                    "Battre les œufs avec le parmesan râpé",
                    "Mélanger les pâtes chaudes avec les œufs et le bacon"
                ],
                temps_preparation=20,
                difficulte="Facile",
                type_plat="Plat principal"
            ),
            Recette(
                nom="Salade César",
                ingredients=[
                    Ingredient("laitue romaine", 1, "pièce"),
                    Ingredient("poulet", 200, "g"),
                    Ingredient("parmesan", 30, "g"),
                    Ingredient("croûtons", 50, "g")
                ],
                instructions=[
                    "Laver et couper la laitue",
                    "Griller le poulet et le couper en lamelles",
                    "Mélanger la salade avec la sauce",
                    "Ajouter le poulet, parmesan et croûtons"
                ],
                temps_preparation=15,
                difficulte="Très facile",
                type_plat="Entrée"
            ),
            Recette(
                nom="Tiramisu",
                ingredients=[
                    Ingredient("mascarpone", 500, "g"),
                    Ingredient("œufs", 4, "pièces"),
                    Ingredient("sucre", 100, "g"),
                    Ingredient("café fort", 300, "ml")
                ],
                instructions=[
                    "Séparer les blancs des jaunes d'œufs",
                    "Mélanger jaunes, sucre et mascarpone",
                    "Monter les blancs en neige et incorporer",
                    "Tremper les biscuits dans le café",
                    "Alterner couches de biscuits et crème"
                ],
                temps_preparation=30,
                difficulte="Moyen",
                type_plat="Dessert"
            ),
            Recette(
                nom="Risotto aux Champignons",
                ingredients=[
                    Ingredient("riz arborio", 300, "g"),
                    Ingredient("champignons", 300, "g"),
                    Ingredient("bouillon", 1, "L"),
                    Ingredient("vin blanc", 150, "ml")
                ],
                instructions=[
                    "Faire revenir les champignons",
                    "Faire griller le riz",
                    "Ajouter le vin blanc puis le bouillon louche par louche",
                    "Remuer constamment pendant 18 minutes"
                ],
                temps_preparation=35,
                difficulte="Moyen",
                type_plat="Plat principal"
            ),
            Recette(
                nom="Soupe de Tomates",
                ingredients=[
                    Ingredient("tomates", 800, "g"),
                    Ingredient("oignon", 1, "pièce"),
                    Ingredient("basilic", 10, "feuilles"),
                    Ingredient("crème", 100, "ml")
                ],
                instructions=[
                    "Faire revenir l'oignon",
                    "Ajouter les tomates et le basilic",
                    "Laisser mijoter 20 minutes",
                    "Mixer et ajouter la crème"
                ],
                temps_preparation=25,
                difficulte="Facile",
                type_plat="Entrée"
            ),
            Recette(
                nom="Mousse au Chocolat",
                ingredients=[
                    Ingredient("chocolat noir", 200, "g"),
                    Ingredient("œufs", 6, "pièces"),
                    Ingredient("sucre", 50, "g"),
                    Ingredient("beurre", 50, "g")
                ],
                instructions=[
                    "Faire fondre le chocolat avec le beurre",
                    "Séparer les blancs des jaunes",
                    "Mélanger jaunes avec le chocolat",
                    "Monter les blancs en neige avec le sucre",
                    "Incorporer délicatement"
                ],
                temps_preparation=20,
                difficulte="Moyen",
                type_plat="Dessert"
            ),
            Recette(
                nom="Tarte aux Pommes",
                ingredients=[
                    Ingredient("pâte brisée", 1, "pièce"),
                    Ingredient("pommes", 4, "pièces"),
                    Ingredient("sucre", 80, "g"),
                    Ingredient("cannelle", 1, "c. à thé")
                ],
                instructions=[
                    "Étaler la pâte dans un moule",
                    "Éplucher et couper les pommes",
                    "Disposer les pommes sur la pâte",
                    "Saupoudrer de sucre et cannelle",
                    "Cuire 40 minutes à 180°C"
                ],
                temps_preparation=15,
                difficulte="Facile",
                type_plat="Dessert"
            ),
            Recette(
                nom="Spaghetti Bolognaise",
                ingredients=[
                    Ingredient("spaghetti", 300, "g"),
                    Ingredient("viande hachée", 300, "g"),
                    Ingredient("tomates concassées", 400, "g"),
                    Ingredient("vin rouge", 100, "ml")
                ],
                instructions=[
                    "Faire revenir la viande hachée",
                    "Ajouter les tomates et le vin",
                    "Laisser mijoter 30 minutes",
                    "Cuire les pâtes et servir avec la sauce"
                ],
                temps_preparation=45,
                difficulte="Facile",
                type_plat="Plat principal"
            )
        ]
        print(f"Debug: Sauvegarde de {len(recettes_defaut)} recettes par défaut dans recettes.json")
        self.data_manager.sauvegarder_recettes(recettes_defaut)
        return recettes_defaut
    
    def ajouter_recette(self, recette: Recette):
        """Ajoute une recette et met à jour le JSON"""
        self.recettes.append(recette)
        print(f"Debug: Ajout de la recette '{recette.nom}', total: {len(self.recettes)} recettes")
        self.data_manager.sauvegarder_recettes(self.recettes)
    
    def supprimer_recette(self, nom: str):
        """Supprime une recette et met à jour le JSON"""
        initial_len = len(self.recettes)
        self.recettes = [r for r in self.recettes if r.nom != nom]
        print(f"Debug: Suppression de la recette '{nom}', total après: {len(self.recettes)} recettes")
        self.data_manager.sauvegarder_recettes(self.recettes)
        if len(self.recettes) == 0:
            print("Debug: Base de données vide après suppression, réinitialisation des recettes par défaut")
            self.recettes = self._initialiser_recettes_defaut()
    
    def sauvegarder(self):
        """Sauvegarde toutes les recettes"""
        print(f"Debug: Sauvegarde de {len(self.recettes)} recettes dans recettes.json")
        self.data_manager.sauvegarder_recettes(self.recettes)
    
    def rechercher_par_ingredient(self, ingredient: str) -> List[Recette]:
        """Recherche des recettes contenant un ingrédient"""
        resultats = []
        for recette in self.recettes:
            for ing in recette.ingredients:
                if ingredient.lower() in ing.nom.lower():
                    resultats.append(recette)
                    break
        return resultats
    
    def rechercher_par_type(self, type_plat: str) -> List[Recette]:
        """Recherche des recettes par type de plat"""
        return [r for r in self.recettes if r.type_plat.lower() == type_plat.lower()]
    
    def rechercher_par_difficulte(self, difficulte: str) -> List[Recette]:
        """Recherche des recettes par difficulté"""
        return [r for r in self.recettes if r.difficulte.lower() == difficulte.lower()]