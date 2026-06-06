# 🏎️ PaceOracle // F1 Race Control Room

**PaceOracle** est une application d'aide à la décision stratégique en temps réel pour la Formule 1. Elle combine la puissance d'un agent conversationnel avancé (**LangGraph**), d'une base de connaissances locale (**RAG**) contenant les directives secrètes de l'écurie, et d'un moteur de calcul physique distant connecté via le protocole **MCP (Model Context Protocol)**.

L'interface utilisateur est propulsée par **Streamlit** pour offrir un tableau de bord digne d'un véritable muret des stands.

---

## 🏗️ Architecture du Projet

Le projet est découpé en trois briques principales :

├── app.py                      # Interface utilisateur (Streamlit Dashboard)
├── .env                        # Variables d'environnement (Clés d'API)
├── core_agent/
│   ├── f1_rag_setup.py         # Base vectorielle FAISS contenant les directives écurie
│   └── f1_strategy_agent.py    # Agent LangGraph (LLaMA 3.3 70B via Groq)
└── mcp_server/
├── f1_mcp_server.py        # Serveur FastMCP exposant les outils de télémétrie
└── data.py                 # Configuration physique de la saison (circuits, pneus)


### 1. Le Moteur de Calcul (`mcp_server/`)
Un serveur **FastMCP** indépendant qui expose des outils de simulation physique et de configuration pour la saison de F1 :
*   `obtenir_infos_circuit` : Récupère les métadonnées et catégories d'un tracé.
*   `simuler_degradation_pneu` : Calcule l'usure exponentielle d'un pneu, le delta de temps perdu au tour et l'état critique de la gomme.
*   `calculer_perte_pitstop` : Chiffre le coût en secondes d'un passage par la pitlane selon le circuit.
*   `comparer_gomme_depart` : Fournit une analyse comparative de longévité entre les composés.

### 2. Le Cerveau Stratégique (`core_agent/`)
*   **RAG Local (`FAISS`)** : Embarque les 24 directives stratégiques secrètes de l'écurie (ex: à Monaco, interdiction absolue de s'arrêter si l'on ressort dans le trafic, peu importe l'usure).
*   **Agent Intelligent (`LangGraph`)** : Orchestre la réflexion de l'ingénieur de course. Dès qu'un circuit est soumis, l'agent interroge obligatoirement le RAG pour connaître ses contraintes historiques, puis appelle les outils MCP pour chiffrer la télémétrie avant de rendre son verdict.

### 3. Le Muret des Stands (`app.py`)
Une interface **Streamlit** épurée et immersive qui permet à l'ingénieur de configurer le contexte de course (Circuit, type de gomme, nombre de tours du relais en cours, messages radio) et de déclencher la simulation.

---

## 🚀 Installation et Configuration

### 1. Prérequis
Assure-toi d'avoir **Python 3.10 ou supérieur** installé sur ton système.

### 2. Cloner le projet et installer les dépendances
Installe l'ensemble des paquets requis (incluant LangChain, LangGraph, Streamlit, FAISS et les composants MCP) :
```bash
pip install streamlit langchain-groq langgraph langchain-mcp-adapters mcp python-dotenv faiss-cpu langchain-huggingface
3. Configurer les variables d'environnement
Crée un fichier .env à la racine du projet et ajoute ta clé d'API Groq :

Extrait de code
GROQ_API_KEY=tu_as_cle_api_groq_ici
💻 Lancement de l'Application
Pour démarrer le dashboard et l'agent, exécute simplement la commande suivante à la racine du projet :

Bash
streamlit run app.py
L'application va automatiquement :

Configurer la boucle d'événements asynchrone (gestion robuste pour Windows).

Initialiser la base de connaissances RAG locale (Embeddings HuggingFace).

Instancier le serveur MCP en arrière-plan sous forme de sous-processus stdio.

Ouvrir ton navigateur sur l'interface de contrôle (http://localhost:8501).

🛠️ Utilisation
Sélectionne le circuit de ton choix dans le menu déroulant (ex: Monaco).

Configure le relais actuel : choisis le type de pneu (Soft / Medium / Hard) et ajuste le curseur du nombre de tours effectués.

Ajoute du contexte additionnel (Facultatif) dans la zone de texte pour simuler des imprévus radio (ex: position_critique_en_piste, pluie prévue dans 5 tours).

Clique sur 🚨 LANCER LA SIMULATION.

Découvre à droite le Rapport du Stratégiste détaillé rédigé par l'IA, combinant tes règles d'équipe et les calculs physiques du serveur MCP.
