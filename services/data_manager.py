import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from models.recette import Recette
from utils.config import Config

class DataManager:
    """Gestionnaire central des données JSON"""
    
    def __init__(self):
        Config.init()
        self.file_path = Config.RECETTES_PATH
    
    def _read_json(self) -> List[Dict]:
        """Lecture sécurisée du fichier JSON"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, data: List[Dict]):
        """Écriture sécurisée dans le fichier JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def sauvegarder_recettes(self, recettes: List[Recette]):
        """Sauvegarde toutes les recettes"""
        self._write_json([r.to_dict() for r in recettes])
    
    def charger_recettes(self) -> List[Dict]:
        """Charge toutes les recettes"""
        return self._read_json()