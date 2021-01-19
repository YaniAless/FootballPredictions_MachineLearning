import generation as gen
import asyncio

chosenChampionshipDay = 0

def askForIntValue():
    isInputIntValue = False
    while isInputIntValue == False:
        try:
            chosenChampionshipDay = int(input("First, tell us for what day you want to know a result ! Choose from 1 to 34\n"))
            print("chosenday ", chosenChampionshipDay)
            gen.generateJsonByChampionshipRound(chosenChampionshipDay)
            isInputIntValue = True
        except ValueError:
            print("please enter a number between 1 and 34")
            isInputIntValue = False

if __name__ == "__main__":
    print("Hello ! Let's predict the result of a match !")
    askForIntValue()
