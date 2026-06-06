import asyncio
import os
import platform
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Ajustement de la boucle d'événements pour la compatibilité sous Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Configuration et résolution des chemins du projet
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Chargement des variables d'environnement (.env)
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Importation de la fonction d'exécution de ton agent stratégique LangGraph
from core_agent.f1_strategy_agent import executer_agent_strategie


# --- CONFIGURATION DE LA PAGE STREAMLIT ---
st.set_page_config(
    page_title="PaceOracle | F1 Race Control",
    page_icon="🏎️",
    layout="wide",
)

# --- STYLE CSS PERSONNALISÉ (Thème Pit Wall Carbon) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #e10600 !important; font-family: 'Formula1', sans-serif; font-weight: 800; }
    h3 { color: #ffffff !important; }
    .stButton>button {
        background-color: #e10600 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #b80500 !important;
        box-shadow: 0 4px 15px rgba(225, 6, 0, 0.4);
    }
    .report-box {
        background-color: #161b22;
        border-left: 5px solid #e10600;
        padding: 20px;
        border-radius: 8px;
        color: #f0f6fc;
        font-family: monospace;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)


# --- CONTEXTE ASYNC POUR LE SERVEUR MCP ---
@asynccontextmanager
async def ouvrir_session_mcp():
    """Lance le serveur FastMCP en arrière-plan et initialise la session client."""
    chemin_serveur = APP_DIR / "mcp_server" / "f1_mcp_server.py"
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(chemin_serveur)],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


async def executer_simulation(question_utilisateur: str) -> str:
    """Ouvre la session MCP et exécute le graphe de l'agent."""
    async with ouvrir_session_mcp() as session_mcp:
        return await executer_agent_strategie(session_mcp, question_utilisateur)


def construire_question(circuit: str, gommes: str, tours: int, message: str) -> str:
    """Formate le prompt qui sera envoyé à l'agent LangGraph."""
    base = (
        f"Nous sommes au Grand Prix de {circuit}. Notre pilote roule avec un train "
        f"de pneus {gommes} depuis {tours} tours. Que devons-nous faire stratégiquement pour le prochain tour ?"
    )
    if message.strip():
        return f"{base}\n\nContexte supplémentaire: {message.strip()}"
    return base


# --- LAYOUT DE L'INTERFACE UTILISATEUR ---
st.title("🏎️ PACEORACLE // RACE CONTROL ROOM")
st.caption("Dashboard de stratégie en temps réel • Agent IA LangGraph + RAG Local + Outils MCP")
st.markdown("---")

colonne_gauche, colonne_droite = st.columns([1, 1.2], gap="large")

# --- COLONNE GAUCHE : SAISIE DU PROMPT ET PARAMÈTRES ---
with colonne_gauche:
    st.subheader("🛠️ Paramètres de course")
    
    # Liste des 24 circuits synchronisés avec ton RAG et ton dictionnaire de configuration
    circuit = st.selectbox(
        "Circuit",
        [
            "Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami",
            "Emilia-Romagna", "Monaco", "Canada", "Spain", "Austria", "Great Britain",
            "Hungary", "Belgium", "Netherlands", "Italy", "Azerbaijan", "Singapore",
            "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"
        ],
        index=7,  # Positionné par défaut sur Monaco
    )
    
    col_pneu, col_tours = st.columns(2)
    with col_pneu:
        gommes = st.selectbox("Type de pneus", ["Soft", "Medium", "Hard"], index=2) # Par défaut sur Hard
    with col_tours:
        tours = st.slider("Tours effectués sur ce train", min_value=1, max_value=60, value=14)
    
    contexte = st.text_area(
        "Contexte additionnel (Radio Team / Conditions)",
        placeholder="Ex: position_critique_en_piste, trafic dense à la sortie des stands, pluie prévue...",
        height=120,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    lancer = st.button("🚨 LANCER LA SIMULATION", use_container_width=True)


# --- COLONNE DROITE : RAPPORT DE L'AGENT IA ---
with colonne_droite:
    st.subheader("📊 Résultat & Rapport Stratégique")
    
    # Initialisation de l'état de session pour le rapport
    if "dernier_rapport" not in st.session_state:
        st.session_state.dernier_rapport = ""

    if lancer:
        if "GROQ_API_KEY" not in os.environ:
            st.error("La variable d'environnement GROQ_API_KEY est absente dans ton fichier .env.")
        else:
            # Construction dynamique du prompt à partir des inputs utilisateur
            question = construire_question(circuit, gommes, tours, contexte)
            
            with st.spinner("Appel du RAG, connexion au serveur MCP et calcul de la stratégie..."):
                try:
                    # Gestion de la boucle d'événements asynchrone selon l'environnement d'exécution
                    st.session_state.dernier_rapport = asyncio.run(executer_simulation(question))
                except RuntimeError as erreur_runtime:
                    if "asyncio.run() cannot be called from a running event loop" in str(erreur_runtime):
                        boucle = asyncio.get_event_loop()
                        st.session_state.dernier_rapport = boucle.run_until_complete(executer_simulation(question))
                    else:
                        raise

    # Zone d'affichage stylisée du rapport rendu par LLaMA-3.3-70B
    if st.session_state.dernier_rapport:
        st.markdown(
            f'<div class="report-box">📝 <b>RAPPORT DU STRATÉGISTE :</b>\n\n{st.session_state.dernier_rapport}</div>',
            unsafe_allow_html=True
        )
        st.caption("⚡ Recommandation calculée en croisant tes directives RAG internes et la télémétrie du serveur MCP.")
    else:
        st.info("Ajuste le prompt avec les paramètres de course à gauche, puis lance la simulation pour générer le rapport du muret des stands.")