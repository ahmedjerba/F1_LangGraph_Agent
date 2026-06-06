from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings





DIRECTIVES_STRATEGIE = [
    # 1. Bahrain
    "Directive Bahreïn (BAH) : L'asphalte de Sakhir est l'un des plus abrasifs de la saison (Broyeur de Gomme). La dégradation thermique arrière est le facteur limitant. Prioriser une stratégie à 2 arrêts (Medium -> Hard -> Hard). L'undercut est puissant en raison de la perte de rythme immédiate sur les vieux pneus.",
    
    # 2. Saudi Arabia
    "Directive Arabie Saoudite (SAU) : Circuit urbain ultra-rapide avec d'énormes contraintes de traction latérale. L'usure physique est faible, mais la gestion de la température des pneus est cruciale (surchauffe). Probabilité très élevée de voiture de sécurité (Safety Car) : anticiper une fenêtre d'arrêt 'gratuit' dès le premier incident.",
    
    # 3. Australia
    "Directive Australie (AUS) : Tracé à faible énergie initiale mais l'évolution de la piste est massive tout au long du week-end. Le phénomène de 'graining' (billage) est fréquent sur le pneu avant-gauche en début de relais. Surveiller les données de grip avant de valider la bascule sur les gommes Hard.",
    
    # 4. Japan
    "Directive Japon (JPN) : Suzuka applique des forces latérales extrêmes dans le premier secteur (S Curves). C'est un broyeur de gomme pur. Un relais unique en Softs au-delà de 10 tours provoque un effondrement thermique (Cliff). Stratégie classique à 2 arrêts (Medium -> Hard -> Medium) requise.",
    
    # 5. China
    "Directive Chine (CHN) : Le virage 1 en escargot impose des contraintes thermiques massives sur le pneu avant-droit, provoquant un sous-virage critique si le pneu est usé. L'undercut est très efficace car la pitlane est longue, mais la chauffe des pneus neufs est rapide.",
    
    # 6. Miami
    "Directive Miami (MIA) : Circuit lisse à forte chaleur au sol. Le pneu Soft surchauffe après seulement 3 tours lancés en qualification ou en début de course. Pour la course, la stratégie Medium -> Hard est la ligne directrice, en évitant la gomme Soft sauf pour un sprint final sous Safety Car.",
    
    # 7. Emilia-Romagna
    "Directive Émilie-Romagne (EMI) : Imola est un tracé traditionnel étroit où les dépassements en piste sont extrêmement difficiles. La position en piste prime sur l'usure des gommes. Il est préférable d'allonger le relais en Medium (quitte à perdre du rythme) pour garantir un arrêt unique et ne pas tomber dans le trafic.",
    
    # 8. Monaco
    "Directive Monaco (MON) : Le circuit demande le moins d'énergie de l'année sur les pneus, mais la position en piste est absolument tout. Même avec une dégradation théorique de 80%, interdiction de s'arrêter si cela fait ressortir la voiture dans le trafic. Attendre impérativement une Safety Car ou un blocage des concurrents.",
    
    # 9. Canada
    "Directive Canada (CAN) : Circuit semi-urbain caractérisé par de gros freinages et des relances (Circuits Lisses / Traction). L'usure globale est faible mais l'usure par usine de freinage et choc sur les vibreurs fatigue la structure. Stratégie à un seul arrêt hautement recommandée (Medium -> Hard).",
    
    # 10. Spain
    "Directive Espagne (ESP) : Barcelone possède des courbes rapides et un asphalte abrasif réputé pour détruire le pneu avant-gauche (virage 3 et 9). C'est un test ultime pour la dégradation. Une stratégie à 2 arrêts (Medium -> Hard -> Medium) est la référence absolue pour contrer le Cliff thermique.",
    
    # 11. Austria
    "Directive Autriche (AUT) : Circuit court en altitude avec de fortes contraintes thermiques au freinage dans les virages 1, 3 et 4. Le pneu Soft souffre de surchauffe immédiate en traction. Préférer un départ en Medium. Risque élevé de cloquage (blistering) si la température de piste dépasse 40°C.",
    
    # 12. Great Britain
    "Directive Grande-Bretagne (GBR) : Silverstone applique des charges aérodynamiques et latérales maximales (Copse, Maggots, Becketts). Les pneus avant souffrent énormément. L'undercut y est dévastateur (gain estimé à 1.5s dans le tour de sortie). Ne jamais pousser un train de Softs au-delà de 12 tours.",
    
    # 13. Hungary
    "Directive Hongrie (HUN) : Le Hungaroring est un enchaînement incessant de virages sans ligne droite pour refroidir les gommes. Les contraintes thermiques sont permanentes. La stratégie à 2 arrêts est obligatoire car les gommes s'essoufflent par surchauffe de la carcasse.",
    
    # 14. Belgium
    "Directive Belgique (BEL) : À Spa-Francorchamps, la compression de l'Eau Rouge/Raidillon génère des charges verticales monumentales. Risque de défaillance structurelle sur les gommes Softs si poussées trop loin. Respecter scrupuleusement la limite fixée par la simulation (14 tours max en Soft).",
    
    # 15. Netherlands
    "Directive Pays-Bas (NED) : Zandvoort possède des virages relevés (bankings) uniques qui augmentent la charge verticale sur les structures de pneus. L'asphalte est plutôt lisse, mais le trafic est compact. La perte en pit-stop étant très faible (18s), l'agressivité à 2 arrêts avec beaucoup d'undercuts est viable.",
    
    # 16. Italy
    "Directive Italie (ITA) : Monza est le temple de la vitesse. Configurations aérodynamiques à faible appui, ce qui fait glisser la voiture dans les virages lents (Variante del Rettifilo) et use les pneus arrière. Cependant, l'arrêt unique (Medium -> Hard) est privilégié en raison du coût élevé de la pitlane.",
    
    # 17. Azerbaijan
    "Directive Azerbaïdjan (AZE) : Longue ligne droite de 2 km qui refroidit excessivement les pneus avant, suivie de freinages à 90° dans le secteur 1. Risque constant de blocage de roue avant (plat sur le pneu). Privilégier une stratégie flexible pour réagir aux très probables drapeaux rouges.",
    
    # 18. Singapore
    "Directive Singapour (SIN) : Course nocturne urbaine ultra-longue, humide et physiquement éprouvante. Énorme contrainte sur les freins et la traction arrière. Le coût d'un pit-stop est le plus élevé de la saison (28.5s). Minimiser à tout prix le nombre d'arrêts (viser 1 seul arrêt Medium -> Hard).",
    
    # 19. USA
    "Directive USA (USA) : Le circuit d'Austin (COTA) possède un secteur 1 bosselé copié sur Silverstone qui fatigue les suspensions et crée du patinage thermique à haute vitesse. La dégradation est équilibrée entre l'avant et l'arrière. Une stratégie à 2 arrêts est souvent requise.",
    
    # 20. Mexico
    "Directive Mexique (MEX) : Altitude extrême (2200m) entraînant une faible densité de l'air : moins d'appui aéro donc la voiture glisse énormément. Surchauffe immédiate de la bande de roulement. La gestion du patinage en sortie de virage lent détermine la survie du pneu arrière.",
    
    # 21. Brazil
    "Directive Brésil (BRA) : Circuit à l'ancienne qui tourne dans le sens anti-horaire, sollicitant fortement les pneus droits. Le pneu arrière-gauche encaisse toute la traction dans la montée finale. Risque d'averses soudaines : l'équipe doit être prête à basculer sur des calculs de gommes Intermediate.",
    
    # 22. Las Vegas
    "Directive Las Vegas (LVS) : Course nocturne dans le désert avec des températures ambiantes extrêmement basses (parfois <10°C). Le défi majeur est la mise en température des pneus (Warm-up). Risque majeur de graining sévère si le pilote attaque trop fort dans les deux premiers tours du relais.",
    
    # 23. Qatar
    "Directive Qatar (QAT) : Losail est composé presque uniquement de courbes à haute et moyenne vitesse (Broyeur de Gomme). Les vibreurs agressifs détruisent l'intérieur de la carcasse. Sécurité absolue requise : la FIA impose souvent une limite stricte de tours par train de pneu pour éviter les crevaisons.",
    
    # 24. Abu Dhabi
    "Directive Abu Dhabi (ABU) : Grand Prix de crépuscule. La température de la piste chute de plus de 10°C pendant la course, modifiant l'équilibre de la dégradation de thermique (arrière) à mécanique (avant) au fil des tours. Ajuster la stratégie en fin de course pour profiter de la fraîcheur de la piste."
]

def initialiser_outils_rag():
    documents = [Document(page_content=texte) for texte in DIRECTIVES_STRATEGIE]
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db=FAISS.from_documents(documents,embeddings)
    retriever=db.as_retriever(search_kwargs={"k":1})
    
    @tool
    def chercher_directives_ecurie(circuit: str) -> str:
        """
        Consulte la base de connaissances interne et secrète de l'écurie pour récupérer 
        les directives historiques, stratégiques et sécuritaires spécifiques à un Grand Prix.
        Argument :
            circuit : Le nom complet du pays du Grand Prix (ex: 'Belgium', 'Monaco', 'Japan')
        """
        docs = retriever.invoke(circuit)
        if docs:    
            return f"📚 [DIRECTIVE INTERNE ÉCURIE] :\n{docs[0].page_content}"
        return "Aucune directive spécifique trouvée pour ce tracé. Appliquez les protocoles standards."
        
    return chercher_directives_ecurie