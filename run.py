#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import queue
import random
#import os
import sys
import time

DOMINO_SET = [(i, j) for i in range(7) for j in range(7) if j >= i]
DOUBLE_SET = [(i, j) for i in range(7) for j in range(7) if (j == i and j != 0)]
FIRST_HAND = [(0,1), (0,2), (0,3), (1,2), (0,4), (1,3), (0,5)]
CONFIG = {'Players':['comp', 'comp', 'comp', 'human']}
LEFT_CHAIN_END = 0
RIGHT_CHAIN_END = 1

class PlayTable(object):
    """
    """
    bazar = [i for i in DOMINO_SET]

    def __init__(self):
        self.game_chain = list()
        self.batch = 0
        self.first_tile = None
        self.players_set = list()

    def add_player(self, player):
        self.players_set.append(player)
        for i in range(7):
            player.get_bone()

    def endtheround(self):
        return True

    def show_table(self):
        print(self.game_chain.pop)

    def str(self):
        for i in self.game_chain:
            print(i, end=' ')
            print('\n')


class Account(object):
    def countup(self):
        pass


class Player(object):
    """"""
    def __init__(self, nature, game):
        self._bones = list()
        self.nature = nature
        self.game = game

    def turn_on(self, tile):
        return (tile[1], tile[0])

    def _ebrain(self):
        """
        Use random choise from set
        :return: tail, tail
        """
        left_num = self.game.game_chain[0][0]
        right_num = self.game.game_chain[-1][1]
        left_end_set = set()
        right_end_set = set()
        for i in self._bones:
            if self.check_tile_suit(i) == LEFT_CHAIN_END:
                left_end_set.add(i)
            else:
                right_end_set.add(i)
        # No tile to move
        if left_end_set == set() and right_end_set == set():
            tile = self.get_tile_from_bazar()
            if tile is None:
                return None, None
            else:
                if self.check_tile_suit(tile) == LEFT_CHAIN_END:
                    if tile[1] == left_num:
                        return tile, LEFT_CHAIN_END
                    else:
                        return self.turn_on(tile), LEFT_CHAIN_END
                else:
                    if tile[0] == right_num:
                        return tile, RIGHT_CHAIN_END
                    else:
                        return self.turn_on(tile), RIGHT_CHAIN_END
        # Can move to left tail
        elif left_end_set and right_end_set == set():
            tile = random.choice(tuple(left_end_set))
            if tile[1] == left_num:
                return tile, LEFT_CHAIN_END
            else:
                return self.turn_on(tile), LEFT_CHAIN_END
        # Can move to the right tail
        elif left_end_set == set() and right_end_set:
            tile = random.choice(tuple(right_end_set))
            if tile[0] == right_num:
                return tile, RIGHT_CHAIN_END
            else:
                return self.turn_on(tile), RIGHT_CHAIN_END
        # Can move to any tail
        else:
            tile = random.choice(tuple(left_end_set.union(right_end_set)))
            if self.check_tile_suit(tile) == LEFT_CHAIN_END:
                if tile[1] == left_num:
                    return tile, LEFT_CHAIN_END
                else:
                    return self.turn_on(tile), LEFT_CHAIN_END
            else:
                if tile[0] == right_num:
                    return tile, RIGHT_CHAIN_END
                else:
                    return self.turn_on(tile), RIGHT_CHAIN_END

    def get_tile_from_bazar(self):
        """ Get tile from bazar """
        if PlayTable.bazar:
            idx = random.randrange(0, len(PlayTable.bazar))
            tile = PlayTable.bazar.pop(idx)
            if self.check_tile_suit(tile):
                return tile
            else:
                self._bones.append(tile)
                self.get_tile_from_bazar()
        else:
            return None

    def check_tile_suit(self, tile):
        """ Is tile suit for game chain ? """
        left_num = self.game.game_chain[0][0]
        right_num = self.game.game_chain[-1][1]
        if left_num == tile[0] or left_num == tile[1]:
            return LEFT_CHAIN_END
        if right_num == tile[0] or right_num == tile[1]:
            return RIGHT_CHAIN_END
        return None

    def move(self):
        """
        Calculate Player move and add tale to game chain if can
        :return: False or True
        """
        if self.nature == 'comp':
            if self.game.batch == 1:
                x = self._bones.index(self.game.first_tile)
                self.game.game_chain.append(self._bones.pop(x))
            else:
                tile, tail = self._ebrain()
                if tile is None:
                    return False
                else:
                    if tail == LEFT_CHAIN_END:
                        self.game.game_chain.insert(0, tile)
                    else:
                        self.game.game_chain.append(tile)
                    return True
        else:
            print('On hand: ', self._bones)
            tile = input('you move:')
            if tile in self._bones:
                if self.check_tile_suit(tile) == LEFT_CHAIN_END:
                    pass
                elif self.check_tile_suit(tile) == RIGHT_CHAIN_END:
                    pass
                else:


            sys.exit(0)


    def get_bone(self):
        num = random.randrange(0, len(PlayTable.bazar))
        bone = PlayTable.bazar.pop(num)
        self._bones.append(bone)

    def i_have(self, tile):
        for i in self._bones:
            if tile == i or self.turn_on(tile) == i:
                return True
        return False


def main():
    """
    read configuration file
    :return:
    """
    random.seed()
    game = PlayTable()
    tally = Account()
    # Defind players and deal the bones
    for i in CONFIG['Players']:
        game.add_player(Player(i, game))
    # Who has (1,1)
    done = False
    for i in DOUBLE_SET + FIRST_HAND:
        for j in game.players_set:
            if j.i_have(i):
                first_hand = game.players_set.index(j)
                game.first_tile = i
                done = True
                break
        if done:
            break
    # Put Players in queue
    q = queue.Queue()
    for i in range(first_hand, len(game.players_set)):
        q.put(game.players_set[i])
    for i in range(first_hand):
        q.put(game.players_set[i])
    # Begin Game
    while not q.empty():
        game.batch += 1
        cur_player = q.get()
        cur_player.move()
        print(game.game_chain)
        if cur_player.nature == 'comp':
            time.sleep(1)
        if game.endtheround():
            tally.countup()
        else:
            q.put(cur_player)

if __name__  == '__main__':
    main()