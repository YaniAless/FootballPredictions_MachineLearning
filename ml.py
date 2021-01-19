import service

def predictWinnerWithFixtureInfos(chosenChampionshipDay, teamName):
    fixtureInfos = service.getTeamFixtureWithRoundAndTeamName(chosenChampionshipDay, teamName)
    print(fixtureInfos)
    # il faut commencer la prédiction