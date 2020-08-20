import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from random import randint
block_size = 25


def load_level():
    file = "../wumpus/Data/map1.txt"
    with open(file) as f:
        size = int(f.readline())
        cave = [[room for room in row.strip().split('.')]
                for row in f.readlines()]
    if len(cave) != size:
        raise Exception('Not enough Row')
    for r in cave:
        if len(r) != size:
            raise Exception('Not enough Col')

    return size, cave


class Game():
    pass


load_level()
