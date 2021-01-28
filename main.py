import service
import ml
import asyncio

chosenChampionshipDay = 0
chosenTeamId = 0
teamsList = []

def askForChampionshipRound():
    global chosenChampionshipDay
    try:
        chosenChampionshipDay = int(input("First, tell us for what championship day you want to know a result !\nChoose the championship day, from 1 to 38\n"))
        if chosenChampionshipDay == 42:
            print("Goodbye !")
            exit()
        elif chosenChampionshipDay <= 38 and chosenChampionshipDay > 0:
            displayTeamsName(chosenChampionshipDay)
        else:
            askForChampionshipRound()
    except ValueError:
        print("Please enter a number between 1 and 38")
        askForChampionshipRound()

def askToChooseTeam():
    global chosenTeamId
    try:
        chosenTeamId = int(input("Pick a team using the number associated with it\n"))
        if chosenTeamId > 20 or chosenTeamId <= 0:
            raise ValueError
        elif chosenChampionshipDay == 42:
            print("Goodbye !")
            exit()
        else:
            startPrediction()
    except ValueError:
        print("Please enter a number between 1 and 20")
        askToChooseTeam()

def startPrediction():
    print("Let's try to found out which team will win the match !")
    ml.predictWinnerWithFixtureInfos(chosenChampionshipDay, teamsList[chosenTeamId - 1])

def displayTeamsName(chosenChampionshipDay):
    teams = service.getTeamsForChampionshipRound(chosenChampionshipDay)    
    global teamsList
    teamsList += teams
    i = 1
    for team in teams:
        print(str(i) + " - " + team)
        i += 1

if __name__ == "__main__":
    print("Hello ! Let's predict the result of a match !")
    askForChampionshipRound()
    askToChooseTeam()
    print("\n\nLet's hope we are right in our prediction ! Goodbye :)")
