import algorithms
import gameplay
import time
import os

# The Number of Games
N_GAMES = 100
N_SAMPLE_GAMES = 5
DEPTH = [
    8,
    10,
    12,
    14
]
h = open('./Results/Overall Results.txt', 'w+')

def run(DEPTH):

    f = open('./Results/' + str(DEPTH) + ' depth results.txt', "w+")
    print('now running AB AMM depth', DEPTH)

    results_list = []
    positions_list = []
    scores_list = []
    total_moves = 0

    games_logPR = 0
    games_tilePR = 0

    # Play Game
    for n in range(N_SAMPLE_GAMES):

        game = gameplay.Game(algorithms.search)
        resultFull = game.play_sample_game('./Results/Game ' + str(DEPTH) + ' Sample Game '+ str(n+1), DEPTH, n+1)

        f.write('\nSample Game ' + str(n+1) + ':')
        f.write('\nFinal Score: ' + str(resultFull[3]))
        f.write('\nLogarithmic Performance: ' + str(resultFull[0]))
        f.write('\nMax Tile Performance: ' + str(resultFull[1]))
        f.write('\nAssigned PR: ' + str(min(resultFull[0], resultFull[1])))
        f.write('\nFinal Position:\n')
        for row in resultFull[2]:
            f.write(str(row) + '\n')

    start = time.time_ns()

    for n in range(N_GAMES):

        if (n+1) % 250 == 0:
            print(n+1, 'games elapsed')

        game = gameplay.Game(algorithms.search)
        resultFull = game.play_game(DEPTH, n+1)
        scores_list.append(resultFull[3])
        positions_list.append(resultFull[2])
        result = min(resultFull[0:2])
        results_list.append(result)

        f.write('\nGame ' + str(n+1) + ':')
        f.write('\nFinal Score: ' + str(resultFull[3]))
        f.write('\nLogarithmic Performance: ' + str(resultFull[0]))
        f.write('\nMax Tile Performance: ' + str(resultFull[1]))
        f.write('\nAssigned PR: ' + str(min(resultFull[0], resultFull[1])))
        f.write('\nFinal Position:\n')
        total_moves += resultFull[4]
        for row in resultFull[2]:
            f.write(str(row) + '\n')
        if resultFull[0] < resultFull[1]:
            games_logPR += 1
        else:
            games_tilePR += 1

    end = time.time_ns()
    timeElapsed = (end-start)
    timeElapsed //= 1000000

    # Result Print
    f.write('\nAverage PR: ' + str(sum(results_list) / N_GAMES))
    f.write('\nMaximum PR: ' + str(max(results_list)))
    f.write('\nMinimum PR: ' + str(min(results_list)))

    f.write('\n\nAverage Score: ' + str(sum(scores_list) / N_GAMES))
    f.write('\nMaximum Score: ' + str(max(scores_list)))
    f.write('\nMinimum Score: ' + str(min(scores_list)))

    f.write('\n\nTotal Time: ' + str(timeElapsed) + 'ms')
    f.write('\nTotal Moves: ' + str(total_moves))
    f.write('\nAverage Move Time: ' + str(round(timeElapsed / total_moves, 2)))

    f.write('\n\nTile PR-Limited Games: ' + str(games_tilePR) + ' (' + str(round(100 * games_tilePR/N_GAMES, 1)) + '%)' )
    f.write('\nLog PR-Limited Games: ' + str(games_logPR) + ' (' + str(round(100 * games_logPR/N_GAMES, 1)) + '%)' )

    # Status Updates
    os.system('clear')
    h.write('completed depth ' + str(DEPTH) + ' in ' + str(round(timeElapsed/1000, 1)) + ' s and ' + str(total_moves) + ' moves, averaging ' + str(round(timeElapsed/total_moves, 2)) + ' ms/move\n')
    h.write('PR: avg ' + str(round(sum(results_list) / N_GAMES, 2)) + ', max ' + str(round(max(results_list), 2)) + ', min ' + str(round(min(results_list), 2)) + '\n')
    h.write('Score: avg ' + str(round(sum(scores_list) / N_GAMES, 1)) + ', max ' + str(max(scores_list)) + ', min ' + str(min(scores_list)) + '\n')
    h.write('Log PR Limited: ' + str(round(100 * games_logPR/N_GAMES, 1)) + '%\n')
    h.write('Tile PR Limited: ' + str(round(100 * games_tilePR/N_GAMES, 1)) + '%\n\n')

    f.close()

def main():
    for i in DEPTH:
        run(i)

main()