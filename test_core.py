# test_core.py
import asyncio
import os
import sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from dotenv import load_dotenv
# Importation directe de ton agent fraîchement codé
from core_agent.f1_strategy_agent import executer_agent_strategie
load_dotenv()

async def lancer_test_integration():
    print("====== 🏎️ TEST D'INTÉGRATION DU STRATEGY AGENT ======")
    
    # 1. Vérification de la clé API Groq
    if "GROQ_API_KEY" not in os.environ:
        print("❌ Erreur : La variable d'environnement 'GROQ_API_KEY' est absente.")
        print("👉 Lance la commande : export GROQ_API_KEY='ta_cle_ici'")
        return

    # 2. Configuration des paramètres pour lancer ton serveur MCP en arrière-plan
    chemin_serveur = os.path.abspath("mcp_server/f1_mcp_server.py")
    if not os.path.exists(chemin_serveur):
        print(f"❌ Erreur : Le fichier serveur introuvable à l'emplacement : {chemin_serveur}")
        return

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[chemin_serveur]
    )
    
    print("🚀 Démarrage et connexion au serveur MCP PaceOracle...")
    
    try:
        # 3. Connexion au serveur MCP via les flux standards (Subprocess)
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialisation du protocole MCP
                await session.initialize()
                print("✅ Connecté au serveur MCP avec succès.")
                
                # 4. Scénario de test : Un cas critique à Spa-Francorchamps
                scenario_prompt = (
                    "Nous sommes au Grand Prix de Belgique. Notre pilote roule avec un train "
                    "de pneus Soft depuis 13 tours. Que devons-nous faire stratégiquement pour le prochain tour ?"
                )
                
                print(f"\n💬 Situation soumise à l'agent :\n{scenario_prompt}\n")
                print("🧠 LLaMA analyse la situation (RAG local + Outils MCP)...")
                print("-" * 60)
                
                # 5. Appel de ton agent LangGraph
                rapport_strategique = await executer_agent_strategie(session, scenario_prompt)
                
                print("\n📊 [RECOMMANDATION DE L'INGÉNIEUR DE COURSE] :")
                print(rapport_strategique)
                print("-" * 60)
                
    except Exception as e:
        print(f"❌ Une erreur est survenue durant le test : {e}")

if __name__ == "__main__":
    # Exécution de la boucle asynchrone
    asyncio.run(lancer_test_integration())