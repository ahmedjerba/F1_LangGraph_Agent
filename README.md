# Mini Projet Agent F1

Petit projet démonstratif d'agents pour un cas d'usage F1 (RAG / stratégie).

## Vue d'ensemble
- Contenu: un petit agent RAG et une stratégie F1 pour démonstration et tests.
- Objectif: fournir une base pour expérimenter l'intégration RAG, un agent de stratégie
  et un serveur MCP local.

## Structure du projet
- `app.py` : point d'entrée (exemples d'utilisation / prototype web minimal).
- `data.py` : utilitaires de gestion des données d'exemple.
- `test_core.py` : tests/unitaires simples pour les composants principaux.
- `core_agent/` : logique des agents
  - `f1_rag_setup.py` : préparation RAG / embeddings / indexation
  - `f1_strategy_agent.py` : stratégie et comportement de l'agent
- `mcp_server/` : serveur MCP minimal
  - `f1_mcp_server.py` : wrapper / serveur pour tests locaux

## Prérequis
- Python 3.10+ recommandé
- Outils optionnels: virtualenv

## Installation rapide
1. Créez un environnement virtuel:

```bash
python -m venv .venv
```

2. Activez l'environnement et installez les dépendances (si `requirements.txt` existe):

```bash
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
```

Si aucun `requirements.txt` n'est présent, installez manuellement les dépendances nécessaires (e.g. `openai`, `langchain`, `chromadb`, etc.) selon vos besoins.

## Exemples d'utilisation
- Lancer le serveur MCP local (exemple) :

```bash
python mcp_server/f1_mcp_server.py
```

- Lancer un petit test/un script :

```bash
python app.py
```

## Fichiers importants
- Voir la section "Structure du projet" ci-dessus.

## Conseils
- Ne pas committer les clés d'API ni les fichiers volumineux (voir `.gitignore`).
- Documentez vos dépendances dans `requirements.txt` pour reproductibilité.

## Licence
Projet d'exemple — adaptez la licence selon vos besoins.
