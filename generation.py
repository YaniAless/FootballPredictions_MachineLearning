import requests
import pandas as pd
import json
import os.path

HOST = "https://api-football-v1.p.rapidapi.com/v2/"
LIGUE1_ID = "2664"
ROUND_LABEL = "Regular_Season_-_"

def getApiKey():
    f = open("vars", "r")
    return f.readline()

HEADERS = { 'X-RapidAPI-Key': getApiKey()}

def createJsonFile(championshipRoundJson, championshipRound):
    with open("./fixtures/" + str(championshipRound) + ".json", "w") as outfile:
        json.dump(championshipRoundJson, outfile)
    

def getWinner(homeTeamScore, awayTeamScore):
    if homeTeamScore > awayTeamScore:
        return 1
    elif homeTeamScore < awayTeamScore:
        return 2
    else:
        return 0

def readJSONFile(pathToFile):
    with open(pathToFile, "r") as JSONFile:
        readJSON = json.load(JSONFile)

    return readJSON

def generateJsonByChampionshipRound(championshipRound):
    championshipRound = championshipRound - 1

    url = HOST + "fixtures/league/" + LIGUE1_ID + "/" + ROUND_LABEL + str(championshipRound - 1)
    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)
    fixtures = reqJson["api"]["fixtures"]

    championshipRoundJson = {}
    championshipRoundJson["matches"] = []
    for fixture in fixtures:
        fixtureWinner = getWinner(fixture["goalsHomeTeam"], fixture["goalsAwayTeam"])
        homeTeamStats, awayTeamStats = getPredictionsForFicture(fixture["fixture_id"], fixtureWinner)
        
        championshipRoundJson["matches"].append({
            "winner": fixtureWinner,
            "home": homeTeamStats,
            "away": awayTeamStats,
        })

    createJsonFile(championshipRoundJson, championshipRound)
    print("Generated JSON File for championship round " + str(championshipRound))

def getPredictionsForFicture(fixtureId, fixtureWinner):
    url = HOST + "predictions/" + str(fixtureId)
    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)
    
    comparison = reqJson["api"]["predictions"][0]["comparison"]
    homeTeamStats = {
        "goals_avg": reqJson["api"]["predictions"][0]["teams"]["home"]["last_5_matches"]["goals_avg"],
        "goals_against_avg": reqJson["api"]["predictions"][0]["teams"]["home"]["last_5_matches"]["goals_against_avg"],
        "forme": comparison["forme"]["home"],
        "att": comparison["att"]["home"],
        "def": comparison["def"]["home"],
        "h2h": comparison["h2h"]["home"],
    }

    awayTeamStats = {
        "goals_avg": reqJson["api"]["predictions"][0]["teams"]["away"]["last_5_matches"]["goals_avg"],
        "goals_against_avg": reqJson["api"]["predictions"][0]["teams"]["away"]["last_5_matches"]["goals_against_avg"],
        "forme": comparison["forme"]["away"],
        "att": comparison["att"]["away"],
        "def": comparison["def"]["away"],
        "h2h": comparison["h2h"]["away"],
    }   
    
    return  homeTeamStats, awayTeamStats