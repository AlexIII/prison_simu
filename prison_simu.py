from typing import *
from random import randrange
from dataclasses import dataclass
from functools import reduce

# Config for a season
@dataclass
class Season:
    days: int               # Number of days in the season
    receiversN: int         # Number of prisoner-receivers in the season
    receiverTarget: int     # Number of tokens a prisoner-receiver must receive in the season

# --- Input params
runGamesN = 1000
seasons = [Season(2800, 10, 10), Season(1500, 1, 10)]
# --- 

prisonersN = reduce(lambda acc, s: acc * s.receiverTarget, seasons, 1)
assert(prisonersN == 100)
daysInGeneration = reduce(lambda acc, s: acc + s.days, seasons, 0)
print(f"{daysInGeneration=}")

def generation() -> Tuple[int, bool]:   # return (days, isGameWon)
    days = 0
    lamp = False
    for seasonIdx, season in enumerate(seasons):
        prevSeasonReceivers = prisonersN if seasonIdx == 0 else seasons[seasonIdx-1].receiversN
        isLastSeason = seasonIdx == len(seasons) - 1

        # Set initial number of tokens
        receivers = [1] * season.receiversN
        transmittersN = prevSeasonReceivers - season.receiversN
        transmitters = [1] * transmittersN

        for _ in range(0, season.days):
            days += 1
            p = randrange(0, prisonersN) # Selecting random prisoner
            if p < season.receiversN: # Is prisoner-receiver, p \in [0, season.receiversN - 1]
                if lamp and receivers[p] < season.receiverTarget: # Check if prisoner-receiver can acquire token
                    receivers[p] += 1
                    lamp = False
                    if isLastSeason and receivers[p] == season.receiverTarget: # Check if we have won the game
                        return (days, True)
            elif p < season.receiversN + transmittersN: # Is prisoner-transmitter, p \in [season.receiversN, season.receiversN + transmittersN - 1]
                if not lamp and transmitters[p - season.receiversN] > 0: # Check if prisoner-transmitter can give token
                    lamp = True
                    transmitters[p - season.receiversN] -= 1

        seasonOk = not lamp and all(r == season.receiverTarget for r in receivers)
        if not seasonOk: # Failed season leads to the whole generation failure :'(
            # print(f"Season {seasonN} has failed (and this generation is too...)")
            return (daysInGeneration, False)
        
        assert(all(t == 0 for t in transmitters))

    assert(days == daysInGeneration)
    return (days, False)

def game() -> Tuple[int, int]:   # return (gens, days)
    days = 0
    gens = 0
    while True:
        gDays, isDone = generation()
        days += gDays
        gens += 1
        if isDone: break
    # print(gens, days)
    return (gens, days)

games = list(map(lambda _: game(), range(runGamesN)))
gamesSum = reduce(lambda acc, g: (acc[0]+g[0], acc[1]+g[1]), games, (0,0))
gamesMean = (gamesSum[0] / runGamesN, gamesSum[1] / runGamesN)

gamesSingleGenMean = reduce(lambda acc, g: acc + (g[1] if g[0] == 1 else 0), games, 0) / runGamesN

print(f"Games played: {runGamesN}")
print(f"Mean generations: {gamesMean[0]}")
print(f"Mean days: {gamesMean[1]}")
print(f"Mean days if the game was won in the first generation: {gamesSingleGenMean}")
