import requests
import pandas as pd
import json

HOST = "https://api-football-v1.p.rapidapi.com/v2/"
LIGUE1_ID = "2664"
ROUND_LABEL = "Regular_Season_-_"

def getApiKey():
    f = open("vars", "r")
    return f.readline()

HEADERS = { 'X-RapidAPI-Key': getApiKey()}

def createJsonFile(dictionary, championshipRound):
    with open("./fixtures/" + str(championshipRound) + ".json", "w") as outfile:
        json.dump(dictionary, outfile)
    

def getWinner(homeTeamScore, awayTeamScore):
    if homeTeamScore > awayTeamScore:
        return 1
    elif homeTeamScore < awayTeamScore:
        return 2
    else:
        return 0

def getMatchesForChampionshipRound(championshipRound):
    url = HOST + "fixtures/league/" + LIGUE1_ID + "/" + ROUND_LABEL + str(championshipRound - 1)
    # print("URL => " + url)
    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)

    fixtures = reqJson["api"]["fixtures"]

    championshipRoundJson = {}
    championshipRoundJson["matches"] = []
    for fixture in fixtures:
        fixtureWinner = getWinner(fixture["goalsHomeTeam"], fixture["goalsAwayTeam"])
        homeTeamStats, awayTeamStats, comparison = getPredictionsForFicture(fixture["fixture_id"], fixtureWinner)
        # print(fixture)
        
        championshipRoundJson["matches"].append({
            "winner": fixtureWinner,
            "home": homeTeamStats,
            "away": awayTeamStats,
        })

    with open("./fixtures/" + str(championshipRound-1) + ".json", "w") as outfile:
        json.dump(championshipRoundJson, outfile)
    # createJsonFile(fixturesIds, championshipRound-1)

def getPredictionsForFicture(fixtureId, fixtureWinner):
    url = HOST + "predictions/" + str(fixtureId)
    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)

    homeTeamStats = reqJson["api"]["predictions"][0]["teams"]["home"]["last_5_matches"]
    awayTeamStats = reqJson["api"]["predictions"][0]["teams"]["away"]["last_5_matches"]
    comparison = reqJson["api"]["predictions"][0]["comparison"]["h2h"]

    return  homeTeamStats, awayTeamStats, comparison

if __name__ == "__main__":
    # homeTeamStats, awayTeamStats, comparison = getLastFiveMatchStats("571659")
    # print(homeTeamStats)
    # print(awayTeamStats)
    # print(comparison)
    getMatchesForChampionshipRound(18)
    