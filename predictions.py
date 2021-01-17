import requests
import json

HEADERS = { 'X-RapidAPI-Key': ''}
HOST = "https://api-football-v1.p.rapidapi.com/v2/"

# - On requete 1 journée de championnat
# - On récupère tous les fixtures ID (10 normalement) + vainqueur du match 
# - On requête les prédictions pour chaque fixture ID récupéré 
# - On ajoute les données reçues, ainsi que le vainqueur du match dans le CSV



def getPredictionsForFicture(fixtureId):

    req = requests.get(HOST + "predictions/" + fixtureId, headers = HEADERS)
    req_json = json.loads(req.text)

    home_team_stats = req_json["api"]["predictions"][0]["teams"]["home"]["last_5_matches"]
    away_team_stats = req_json["api"]["predictions"][0]["teams"]["away"]["last_5_matches"]
    comparison = req_json["api"]["predictions"][0]["comparison"]["h2h"]

    return  home_team_stats, away_team_stats, comparison

if __name__ == "__main__":
    home_team_stats, away_team_stats, comparison = getLastFiveMatchStats("571659")

    print(home_team_stats)
    print(away_team_stats)
    print(comparison)