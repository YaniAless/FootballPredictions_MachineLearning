import service
import numpy as np
import matplotlib.pyplot as plt

from math import *
from sklearn.neural_network import MLPClassifier

def predictWinnerWithFixtureInfos(chosenChampionshipRound, teamName):
    fixtureInfos = service.getTeamFixtureWithRoundAndTeamName(chosenChampionshipRound, teamName)
    # print(fixtureInfos)

    filePath = service.FOLDER_PATH + str(chosenChampionshipRound) + ".json"
    championshipRoundsJSON = service.readJSONFile(filePath)

    inputs, desired = extractInputsAndDesiredValues(championshipRoundsJSON["matches"])
    
    print(inputs)
    print("/n")
    print(desired)

    TEST_PERCENTAGE = 30
    training_size = int(len(inputs) * (1.0 - TEST_PERCENTAGE / 100.0))
    train_inputs, train_outputs = inputs[:training_size], desired[:training_size] #On coupe le jeu de données en 2
    test_inputs, test_outputs = inputs[training_size:], desired[training_size:]

    mlp = MLPClassifier()
    mlp.fit(train_inputs, train_outputs)

    #Evaluer sur l'ensemble d'apprentissage la qualité de mon modèle
    learning_score = mlp.score(train_inputs, train_outputs)
    print(f"#Score d'apprentissage : {round(learning_score * 100)}%")

    #Evaluer sur l'ensemble de test la qualité de mon modèle
    learning_score = mlp.score(test_inputs, test_outputs)
    print(f"#Score de test : {round(learning_score * 100)}%")
    

def extractInputsAndDesiredValues(championshipRoundsMatches):
    desired = []
    inputs = []

    for championshipRound in championshipRoundsMatches:
        desired.append(championshipRound["winner"])

        # On ajoute les valeurs de "home" de notre JSON dans inputs
        # On continue avec les valeurs de "away"
        homeGoalsAvg = championshipRound["home"]["goals_avg"]
        homeGoalsAgainstAvg = championshipRound["home"]["goals_against_avg"]   

        # On convertit les pourcentages en float
        homeForme = convertPercentToFloat(championshipRound["home"]["forme"])
        homeAtt = convertPercentToFloat(championshipRound["home"]["att"])
        homeDef = convertPercentToFloat(championshipRound["home"]["def"])
        homeH2h = convertPercentToFloat(championshipRound["home"]["h2h"])

        awayGoalsAvg = championshipRound["away"]["goals_avg"]
        awayGoalsAgainstAvg = championshipRound["away"]["goals_against_avg"]
        
        # On convertit les pourcentages en float
        awayForme = convertPercentToFloat(championshipRound["home"]["forme"])
        awayAtt = convertPercentToFloat(championshipRound["home"]["att"])
        awayDef = convertPercentToFloat(championshipRound["home"]["def"])
        awayH2h = convertPercentToFloat(championshipRound["home"]["h2h"])

        groupedInfo = [homeGoalsAvg, homeGoalsAgainstAvg, homeForme, homeAtt, homeDef, homeH2h, awayGoalsAvg, awayGoalsAgainstAvg, awayForme, awayAtt, awayDef, awayH2h]

        inputs.append(groupedInfo)
            
    return inputs, desired

def convertPercentToFloat(valueToConvert):
    return float(valueToConvert.strip('%'))/10

if __name__ == "__main__":
    predictWinnerWithFixtureInfos(19, "Paris Saint Germain")
    # il faut commencer la prédiction