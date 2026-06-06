import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_mcp_adapters.tools import load_mcp_tools

from core_agent.f1_rag_setup import initialiser_outils_rag

class MCP_State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
def routeur_mcp(state:MCP_State)->str:
    dernier_message=state["messages"][-1]
    if hasattr(dernier_message,"tool_calls") and dernier_message.tool_calls:
        return "executer_outils"
    return "fin"
PROMPT_STRATEGIE = """Tu es l'ingénieur en chef de la stratégie de course (Race Strategist) pour une écurie de Formule 1.
Ton but est de formuler une recommandation stratégique ultra-précise à ton directeur d'équipe concernant l'arrêt aux stands d'un pilote.

Tu as à ta disposition deux types d'outils essentiels :
1. L'outil RAG local 'chercher_directives_ecurie' (Historique, contraintes de sécurité de l'équipe).
2. Les outils MCP distants (Données de circuit, télémétrie d'usure des pneus, coûts des pit-stops).

Méthode de réflexion obligatoire :
- Dès que tu connais le circuit, appelle TOUJOURS 'chercher_directives_ecurie' pour prendre connaissance des contraintes secrètes.
- Appelle ensuite 'obtenir_infos_circuit' et 'simuler_degradation_pneu' pour chiffrer l'état actuel et physique des pneumatiques.
- Calcule la perte dans les stands avec 'calculer_perte_pitstop'.
- Rassemble toutes ces données pour construire ton rapport d'ingénieur. Ne devine rien, base-toi sur les retours des outils.
"""

async def executer_agent_strategie(session_mcp,question_utilisateur:str):
    outil_rag=initialiser_outils_rag()
    outils_mcp=await load_mcp_tools(session_mcp)
    tous_les_outils=outils_mcp+[outil_rag]
    dictionnaire_outils={outil.name:outil for outil in tous_les_outils}
    
    llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.1)
    llm_avec_outils=llm.bind_tools(tous_les_outils)
    
    def noeud_agent(state:MCP_State):
        messages_complets=[SystemMessage(content=PROMPT_STRATEGIE)]+state["messages"]
        reponse=llm_avec_outils.invoke(messages_complets)
        return {"messages":[reponse]}
    
    async def noeud_executeur_outils(state:MCP_State):
        dernier_message=state["messages"][-1]
        messages_retour=[]
        if hasattr(dernier_message,"tool_calls") and dernier_message.tool_calls:
            for tool_call in dernier_message.tool_calls:
                nom_outil=tool_call["name"]
                arguments=tool_call["args"]
                
                if nom_outil in dictionnaire_outils:
                    outil_cible=dictionnaire_outils[nom_outil]
                    resultat=await outil_cible.ainvoke(arguments)
                    messages_retour.append(
                        ToolMessage(content=str(resultat),tool_call_id=tool_call["id"],name=nom_outil)
                    )
                    
        return {"messages":messages_retour}
    builder=StateGraph(MCP_State)
    builder.add_node("agent",noeud_agent)
    builder.add_node("executer_outils",noeud_executeur_outils)
    builder.set_entry_point("agent")
    builder.add_conditional_edges(
        "agent",
        routeur_mcp,
        {
            "executer_outils":"executer_outils",
            "fin":END
        }
    )
    builder.add_edge("executer_outils","agent")
    graphe_final=builder.compile()
    inputs={"messages":[HumanMessage(content=question_utilisateur)]}
    resultat_final=await graphe_final.ainvoke(inputs)
    
    return resultat_final["messages"][-1].content
