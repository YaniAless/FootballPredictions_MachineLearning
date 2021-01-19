import generation as gen
import asyncio

chosenChampionshipDay = 0

def askForChampionshipRound():
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

def displayTeamsName(chosenChampionshipDay):
    teams = gen.getTeamsForChampionshipRound(chosenChampionshipDay)
    print("Type the exact name of the team you want to choose")
    for team in teams:
        print(team)

if __name__ == "__main__":
    print("Hello ! Let's predict the result of a match !")
    print("infos : you can exit this software by typing 42")
    while chosenChampionshipDay != 42:
        askForChampionshipRound()
        askFor
    
