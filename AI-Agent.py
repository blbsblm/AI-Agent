# -*- coding: utf-8 -*-
"""
Interface Streamlit pour l'Agent AI Culinaire avec intégration Gemini AI
Langage: Python 3.x
"""

import streamlit as st
import json
import random
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import threading
import uvicorn
from contextlib import asynccontextmanager

# Configuration Gemini AI
GEMINI_API_KEY = "AIzaSyAF1VlUMnm6fH431zmvW_JZQ86CReIB_lk"  # Remplacez par votre clé API Gemini

# Vérification de la clé API
if GEMINI_API_KEY == "VOTRE_CLE_API_GEMINI_ICI":
    st.error("⚠️ **ATTENTION**: Veuillez configurer votre clé API Gemini dans le code (ligne 15)")
    st.info("📝 Instructions: Remplacez 'VOTRE_CLE_API_GEMINI_ICI' par votre vraie clé API Gemini")

genai.configure(api_key=GEMINI_API_KEY)

# Configuration de la page Streamlit
st.set_page_config(
    page_title="🤖 Agent AI Culinaire",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class Ingredient:
    def __init__(self, nom: str, quantite: float, unite: str):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite
    
    def __str__(self):
        return f"{self.quantite} {self.unite} de {self.nom}"
    
    def to_dict(self):
        return {"nom": self.nom, "quantite": self.quantite, "unite": self.unite}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["nom"], data["quantite"], data["unite"])

class Recette:
    def __init__(self, nom: str, ingredients: List[Ingredient], 
                 instructions: List[str], temps_preparation: int, 
                 difficulte: str, type_plat: str):
        self.nom = nom
        self.ingredients = ingredients
        self.instructions = instructions
        self.temps_preparation = temps_preparation
        self.difficulte = difficulte
        self.type_plat = type_plat
    
    def to_dict(self):
        return {
            "nom": self.nom,
            "ingredients": [ing.to_dict() for ing in self.ingredients],
            "instructions": self.instructions,
            "temps_preparation": self.temps_preparation,
            "difficulte": self.difficulte,
            "type_plat": self.type_plat
        }
    
    @classmethod
    def from_dict(cls, data):
        ingredients = [Ingredient.from_dict(ing) for ing in data["ingredients"]]
        return cls(
            data["nom"], ingredients, data["instructions"],
            data["temps_preparation"], data["difficulte"], data["type_plat"]
        )