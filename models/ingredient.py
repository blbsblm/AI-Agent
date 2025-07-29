class Ingredient:
    """Modèle représentant un ingrédient culinaire"""
    
    def __init__(self, nom: str, quantite: float, unite: str):
        """
        Initialise un nouvel ingrédient
        :param nom: Nom de l'ingrédient (ex: "tomate")
        :param quantite: Quantité nécessaire (ex: 2)
        :param unite: Unité de mesure (ex: "pièces")
        """
        self.nom = nom
        self.quantite = quantite
        self.unite = unite
    
    def __str__(self):
        """Formatage pour l'affichage (ex: '2 pièces de tomate')"""
        return f"{self.quantite} {self.unite} de {self.nom}"
    
    def to_dict(self) -> dict:
        """Convertit l'ingrédient en dictionnaire pour le JSON"""
        return {
            "nom": self.nom,
            "quantite": self.quantite,
            "unite": self.unite
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crée un Ingredient à partir d'un dictionnaire"""
        return cls(data["nom"], data["quantite"], data["unite"])