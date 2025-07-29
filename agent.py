from datetime import datetime
import random
from typing import List
from models.base_connaissances import BaseConnaissances
from models.recette import Recette
from services.gemini_service import GeminiAIService

class RecommandationEngine:
    """Moteur de recommandation de recettes"""
    
    def __init__(self, base_connaissances: BaseConnaissances):
        self.base = base_connaissances
    
    def recommander_par_ingredients(self, ingredients_dispo: List[str]) -> List[Recette]:
        """Recommande des recettes basées sur les ingrédients disponibles"""
        scores = {}
        for recette in self.base.recettes:
            score = sum(
                1 for ing in recette.ingredients 
                if any(i.lower() in ing.nom.lower() for i in ingredients_dispo)
            )
            if score > 0:
                scores[recette] = score / len(recette.ingredients)
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    
    def recommander_par_temps(self, temps_max: int) -> List[Recette]:
        """Recommande des recettes selon le temps maximum"""
        return [r for r in self.base.recettes if r.temps_preparation <= temps_max]
    
    def recommander_aleatoire(self) -> Recette:
        """Retourne une recette aléatoire"""
        if self.base.recettes:
            random.seed()
            return random.choice(self.base.recettes)
        return None

class AgentCulinaire:
    """Agent intelligent pour l'assistance culinaire"""
    
    def __init__(self):
        self.base_connaissances = BaseConnaissances()
        self.moteur_recommandation = RecommandationEngine(self.base_connaissances)
        self.gemini_service = GeminiAIService()
    
    def traiter_requete(self, requete: str) -> str:
        """Traite les requêtes simples basées sur des mots-clés"""
        requete = requete.lower().strip()
        
        if "bonjour" in requete or "salut" in requete:
            return "🤖 Bonjour ! Je suis votre assistant culinaire. Comment puis-je vous aider aujourd'hui ?"
        
        elif "recommande" in requete or "suggère" in requete:
            if "rapide" in requete:
                recettes = self.moteur_recommandation.recommander_par_temps(20)
                if recettes:
                    random.seed(datetime.now().microsecond)
                    recette_choisie = random.choice(recettes)
                    return f"🏃‍♂️ Voici une recette rapide : **{recette_choisie.nom}** ({recette_choisie.temps_preparation} min)"
                return "😔 Aucune recette rapide disponible"
            else:
                random.seed(datetime.now().microsecond)
                recette = self.moteur_recommandation.recommander_aleatoire()
                if recette:
                    return f"🎲 Je vous recommande : **{recette.nom}** ({recette.type_plat}, {recette.temps_preparation} min)"
                return "😔 Aucune recette disponible"
        
        elif "ingrédient" in requete:
            mots = requete.split()
            if len(mots) > 1:
                ingredient = mots[-1]
                recettes = self.base_connaissances.rechercher_par_ingredient(ingredient)
                if recettes:
                    return f"🔍 Recettes avec {ingredient} : " + ", ".join([r.nom for r in recettes[:3]])
                return f"😔 Aucune recette trouvée avec {ingredient}"
            return "Veuillez préciser un ingrédient"
        
        elif "dessert" in requete:
            recettes = self.base_connaissances.rechercher_par_type("Dessert")
            if recettes:
                random.shuffle(recettes)
                return f"🍰 Desserts disponibles : " + ", ".join([r.nom for r in recettes])
            return "😔 Aucun dessert disponible"
        
        elif "entrée" in requete:
            recettes = self.base_connaissances.rechercher_par_type("Entrée")
            if recettes:
                random.shuffle(recettes)
                return f"🥗 Entrées disponibles : " + ", ".join([r.nom for r in recettes])
            return "😔 Aucune entrée disponible"
        
        elif "plat" in requete:
            recettes = self.base_connaissances.rechercher_par_type("Plat principal")
            if recettes:
                random.shuffle(recettes)
                return f"🍽️ Plats principaux : " + ", ".join([r.nom for r in recettes])
            return "😔 Aucun plat principal disponible"
        
        elif "facile" in requete:
            recettes = self.base_connaissances.rechercher_par_difficulte("Facile")
            if recettes:
                return f"👨‍🍳 Recettes faciles : " + ", ".join([r.nom for r in recettes])
            return "😔 Aucune recette facile disponible"
        
        elif "aide" in requete or "help" in requete:
            return """
            🆘 **Commandes disponibles :**
            • "Recommande-moi une recette" - Suggestion aléatoire
            • "Recommande quelque chose de rapide" - Recette rapide
            • "Recettes avec [ingrédient]" - Recherche par ingrédient
            • "Montre-moi les desserts" - Recettes de dessert
            • "Recettes faciles" - Recettes par difficulté
            """
        
        else:
            return "🤖 Je n'ai pas compris votre demande. Tapez 'aide' pour voir les commandes disponibles."
    
    async def traiter_requete_ia(self, requete: str) -> str:
        """Utilise Gemini pour les requêtes complexes"""
        recettes_context = ""
        for recette in self.base_connaissances.recettes:
            recettes_context += f"- {recette.nom} ({recette.type_plat}, {recette.difficulte}, {recette.temps_preparation}min)\n"
        return await self.gemini_service.generer_reponse_culinaire(requete, recettes_context)