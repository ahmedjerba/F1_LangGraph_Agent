COMPOUND_MAP = {
    'PIT_HARD': 1,
    'PIT_MEDIUM': 2,
    'PIT_SOFT': 3
}

F1_SEASON_2024_CONFIG = {
    'Bahrain': {
        'category': 'Broyeurs de Gomme',
        'code': 'BAH', 'round': 1, 
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.85, 'pit_loss': 23.0,
        'tyre_limits': {'Hard': 34, 'Medium': 24, 'Soft': 16}
    },
    'Saudi Arabia': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'SAU', 'round': 2,
        'compounds': {'Hard': 2, 'Medium': 3, 'Soft': 4},
        'wear_factor': 1.10, 'pit_loss': 24.0,
        'tyre_limits': {'Hard': 48, 'Medium': 34, 'Soft': 22}
    },
    'Australia': { # Remplacement de 'Melbourne'
        'category': 'Faible Énergie',
        'code': 'AUS', 'round': 3,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.05, 'pit_loss': 21.0,
        'tyre_limits': {'Hard': 38, 'Medium': 26, 'Soft': 14}
    },
    'Japan': { # Remplacement de 'Suzuka'
        'category': 'Broyeurs de Gomme',
        'code': 'JPN', 'round': 4,
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.80, 'pit_loss': 22.5,
        'tyre_limits': {'Hard': 32, 'Medium': 22, 'Soft': 15}
    },
    'China': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'CHN', 'round': 5,
        'compounds': {'Hard': 2, 'Medium': 3, 'Soft': 4},
        'wear_factor': 0.95, 'pit_loss': 25.5,
        'tyre_limits': {'Hard': 35, 'Medium': 25, 'Soft': 17}
    },
    'Miami': {
        'category': 'Circuits Lisses',
        'code': 'MIA', 'round': 6,
        'compounds': {'Hard': 2, 'Medium': 3, 'Soft': 4},
        'wear_factor': 1.15, 'pit_loss': 24.5,
        'tyre_limits': {'Hard': 42, 'Medium': 28, 'Soft': 18}
    },
    'Emilia-Romagna': { # Remplacement de 'Imola'
        'category': 'Circuits Lisses',
        'code': 'EMI', 'round': 7,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.00, 'pit_loss': 23.0,
        'tyre_limits': {'Hard': 44, 'Medium': 30, 'Soft': 20}
    },
    'Monaco': {
        'category': 'Faible Énergie',
        'code': 'MON', 'round': 8,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.50, 'pit_loss': 25.0,
        'tyre_limits': {'Hard': 60, 'Medium': 45, 'Soft': 30}
    },
    'Canada': {
        'category': 'Circuits Lisses',
        'code': 'CAN', 'round': 9,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.25, 'pit_loss': 22.5,
        'tyre_limits': {'Hard': 48, 'Medium': 32, 'Soft': 20}
    },
    'Spain': {
        'category': 'Broyeurs de Gomme',
        'code': 'ESP', 'round': 10,
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.82, 'pit_loss': 23.0,
        'tyre_limits': {'Hard': 34, 'Medium': 24, 'Soft': 16}
    },
    'Austria': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'AUT', 'round': 11,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 0.88, 'pit_loss': 20.5,
        'tyre_limits': {'Hard': 40, 'Medium': 28, 'Soft': 18}
    },
    'Great Britain': { # Remplacement de 'Silverstone'
        'category': 'Broyeurs de Gomme',
        'code': 'GBR', 'round': 12,
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.75, 'pit_loss': 20.0,
        'tyre_limits': {'Hard': 35, 'Medium': 25, 'Soft': 17}
    },
    'Hungary': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'HUN', 'round': 13,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 0.92, 'pit_loss': 23.5,
        'tyre_limits': {'Hard': 40, 'Medium': 28, 'Soft': 18}
    },
    'Belgium': { # Remplacement de 'Spa'
        'category': 'Broyeurs de Gomme',
        'code': 'BEL', 'round': 14,
        'compounds': {'Hard': 2, 'Medium': 3, 'Soft': 4},
        'wear_factor': 0.90, 'pit_loss': 23.5,
        'tyre_limits': {'Hard': 30, 'Medium': 22, 'Soft': 14}
    },
    'Netherlands': { # Remplacement de 'Zandvoort'
        'category': 'Circuits Lisses',
        'code': 'NED', 'round': 15,
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.82, 'pit_loss': 18.0,
        'tyre_limits': {'Hard': 42, 'Medium': 30, 'Soft': 20}
    },
    'Italy': { # Remplacement de 'Monza'
        'category': 'Circuits Lisses',
        'code': 'ITA', 'round': 16,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.05, 'pit_loss': 24.0,
        'tyre_limits': {'Hard': 40, 'Medium': 28, 'Soft': 18}
    },
    'Azerbaijan': { # Remplacement de 'Baku'
        'category': 'Faible Énergie',
        'code': 'AZE', 'round': 17,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.15, 'pit_loss': 26.0,
        'tyre_limits': {'Hard': 42, 'Medium': 28, 'Soft': 18}
    },
    'Singapore': {
        'category': 'Faible Énergie',
        'code': 'SIN', 'round': 18,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.20, 'pit_loss': 28.5,
        'tyre_limits': {'Hard': 42, 'Medium': 28, 'Soft': 18}
    },
    'USA': { # Remplacement de 'Austin'
        'category': 'Circuits Lisses',
        'code': 'USA', 'round': 19,
        'compounds': {'Hard': 2, 'Medium': 3, 'Soft': 4},
        'wear_factor': 0.88, 'pit_loss': 24.0,
        'tyre_limits': {'Hard': 36, 'Medium': 24, 'Soft': 16}
    },
    'Mexico': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'MEX', 'round': 20,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.10, 'pit_loss': 24.5,
        'tyre_limits': {'Hard': 50, 'Medium': 35, 'Soft': 22}
    },
    'Brazil': { # Remplacement de 'Interlagos'
        'category': 'Contraintes Thermiques & Traction',
        'code': 'BRA', 'round': 21,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 0.95, 'pit_loss': 21.0,
        'tyre_limits': {'Hard': 40, 'Medium': 28, 'Soft': 18}
    },
    'Las Vegas': {
        'category': 'Faible Énergie',
        'code': 'LVS', 'round': 22,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.35, 'pit_loss': 27.0,
        'tyre_limits': {'Hard': 48, 'Medium': 32, 'Soft': 20}
    },
    'Qatar': {
        'category': 'Broyeurs de Gomme',
        'code': 'QAT', 'round': 23,
        'compounds': {'Hard': 1, 'Medium': 2, 'Soft': 3},
        'wear_factor': 0.70, 'pit_loss': 25.0,
        'tyre_limits': {'Hard': 30, 'Medium': 22, 'Soft': 16}
    },
    'Abu Dhabi': {
        'category': 'Contraintes Thermiques & Traction',
        'code': 'ABU', 'round': 24,
        'compounds': {'Hard': 3, 'Medium': 4, 'Soft': 5},
        'wear_factor': 1.10, 'pit_loss': 24.0,
        'tyre_limits': {'Hard': 40, 'Medium': 28, 'Soft': 18}
    }
}