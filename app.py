import streamlit as st
import asyncio
import json
import random
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import threading
import uvicorn
from contextlib import asynccontextmanager
from agent import AgentCulinaire
from models.recette import Recette
from models.ingredient import Ingredient

# Configuration de la page Streamlit
st.set_page_config(
    page_title="🤖 Agent AI Culinaire",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Démarrage du serveur FastAPI pour l'Agent AI Culinaire")
    yield
    print("🛑 Arrêt du serveur FastAPI")

app = FastAPI(
    title="Agent AI Culinaire API",
    description="API pour l'agent culinaire avec IA Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Instance globale de l'agent
agent_global = AgentCulinaire()

@app.post("/chat")
async def chat_endpoint(request: dict):
    try:
        response_ia = await agent_global.traiter_requete_ia(request.get("message", ""))
        suggestion = await agent_global.gemini_service.suggerer_recette_ia(
            ingredients=request.get("ingredients", []),
            preferences=request.get("context", "")
        )
        return {"response": response_ia, "suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recettes")
async def get_recettes():
    return [recette.to_dict() for recette in agent_global.base_connaissances.recettes]

@app.get("/recettes/type/{type_plat}")
async def get_recettes_by_type(type_plat: str):
    recettes = agent_global.base_connaissances.rechercher_par_type(type_plat)
    return [recette.to_dict() for recette in recettes]

# Fonction pour démarrer FastAPI en arrière-plan
def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# Démarrage automatique de FastAPI en arrière-plan
if 'fastapi_started' not in st.session_state:
    st.session_state.fastapi_started = True
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

# Initialisation de l'agent
if 'agent' not in st.session_state:
    st.session_state.agent = AgentCulinaire()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Interface principale
st.title("🤖 Agent AI Culinaire")
st.markdown("### Votre assistant intelligent pour la cuisine")

# Sidebar pour navigation
with st.sidebar:
    st.header("🧭 Navigation")
    page = st.selectbox(
        "Choisissez une section",
        ["💬 Chatbot", "🔍 Recherche", "📚 Gestion des recettes", "📊 Statistiques"]
    )

# Page Chatbot
if page == "💬 Chatbot":
    st.header("💬 Chatbot Culinaire")
    
    chat_container = st.container()
    
    with chat_container:
        for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
            st.markdown(f"**Vous:** {user_msg}")
            st.markdown(f"**🤖 Assistant:** {bot_msg}")
            st.markdown("---")
    
    user_input = st.text_input("💬 Tapez votre message ici...", key="chat_input")
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("📤 Envoyer (IA)"):
            if user_input:
                try:
                    response = asyncio.run(st.session_state.agent.traiter_requete_ia(user_input))
                    st.session_state.chat_history.append((user_input, f"🤖 IA: {response}"))
                except Exception as e:
                    response = f"❌ Erreur IA: {str(e)}"
                    st.session_state.chat_history.append((user_input, response))
                st.rerun()
    
    with col2:
        if st.button("📤 Classique"):
            if user_input:
                response = st.session_state.agent.traiter_requete(user_input)
                st.session_state.chat_history.append((user_input, f"🔧 Classique: {response}"))
                st.rerun()
    
    with col3:
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.info("💡 **Mode IA activé par défaut** - Utilisez 'Envoyer (IA)' pour des réponses intelligentes ou 'Classique' pour les commandes spécifiques")
    
    st.markdown("### 🚀 Suggestions rapides")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎲 Surprise IA"):
            try:
                response = asyncio.run(st.session_state.agent.traiter_requete_ia("Suggère-moi une recette originale et créative"))
                st.session_state.chat_history.append(("Surprise IA", f"🤖 IA: {response}"))
            except Exception as e:
                response = f"❌ Erreur IA: {str(e)}"
                st.session_state.chat_history.append(("Surprise IA", response))
            st.rerun()
    
    with col2:
        if st.button("⚡ Rapide IA"):
            try:
                response = asyncio.run(st.session_state.agent.traiter_requete_ia("Donne-moi une recette rapide et facile à faire"))
                st.session_state.chat_history.append(("Recette rapide IA", f"🤖 IA: {response}"))
            except Exception as e:
                response = f"❌ Erreur IA: {str(e)}"
                st.session_state.chat_history.append(("Recette rapide IA", response))
            st.rerun()
    
    with col3:
        if st.button("🍰 Dessert IA"):
            try:
                response = asyncio.run(st.session_state.agent.traiter_requete_ia("Propose-moi un dessert original et délicieux"))
                st.session_state.chat_history.append(("Dessert IA", f"🤖 IA: {response}"))
            except Exception as e:
                response = f"❌ Erreur IA: {str(e)}"
                st.session_state.chat_history.append(("Dessert IA", response))
            st.rerun()
    
    with col4:
        if st.button("🥘 Conseil Chef"):
            try:
                response = asyncio.run(st.session_state.agent.traiter_requete_ia("Donne-moi un conseil de chef professionnel pour améliorer ma cuisine"))
                st.session_state.chat_history.append(("Conseil Chef", f"🤖 IA: {response}"))
            except Exception as e:
                response = f"❌ Erreur IA: {str(e)}"
                st.session_state.chat_history.append(("Conseil Chef", response))
            st.rerun()

# Page Recherche
elif page == "🔍 Recherche":
    st.header("🔍 Recherche de Recettes")
    
    # Debug: Display total recipes and their names
    recettes = st.session_state.agent.base_connaissances.recettes
    st.write(f"**Debug**: {len(recettes)} recettes chargées depuis la base de données")
    st.write("**Noms des recettes**: " + ", ".join([r.nom for r in recettes]))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        type_filtre = st.selectbox(
            "Type de plat",
            ["Tous", "Entrée", "Plat principal", "Dessert"],
            index=0  # Default to "Tous"
        )
    
    with col2:
        difficulte_filtre = st.selectbox(
            "Difficulté",
            ["Toutes", "Très facile", "Facile", "Moyen", "Difficile"],
            index=0  # Default to "Toutes"
        )
    
    with col3:
        temps_max = st.slider("Temps max (min)", 5, 180, 180)  # Default to max to show all
    
    ingredient_recherche = st.text_input("🔍 Rechercher par ingrédient")
    
    recettes_filtrees = st.session_state.agent.base_connaissances.recettes
    
    if type_filtre != "Tous":
        recettes_filtrees = [r for r in recettes_filtrees if r.type_plat == type_filtre]
    
    if difficulte_filtre != "Toutes":
        recettes_filtrees = [r for r in recettes_filtrees if r.difficulte == difficulte_filtre]
    
    recettes_filtrees = [r for r in recettes_filtrees if r.temps_preparation <= temps_max]
    
    if ingredient_recherche:
        recettes_filtrees = [r for r in recettes_filtrees 
                           if any(ingredient_recherche.lower() in ing.nom.lower() 
                                 for ing in r.ingredients)]
    
    st.markdown(f"### 📋 Résultats ({len(recettes_filtrees)} recettes)")
    
    for recette in recettes_filtrees:
        with st.expander(f"🍽️ {recette.nom} ({recette.temps_preparation} min)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Type:** {recette.type_plat}")
                st.markdown(f"**Difficulté:** {recette.difficulte}")
                st.markdown(f"**Temps:** {recette.temps_preparation} minutes")
                
                st.markdown("**Ingrédients:**")
                for ing in recette.ingredients:
                    st.markdown(f"• {ing}")
            
            with col2:
                st.markdown("**Instructions:**")
                for i, instruction in enumerate(recette.instructions, 1):
                    st.markdown(f"{i}. {instruction}")

# Page Gestion des recettes
elif page == "📚 Gestion des recettes":
    st.header("📚 Gestion des Recettes")
    
    tab1, tab2, tab3 = st.tabs(["➕ Ajouter", "📝 Modifier", "🗑️ Supprimer"])
    
    with tab1:
        st.subheader("➕ Ajouter une nouvelle recette")
        
        with st.form("nouvelle_recette"):
            nom = st.text_input("Nom de la recette")
            type_plat = st.selectbox("Type", ["Entrée", "Plat principal", "Dessert"])
            difficulte = st.selectbox("Difficulté", ["Très facile", "Facile", "Moyen", "Difficile"])
            temps = st.number_input("Temps de préparation (min)", min_value=1, value=30)
            
            st.markdown("**Ingrédients:**")
            nb_ingredients = st.number_input("Nombre d'ingrédients", min_value=1, value=3)
            
            ingredients = []
            for i in range(nb_ingredients):
                col1, col2, col3 = st.columns(3)
                with col1:
                    nom_ing = st.text_input(f"Ingrédient {i+1}", key=f"ing_nom_{i}")
                with col2:
                    qty = st.number_input(f"Quantité {i+1}", min_value=0.1, value=1.0, key=f"ing_qty_{i}")
                with col3:
                    unite = st.text_input(f"Unité {i+1}", value="g", key=f"ing_unit_{i}")
                
                if nom_ing:
                    ingredients.append(Ingredient(nom_ing, qty, unite))
            
            st.markdown("**Instructions:**")
            instructions_text = st.text_area("Instructions (une par ligne)")
            instructions = [inst.strip() for inst in instructions_text.split('\n') if inst.strip()]
            
            if st.form_submit_button("➕ Ajouter la recette"):
                if nom and ingredients and instructions:
                    nouvelle_recette = Recette(nom, ingredients, instructions, temps, difficulte, type_plat)
                    st.session_state.agent.base_connaissances.ajouter_recette(nouvelle_recette)
                    st.session_state.agent.base_connaissances.sauvegarder()
                    st.success(f"✅ Recette '{nom}' ajoutée avec succès!")
                else:
                    st.error("❌ Veuillez remplir tous les champs obligatoires")
    
    with tab2:
        st.subheader("📝 Modifier une recette")
        
        recettes_noms = [r.nom for r in st.session_state.agent.base_connaissances.recettes]
        if recettes_noms:
            recette_selectionnee = st.selectbox("Choisir une recette", recettes_noms)
            
            recette = next(r for r in st.session_state.agent.base_connaissances.recettes 
                          if r.nom == recette_selectionnee)
            
            st.markdown("**Détails actuels:**")
            st.json(recette.to_dict())
            
            st.info("💡 Pour modifier une recette, supprimez-la et recréez-la avec les nouvelles informations.")
        else:
            st.info("Aucune recette disponible pour modification")
    
    with tab3:
        st.subheader("🗑️ Supprimer une recette")
        
        recettes_noms = [r.nom for r in st.session_state.agent.base_connaissances.recettes]
        if recettes_noms:
            recette_a_supprimer = st.selectbox("Choisir une recette à supprimer", recettes_noms)
            
            if st.button("🗑️ Supprimer", type="secondary"):
                st.session_state.agent.base_connaissances.supprimer_recette(recette_a_supprimer)
                st.session_state.agent.base_connaissances.sauvegarder()
                st.success(f"✅ Recette '{recette_a_supprimer}' supprimée!")
                st.rerun()
        else:
            st.info("Aucune recette disponible pour suppression")

# Page Statistiques
elif page == "📊 Statistiques":
    st.header("📊 Statistiques des Recettes")
    
    recettes = st.session_state.agent.base_connaissances.recettes
    
    if recettes:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total recettes", len(recettes))
        
        with col2:
            temps_moyen = sum(r.temps_preparation for r in recettes) / len(recettes)
            st.metric("Temps moyen", f"{temps_moyen:.0f} min")
        
        with col3:
            types = [r.type_plat for r in recettes]
            type_populaire = max(set(types), key=types.count)
            st.metric("Type populaire", type_populaire)
        
        with col4:
            difficultes = [r.difficulte for r in recettes]
            diff_populaire = max(set(difficultes), key=difficultes.count)
            st.metric("Difficulté populaire", diff_populaire)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Répartition par type")
            type_counts = {}
            for r in recettes:
                type_counts[r.type_plat] = type_counts.get(r.type_plat, 0) + 1
            
            df_types = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Nombre'])
            st.bar_chart(df_types.set_index('Type'))
        
        with col2:
            st.subheader("📈 Répartition par difficulté")
            diff_counts = {}
            for r in recettes:
                diff_counts[r.difficulte] = diff_counts.get(r.difficulte, 0) + 1
            
            df_diff = pd.DataFrame(list(diff_counts.items()), columns=['Difficulté', 'Nombre'])
            st.bar_chart(df_diff.set_index('Difficulté'))
        
        st.subheader("📋 Tableau détaillé")
        data = []
        for r in recettes:
            data.append({
                'Nom': r.nom,
                'Type': r.type_plat,
                'Difficulté': r.difficulte,
                'Temps (min)': r.temps_preparation,
                'Nb ingrédients': len(r.ingredients)
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    else:
        st.info("Aucune recette disponible pour les statistiques")

# Footer avec informations sur l'API
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            🤖 Agent AI Culinaire - Développé avec Streamlit & Gemini AI
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            🚀 API FastAPI disponible sur http://localhost:8000
        </div>
        """,
        unsafe_allow_html=True
    )