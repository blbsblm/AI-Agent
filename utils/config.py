import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration centrale de l'application"""
    
    # Validation des variables d'environnement
    @staticmethod
    def _get_env(key, default=None, required=True):
        value = os.getenv(key, default)
        if required and not value:
            raise ValueError(f"La variable {key} est requise dans .env")
        return value
    
    # Configuration Gemini
    GEMINI_API_KEY = _get_env("GEMINI_API_KEY")
    
    # Gestion des données
    DATA_DIR = Path(_get_env("DATA_FOLDER", "data"))
    RECETTES_FILE = _get_env("RECETTES_FILE", "recettes.json")
    RECETTES_PATH = DATA_DIR / RECETTES_FILE
    
    # Initialisation
    @classmethod
    def init(cls):
        cls.DATA_DIR.mkdir(exist_ok=True)
        if not cls.RECETTES_PATH.exists():
            cls.RECETTES_PATH.write_text("[]", encoding="utf-8")