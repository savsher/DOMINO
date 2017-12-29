#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import queue

DOMINO_SET = [(i, j) for i in range(7) for j in range(7) if j >= i]
CONFIG = []

class PlayTable(object):
    def __init__(self):
        _domino_set = DOMINO_SET
        play_set = list()
        players = list()

class Bazar(object):
    def __init__(self):
        pass

class Player(object):
    def __init__(self, type ):
        self._bones = list()
        self._players = list()
        self._draw = list()
    def move(self):
        pass
    def get_bone(self):
        pass
    def add_player(self, pl):

        pass

def main():
    """
    read configuration file
    :return:
    """
    p1 = Player('M')
    p2 = Player('M')
    p3 = Player('M')
    p4 = Player('H')

    m = PlayTable()

    q = queue.Queue()
    for i in range(4):
        q.put(i)
    while not q.empty():
        z = q.get()
        print(z)
        if z == x3:
            break
        q.put(z)

if __name__  == '__main__':
    main()