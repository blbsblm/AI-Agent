# 🍽️ Agent AI Culinaire

**Agent AI Culinaire** est une application intelligente qui combine **Streamlit** (interface utilisateur), **FastAPI** (API REST) et **Google Gemini AI 🤖** pour proposer des suggestions de recettes personnalisées dans une interface conviviale et interactive.

---

## 📌 Sommaire

- 🎯 [Fonctionnalités](#fonctionnalités)  
- 🏗️ [Architecture du Projet](#architecture-du-projet)  
- 🧠 [Modélisation et IA](#modélisation-et-ia)  
- 🚀 [Utilisation](#utilisation)  
- 🍴 [Recettes par Défaut](#recettes-par-défaut)  
- 👥 [Membres du Groupe](#membres-du-groupe)

---

## 🎯 Fonctionnalités

- 💬 **Chatbot IA** : Dialogue avec un chef virtuel via Gemini pour obtenir des idées de recettes ou poser des questions spécifiques.  
- 🔍 **Recherche de recettes** : Filtrage par type (entrée, plat principal, dessert), difficulté, temps ou ingrédients.  
- 📝 **Gestion des recettes** : Ajouter, afficher, ou supprimer des recettes dans `recettes.json`. L’édition se fait en supprimant puis en recréant.  
- 📊 **Statistiques visuelles** : Visualisation du nombre de recettes, temps moyen de préparation, graphiques par type et difficulté.  
- 🌐 **API REST (FastAPI)** : Accès aux données via des endpoints (http://localhost:8000).

---

## 🏗️ Architecture du Projet

Voici la structure principale du dossier `AI-Agent/` :

```plaintext
AI-Agent/
├── .env                      → Clé API (GEMINI_API_KEY)
├── app.py                   → Interface Streamlit
├── agent.py                 → Logique de recommandation
├── services/
│   ├── gemini_service.py    → Intégration avec Gemini AI
│   └── data_manager.py      → Gestion des recettes JSON
├── models/
│   ├── ingredient.py        → Classe Ingrédient
│   ├── recette.py           → Classe Recette
│   └── base_connaissances.py→ Accès à la base de données
├── utils/
│   └── config.py            → Chargement des variables d’environnement
├── data/
│   └── recettes.json        → Recettes par défaut
├── requirements.txt         → Dépendances Python
```


## 🧠 Modélisation et IA

### 📋 Modèles de Données

- `Ingredient` : nom, quantité, unité, avec fonctions de sérialisation.
- `Recette` : nom, liste d’ingrédients, instructions, temps de préparation, difficulté, type de plat.
- `BaseConnaissances` : interface pour rechercher, ajouter, supprimer des recettes dans le fichier JSON.

### 🤖 Intégration IA

- `GeminiService` : envoie des requêtes à l’API Gemini pour obtenir des suggestions ou des réponses.
- `agent.py` : moteur de recommandation intelligent selon les ingrédients, le temps disponible ou au hasard.

---

## 🚀 Utilisation

### 💬 Chatbot

- **Mode IA** : Cliquez sur "Envoyer (IA)" et tapez des requêtes comme :  
  `Suggère une recette avec du poulet`
- **Mode classique** : Recherchez par mots-clés :  
  `recette dessert`, `pâtes`, etc.
- **Raccourcis** : Boutons comme "Surprise IA 🎲" pour générer une recette aléatoire.

### 🔍 Recherche

- Filtrage multiple (type, difficulté, temps, ingrédients).
- Affichage détaillé et dynamique (sections déroulantes).

### 📝 Gestion des Recettes

- Ajout via formulaire interactif.
- Suppression directe (aucune édition en place).
- Les données sont stockées dans `data/recettes.json`.

### 📊 Statistiques

- Nombre total de recettes
- Temps moyen de préparation
- Graphiques générés dynamiquement par catégorie

---

## 🍴 Recettes par Défaut

| Nom                      | Type           | Difficulté   | Temps    |
|--------------------------|----------------|--------------|----------|
| 🍝 Pasta Carbonara       | Plat principal | Facile       | 20 min   |
| 🥗 Salade César          | Entrée         | Très facile  | 15 min   |
| 🍰 Tiramisu              | Dessert        | Moyen        | 30 min   |
| 🍚 Risotto Champignons   | Plat principal | Moyen        | 35 min   |
| 🥣 Soupe de Tomates      | Entrée         | Facile       | 25 min   |
| 🍫 Mousse au Chocolat    | Dessert        | Moyen        | 20 min   |
| 🥧 Tarte aux Pommes      | Dessert        | Facile       | 15 min   |
| 🍝 Spaghetti Bolognaise  | Plat principal | Facile       | 45 min   |

---

## 👥 Membres du Groupe

- **Boualem Belbessai**
- **Youba Bouanani**
- **Mohand Tahar Aroua**


