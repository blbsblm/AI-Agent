import google.generativeai as genai
import asyncio
from typing import List  # Added to fix NameError
from utils.config import Config

class GeminiAIService:
    """Service d'intégration avec l'API Gemini de Google"""
    
    def __init__(self):
        """Initialise le modèle Gemini"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except:
                try:
                    self.model = genai.GenerativeModel('models/gemini-1.5-flash')
                except:
                    self.model = None
                    print("❌ Aucun modèle Gemini disponible")
    
    async def generer_reponse_culinaire(self, requete: str, recettes_context: str = "") -> str:
        """Génère une réponse culinaire en utilisant Gemini"""
        if self.model is None:
            return "❌ Modèle Gemini non disponible. Vérifiez votre clé API et la connexion internet."
        
        try:
            prompt = f"""
            Tu es un assistant culinaire expert, passionné et créatif. Tu dois répondre de manière naturelle et conversationnelle.
            
            CONTEXTE - Recettes disponibles dans la base de données:
            {recettes_context}
            
            QUESTION DE L'UTILISATEUR: {requete}
            
            INSTRUCTIONS IMPORTANTES:
            - Réponds TOUJOURS en français
            - Sois naturel, amical et enthousiaste
            - Si la question concerne une recette spécifique de la base, utilise ces informations
            - Si la question est générale sur la cuisine, donne des conseils créatifs et pratiques
            - Pour les recommandations, sois créatif et propose des idées originales
            - Utilise des emojis pour rendre tes réponses plus engageantes
            - Adapte ton ton à la question (conseil, recette, technique, etc.)
            - Si tu ne trouves pas d'info dans la base, propose des alternatives créatives
            - Évite les réponses trop longues, reste concis mais informatif
            
            Réponds comme un vrai chef cuisinier passionné qui adore partager ses connaissances !
            """
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return """❌ **Erreur de modèle Gemini**
                
🔧 **Solutions possibles :**
1. Vérifiez que votre clé API Gemini est valide
2. Assurez-vous d'avoir accès aux modèles Gemini 1.5
3. Vérifiez votre connexion internet
4. La clé API doit avoir les permissions pour Gemini

💡 **Modèles testés :** gemini-1.5-flash, gemini-1.5-pro"""
            return f"🤖 Erreur technique: {error_msg}\n\n💡 Vérifiez votre configuration Gemini."
    
    async def suggerer_recette_ia(self, ingredients: List[str] = None, preferences: str = "") -> str:
        """Suggère une recette originale via Gemini"""
        if self.model is None:
            return "❌ Modèle Gemini non disponible"
        
        try:
            prompt = f"""
            Tu es un chef cuisinier créatif. Crée une suggestion de recette originale.
            
            Ingrédients disponibles: {', '.join(ingredients) if ingredients else 'Aucun spécifié'}
            Préférences: {preferences}
            
            Crée une suggestion courte et attrayante avec:
            - Nom de la recette
            - Temps de préparation estimé
            - Niveau de difficulté
            - Une phrase d'accroche appétissante
            
            Format: 🍽️ **Nom** (Temps min, Difficulté) - Description courte
            """
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text
        except Exception as e:
            return "🤖 Impossible de générer une suggestion pour le moment."