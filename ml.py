import service
import numpy as np
import matplotlib.pyplot as plt

from math import *
from sklearn.neural_network import MLPClassifier

def predictWinnerWithFixtureInfos(chosenChampionshipRound, teamName):

    #filePath = service.FOLDER_PATH + str(chosenChampionshipRound) + ".json"
    #championshipRoundsJSON = service.readJSONFile(filePath)
    #inputs = extractInputsValuesFromMatches(championshipRoundsJSON["matches"])
    #desired = extractDesiredValuesFromMatches(championshipRoundsJSON["matches"])

    fixtureInfosToCompare = service.getTeamFixtureWithRoundAndTeamName(chosenChampionshipRound, teamName)
    inputs, desired = service.combinedAllRoundsFound()

    TEST_PERCENTAGE = 30
    training_size = int(len(inputs) * (1.0 - TEST_PERCENTAGE / 100.0))
    train_inputs, train_outputs = inputs[:training_size], desired[:training_size] #On coupe le jeu de données en 2
    test_inputs, test_outputs = inputs[training_size:], desired[training_size:]

    mlp = MLPClassifier(solver='adam', max_iter=10000, learning_rate_init=0.048214, random_state=3, hidden_layer_sizes=(14), verbose=True, tol=0.000001)    
    trainedModel = mlp.fit(train_inputs, train_outputs)
    
    # Evaluer sur l'ensemble d'apprentissage la qualité de mon modèle
    learning_score = mlp.score(train_inputs, train_outputs)
    print(f"#Score d'apprentissage : {round(learning_score * 100)}%")

    ## Evaluer sur l'ensemble de test la qualité de mon modèle
    learning_score = mlp.score(test_inputs, test_outputs)
    print(f"#Score de test : {round(learning_score * 100)}%")

    fig, ax = plt.subplots()
    ax.plot(mlp.loss_curve_)
    plt.yscale('log')
    plt.show()

    inputsToCompare = extractInputsFromFixtureStats(fixtureInfosToCompare)
    prediction = mlp.predict(np.array(inputsToCompare).reshape(1, -1))
    prediction_odds = mlp.predict_proba(np.array(inputsToCompare).reshape(1, -1))
    
    #print("Match prediction => " + str(prediction))
    #print("Match odds => " + str(prediction_odds))
    

def extractDesiredValuesFromMatches(championshipRoundsMatches):
    desired = []

    for championshipRound in championshipRoundsMatches:
        desired.append(championshipRound["winner"])
    
    return desired

def extractDesiredValuesFromFixtureStats(fixtureStats):
    return fixtureStats["winner"]
    
def extractInputsFromFixtureStats(fixtureStats):
    # On ajoute les valeurs de "home" de notre JSON dans inputs
    # On continue avec les valeurs de "away"
    homeGoalsAvg = fixtureStats["home"]["goals_avg"]
    homeGoalsAgainstAvg = fixtureStats["home"]["goals_against_avg"]   

    # On convertit les pourcentages en float
    homeForme = convertPercentToFloat(fixtureStats["home"]["forme"])
    homeAtt = convertPercentToFloat(fixtureStats["home"]["att"])
    homeDef = convertPercentToFloat(fixtureStats["home"]["def"])
    homeH2h = convertPercentToFloat(fixtureStats["home"]["h2h"])

    awayGoalsAvg = fixtureStats["away"]["goals_avg"]
    awayGoalsAgainstAvg = fixtureStats["away"]["goals_against_avg"]
    
    # On convertit les pourcentages en float
    awayForme = convertPercentToFloat(fixtureStats["home"]["forme"])
    awayAtt = convertPercentToFloat(fixtureStats["home"]["att"])
    awayDef = convertPercentToFloat(fixtureStats["home"]["def"])
    awayH2h = convertPercentToFloat(fixtureStats["home"]["h2h"])

    inputfixtureStats = [homeGoalsAvg, homeGoalsAgainstAvg, homeForme, homeAtt, homeDef, homeH2h, awayGoalsAvg, awayGoalsAgainstAvg, awayForme, awayAtt, awayDef, awayH2h]
    return inputfixtureStats


def extractInputsValuesFromMatches(championshipRoundsMatches):    
    inputs = []

    for championshipRound in championshipRoundsMatches:

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
            
    return inputs

def convertPercentToFloat(valueToConvert):
    valueToFloat = float(valueToConvert.strip('%'))/10
    return round(valueToFloat, 2)

if __name__ == "__main__":
    predictWinnerWithFixtureInfos(21, "Marseille")
    # il faut commencer la prédiction