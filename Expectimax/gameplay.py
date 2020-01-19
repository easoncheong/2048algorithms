import random
import math
import gamestate
import os
import time

'''
Gameplay Classes
'''

class Game:

    gameState = gamestate.GameState()

    FUNCT_LIST = [
        gameState.left_position,
        gameState.down_position,
        gameState.up_position,
        gameState.right_position
    ]

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.score = 0
        self.position = [[0 for _ in range(4)] for _ in range(4)]

    def make_move(self, move):
        if move in self.gameState.list_legal_moves(self.position):
            self.position, scoreIncrease = self.FUNCT_LIST[move](self.position, True)
            self.position = self.gameState.add_new_tile(self.position)
            self.score += scoreIncrease
            return True
        else:
            return False

    def game_active(self):
        return self.gameState.list_legal_moves(self.position) != []

    def play_game(self, depth, game_no):

        moves_count = 0
        for _ in range(2):
            self.position = self.gameState.add_new_tile(self.position)

        while self.game_active():
            timeStart = time.time_ns()
            moves_count += 1
            legal_positions = self.gameState.list_legal_moves(self.position)
            move_selected, ev = self.algorithm(self.position, depth, legal_positions)
            while not self.make_move(move_selected):
                move_selected, ev = self.algorithm(self.position, depth, legal_positions)
            timeEnd = time.time_ns()
            tile_perm = self.gameState.tilePerm(self.position)

            os.system('clear')
            print('Expectiminimax Game', game_no)
            print('Depth', depth)
            print('Move:', str(moves_count))
            print('Score', str(self.score))
            print('Tile', int(2**(tile_perm-1)))
            print('Evaluation:', str(ev))
            print('Time for previous move:', str(round((timeEnd - timeStart)/1000000, 3)))
        
        log_perm = self.gameState.logPerm(self.position)
        tile_perm = self.gameState.tilePerm(self.position)

        return log_perm, tile_perm, self.position, self.score, moves_count

    def play_sample_game(self, file_name, depth, game_no):

        f = open(file_name + '.txt', 'w+')

        f.write(file_name[10:])

        moves_count = 0
        for _ in range(2):
            self.position = self.gameState.add_new_tile(self.position)

        while self.game_active():
            timeStart = time.time_ns()
            moves_count += 1
            legal_positions = self.gameState.list_legal_moves(self.position)
            move_selected, ev = self.algorithm(self.position, depth, legal_positions)
            
            while not self.make_move(move_selected):
                move_selected, ev = self.algorithm(self.position, depth, legal_positions)
            timeEnd = time.time_ns()
            f.write('\nMove selected: ' + ['Left', 'Down', 'Up', 'Right'][move_selected])
            f.write('\n\nMove ' + str(moves_count))
            f.write('\nPosition:')
            tile_perm = self.gameState.tilePerm(self.position)

            os.system('clear')
            print('Expectiminimax Sample Game', game_no)
            print('Depth', depth)
            print('Move:', str(moves_count))
            print('Score', str(self.score))
            print('Tile', int(2**(tile_perm-1)))
            print('Evaluation:', str(ev))
            print('Time for previous move:', str(round((timeEnd - timeStart)/1000000, 3)))
            

            for i in self.position:
                f.write('\n' + str(i))


        log_perm = self.gameState.logPerm(self.position)
        tile_perm = self.gameState.tilePerm(self.position)

        return log_perm, tile_perm, self.position, self.score, moves_count
    