from mcp.server.fastmcp import FastMCP
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

mcp=FastMCP("mcp_f1_predictor")
from data import F1_SEASON_2024_CONFIG
@mcp.tool()
def obtenir_infos_circuit(circuit:str)->str:
    """Retourne les informations clés du circuit demandé."""
    nom_propre=circuit.strip().title()
    if nom_propre not in F1_SEASON_2024_CONFIG:
        return f"Erreur : Circuit '{circuit}' non trouvé dans la configuration."
    infos=F1_SEASON_2024_CONFIG[nom_propre]
    return f"🏁 [{infos['code']}] Grand Prix : {nom_propre} - Catégorie : {infos['category']}"
@mcp.tool()
def simuler_degradation_pneu(circuit:str,type_gomme:str,tours_effectues:int)->str:
    """Simule la degradation des npeus en focntion du nombre de tours effectues ,du type de gomme et du circuit"""
    c_name=circuit.strip().title()
    g_name=type_gomme.strip().title()
    if c_name not in F1_SEASON_2024_CONFIG:
        return f"Erreur : Circuit '{circuit}' non trouvé dans la configuration."
    cfg=F1_SEASON_2024_CONFIG[c_name]
    if g_name not in cfg["compounds"]:
        return f"Erreur : Type de gomme '{type_gomme}' non disponible pour le circuit '{circuit}'."
    limite_theorique=cfg["tyre_limits"][g_name]
    facteur_circuit=cfg["wear_factor"]
    usure_base= (tours_effectues / limite_theorique) *(1/facteur_circuit)
    
    usure_pourcent = 100 * (1 / (1 + math.exp(-5 * (usure_base - 0.7))))
    usure_pourcent = min(100.0, max(0.0, round(usure_pourcent, 1)))
    perte_rythme = round((usure_pourcent / 100) **2.5*3.0,2)
    statut = "🟢 OK" if usure_pourcent < 45 else ("⚠️ ATTENTION" if usure_pourcent < 70 else "🚨 CRITIQUE (Cliff)")
    return (
        f"📊 [Simulation Télémétrie {cfg['code']}]\n"
        f"• Gomme : {g_name} après {tours_effectues} tours\n"
        f"• Usure calculée : {usure_pourcent}%\n"
        f"• Perte de performance au tour : +{perte_rythme}s\n"
        f"• Statut pneu : {statut}"
    )
    
@mcp.tool()
def calculer_perte_pitstop(circuit:str,nombre_arrets:int=1)->str:
    """
    Calcule le temps total perdu dans la voie des stands pour une stratégie donnée.
    Arguments :
        circuit : Nom du pays (ex: 'Japan')
        nombre_arrets : Le nombre d'arrêts prévus dans la stratégie (int, par défaut 1)
    """
    nom_propre=circuit.strip().title()
    if nom_propre not in F1_SEASON_2024_CONFIG:
        return f"Erreur : Circuit '{circuit}' non trouvé dans la configuration."
    cfg=F1_SEASON_2024_CONFIG[nom_propre]
    perte_par_arret=cfg["pit_loss"]
    perte_totale=round(perte_par_arret*nombre_arrets,2)
    return (
        f"⏱️ [Analyse Pitlane - {nom_propre}]\n"
        f"• Coût d'un arrêt unique : {perte_par_arret}s\n"
        f"• Nombre d'arrêts analysés : {nombre_arrets}\n"
        f"• Temps total perdu sur la course : {perte_totale} secondes."
    )
    
@mcp.tool()
def comparer_gomme_depart(circuit:str)->str:
    """
    Compare les avantages et inconvénients de partir en Hard vs Soft sur un circuit donné.
    Arguments :
        circuit : Nom du pays (ex: 'Japan')
    """
    nom_propre=circuit.strip().title()
    if nom_propre not in F1_SEASON_2024_CONFIG:
        return f"Erreur : Circuit '{circuit}' non trouvé dans la configuration."
    cfg=F1_SEASON_2024_CONFIG[nom_propre]
    medium_limite=cfg["tyre_limits"]["Hard"]
    soft_limite=cfg["tyre_limits"]["Soft"]
    ratio=round(medium_limite/soft_limite,2)
    conseil = "Stratégie agressive (Soft) possible si position sur la grille cruciale."
    if ratio > 1.5 and cfg['wear_factor'] < 0.90:
        conseil = "Départ en Medium impératif. Les Softs s'effondreront trop vite sur ce tracé exigeant."
        
    return (
        f"⚖️ [Comparatif Départ - {nom_propre}]\n"
        f"• Durée Soft max : {cfg['tyre_limits']['Soft']} tours\n"
        f"• Durée Medium max : {cfg['tyre_limits']['Medium']} tours\n"
        f"• Indice de criticité : {cfg['category']}\n"
        f"• Recommandation : {conseil}"
    )
if __name__ == "__main__":
    mcp.run()
    