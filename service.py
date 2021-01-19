import requests
import pandas as pd
import json
import os.path

HOST = "https://api-football-v1.p.rapidapi.com/v2/"
LIGUE1_ID = "2664"
ROUND_LABEL = "Regular_Season_-_"
FOLDER_PATH = "./rounds/"

def getApiKey():
    f = open("vars", "r")
    return f.readline()

HEADERS = {"X-RapidAPI-Key": getApiKey()}

def createJsonFile(championshipRoundJson, championshipRound):
    with open(FOLDER_PATH + str(championshipRound) + ".json", "w") as outfile:
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

    url = HOST + "fixtures/league/" + LIGUE1_ID + "/" + ROUND_LABEL + str(championshipRound - 1)

    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)

    fixtures = reqJson["api"]["fixtures"]

    championshipRoundJson = {}
    championshipRoundJson["matches"] = []
    championshipRoundJson["teams"] = []
    for fixture in fixtures:
        if fixture["goalsHomeTeam"] != None:
            fixtureWinner = getWinner(fixture["goalsHomeTeam"], fixture["goalsAwayTeam"])
            championshipRoundJson["teams"].append(fixture["homeTeam"]["team_name"])
            championshipRoundJson["teams"].append(fixture["awayTeam"]["team_name"])
        else:
            fixtureWinner = "null"
        homeTeamStats, awayTeamStats = getPredictionsForfixture(fixture["fixture_id"], fixtureWinner)
        
        championshipRoundJson["matches"].append({
            "winner": fixtureWinner,
            "home": homeTeamStats,
            "away": awayTeamStats,
        })

    createJsonFile(championshipRoundJson, championshipRound-1)
    print("Generated JSON File for championship round " + str(championshipRound))

def getTeamFixtureWithRoundAndTeamName(championshipRound, teamName):
    url = HOST + "fixtures/league/" + LIGUE1_ID + "/" + ROUND_LABEL + str(championshipRound - 1)

    req = requests.get(url, headers = HEADERS)
    reqJson = json.loads(req.text)

    fixtures = reqJson["api"]["fixtures"]
    fixtureInfos = {}
    for fixture in fixtures:
        homeTeamName = fixture["homeTeam"]["team_name"]
        awayTeamName = fixture["awayTeam"]["team_name"]
        if homeTeamName or awayTeamName == teamName:
            print(homeTeamName + "vs" + awayTeamName + " - selected " + teamName)
            fixtureId = fixture["fixture_id"]
            fixtureStats = getFixtureStatsToPredict(fixtureId)
            break
    
    return fixtureStats


def getFixtureStatsToPredict(fixtureId):
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
    
    fixtureStats = {
        "home": homeTeamStats,
        "away": awayTeamStats,
    }

    return fixtureStats

def getPredictionsForfixture(fixtureId, fixtureWinner):
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

def getTeamsForChampionshipRound(championshipRound):
    filePath = FOLDER_PATH + str(championshipRound-1) + ".json"
    if os.path.isfile(filePath):
        jsonFile = readJSONFile(filePath)
        teams = jsonFile["teams"]
        teams.sort()
        return teams
    else:
        print("Retrieving the championship round informations... please wait...")
        generateJsonByChampionshipRound(championshipRound)
        jsonFile = readJSONFile(filePath)
        teams = jsonFile["teams"]
        teams.sort()
        return teams