# FootballPredictions - Machine Learning

Football predictions using Machine Learning

## Etapes à faire pour récolter les données

1. On requete 1 journée de championnat
2. On récupère tous les fixtures ID (10 normalement) + vainqueur du match 
3. On requête les prédictions pour chaque fixture ID récupéré 
4. On ajoute les données reçues, ainsi que le vainqueur du match dans le CSV

### Notes

"last_5_matchs" : les performances sur les 5 derniers matchs d'une équipe donnée, dans le championnat donné

"comparison" : comparaison des matchs entre deux équipes données

## Données interessantes

**Exemple pour https://api-football-v1.p.rapidapi.com/v2/predictions/571659**

### PSG
```
"last_5_matches": {
    "forme": "53%",
    "att": "50%",
    "def": "86%",
    "goals": 7,
    "goals_avg": 1.4,
    "goals_against": 2,
    "goals_against_avg": 0.4
}
```

### BREST
```
"last_5_matches": {
    "forme": "53%",
    "att": "64%",
    "def": "50%",
    "goals": 9,
    "goals_avg": 1.8,
    "goals_against": 7,
    "goals_against_avg": 1.4
}
```

### PSG - BREST

```
"comparison": {
    "forme": {
        "home": "50%",
        "away": "50%"
    },
    "att": {
        "home": "44%",
        "away": "56%"
    },
    "def": {
        "home": "78%",
        "away": "22%"
    },
    "fish_law": {
        "home": "0%",
        "away": "0%"
    },
    "h2h": {
        "home": "93%",
        "away": "7%"
    },
    "goals_h2h": {
        "home": "76%",
        "away": "24%"
    }
}
```