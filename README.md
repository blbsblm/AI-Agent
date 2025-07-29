🍽️ Agent AI Culinaire
Agent AI Culinaire est une application qui utilise Streamlit pour une interface utilisateur interactive, FastAPI pour une API REST, et Google Gemini AI 🤖 pour des suggestions de recettes intelligentes, offrant une expérience culinaire personnalisée et conviviale.

🎯 Fonctionnalités
💬 Chatbot : Discutez avec un chef virtuel via l’IA Gemini pour des idées de recettes ou utilisez des commandes simples pour des recherches spécifiques.
🔍 Recherche : Filtrez les recettes par type (Entrée, Plat principal, Dessert), difficulté, temps de préparation ou ingrédients.
📝 Gestion des recettes : Ajoutez, visualisez ou supprimez des recettes stockées dans data/recettes.json. L’édition passe par suppression et recréation.
📊 Statistiques : Consultez des métriques (ex. : nombre total de recettes, temps moyen) et des graphiques pour les types et difficultés des recettes.
🌐 API : Accédez aux données des recettes via des endpoints FastAPI sur http://localhost:8000 (ex. : /recettes, /chat).

📂 Structure du Projet
AI-Agent/
├── .env                    # 🔑 Variables d’environnement (ex. : GEMINI_API_KEY)
├── app.py                  # 🎨 Interface Streamlit
├── agent.py                # 🧠 Logique principale pour recommandations et IA
├── services/               # 🛠️ Services pour API et gestion des données
│   ├── __init__.py
│   ├── gemini_service.py   # 🤖 Intégration Gemini AI
│   ├── data_manager.py     # 💾 Gestion du fichier JSON
├── models/                 # 📋 Modèles de données pour recettes et ingrédients
│   ├── __init__.py
│   ├── ingredient.py       # 🍎 Classe Ingrédient
│   ├── recette.py          # 🍽️ Classe Recette
│   ├── base_connaissances.py # 📚 Gestion de la base de recettes
├── utils/                  # ⚙️ Utilitaires de configuration
│   ├── __init__.py
│   ├── config.py           # 🔧 Chargement des variables d’environnement
├── data/                   # 🗄️ Base de données des recettes
│   ├── recettes.json       # 📄 Fichier JSON avec 8 recettes par défaut
├── media/                  # 🖼️ Images des diagrammes UML
│   ├── class_diagram.png
│   ├── use_case_diagram.png
├── requirements.txt        # 📦 Dépendances Python

🏛️ Architecture
Modélisation des Données :
Ingredient : Représente un ingrédient avec nom, quantite, et unite, avec sérialisation/désérialisation.
Recette : Définit une recette avec nom, ingredients, instructions, temps_preparation, difficulte, et type_plat.
BaseConnaissances : Gère la base de recettes (recettes.json) avec des méthodes pour ajouter, supprimer et rechercher.


Intégration IA : GeminiService utilise l’API Gemini pour des réponses culinaires créatives, avec gestion des erreurs.
Moteur de Recommandation : Suggests recipes based on ingredients, time, or randomly (in agent.py).
Interface et API :
Interface Streamlit avec quatre onglets : Chatbot 💬, Recherche 🔍, Gestion des recettes 📝, Statistiques 📊.
Serveur FastAPI pour un accès programmatique sur http://localhost:8000.


🚀 Utilisation

💬 Chatbot : Utilisez "Envoyer (IA)" pour des réponses IA (ex. : "Suggère une recette avec poulet") ou "Classique" pour des requêtes par mots-clés (ex. : "recette dessert"). Boutons rapides comme "Surprise IA" 🎲 pour des suggestions instantanées.
🔍 Recherche : Filtrez les recettes par type, difficulté, temps ou ingrédients. Affichez les détails dans des sections déroulantes.
📝 Gestion des recettes : Ajoutez, visualisez ou supprimez des recettes. L’édition nécessite de supprimer et recréer une recette.
📊 Statistiques : Consultez des métriques (ex. : 8 recettes, temps moyen) et des graphiques pour les types et difficultés.
🌐 API : Utilisez des endpoints comme GET /recettes ou POST /chat (voir docs FastAPI).

🍴 Recettes par Défaut

🍝 Pasta Carbonara (Plat principal, Facile, 20 min)
🥗 Salade César (Entrée, Très facile, 15 min)
🍰 Tiramisu (Dessert, Moyen, 30 min)
🍚 Risotto aux Champignons (Plat principal, Moyen, 35 min)
🥣 Soupe de Tomates (Entrée, Facile, 25 min)
🍫 Mousse au Chocolat (Dessert, Moyen, 20 min)
🥧 Tarte aux Pommes (Dessert, Facile, 15 min)
🍝 Spaghetti Bolognaise (Plat principal, Facile, 45 min)

👥 Membres du groupe :

Boualem Belbessai
Youba Bouanani
Mohand Tahar Aroua
