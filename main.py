import generation as gen
import asyncio

chosenChampionshipDay = 0
chosenTeamId = 0
teamsList = []

def askForChampionshipRound():
    global chosenChampionshipDay
    isInputIntValue = False
    while isInputIntValue == False:
        try:
            chosenChampionshipDay = int(input("First, tell us for what day you want to know a result ! Choose from 1 to 34\n"))
            if chosenChampionshipDay == 42:
                exit()
            else:
                isInputIntValue = True
                displayTeamsName(chosenChampionshipDay)
        except ValueError:
            print("Please enter a number between 1 and 34")
            isInputIntValue = False

def askToChooseTeam():
    global chosenTeamId
    isInputIntValue = False
    while isInputIntValue == False:
        try:
            chosenTeamId = int(input("Pick a team using the number associated with it\n"))
            isInputIntValue = True
            
        except ValueError:
            print("Please enter a number between 1 and 20")
            isInputIntValue = False

def displayTeamsName(chosenChampionshipDay):
    teams = gen.getTeamsForChampionshipRound(chosenChampionshipDay)    
    global teamsList
    teamsList += teams
    i = 1
    for team in teams:
        print(str(i) + " - " + team)
        i += 1

def predictWinnerWithFixtureInfos():
    fixtureInfos = gen.getTeamFixtureWithRoundAndTeamName(chosenChampionshipDay, teamsList[chosenTeamId - 1])
    
    # il faut commencer la prédiction

if __name__ == "__main__":
    print("Hello ! Let's predict the result of a match !")

    askForChampionshipRound()
    askToChooseTeam()
    # On récupère les infos du match pour la journée donnée
    predictWinnerWithFixtureInfos()