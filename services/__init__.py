"""
Package des services de l'application culinaire

Contient :
- data_manager.py : Gestion persistance des données
- gemini_service.py : Intégration avec l'API Gemini
"""

from .data_manager import DataManager
from .gemini_service import GeminiAIService

__all__ = ['DataManager', 'GeminiAIService']