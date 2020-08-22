from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
block_size = 60


def load_level():
    file = "./Data/map1.txt"
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


class Game(Frame):
    def play(self):
        print('hello')
        pass

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('Wumpus')
        self.window = Canvas(self.master, width=block_size * 16,
                             height=block_size * 11, bg='#fffcb7')
        # cols
        [self.window.create_line(block_size // 2 + c * block_size, block_size // 2,
                                 block_size // 2 + c * block_size, block_size // 2 + block_size * 10) for c in range(11)]
        # rows
        [self.window.create_line(block_size // 2, block_size // 2 + r * block_size,
                                 block_size // 2 + block_size * 10, block_size // 2 + r * block_size) for r in range(11)]
        # game name
        c = ImageTk.PhotoImage(Image.open(
            './Img/letter_c.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        e = ImageTk.PhotoImage(Image.open(
            './Img/letter_e.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        h = ImageTk.PhotoImage(Image.open(
            './Img/letter_h.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        m = ImageTk.PhotoImage(Image.open(
            './Img/letter_m.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        n = ImageTk.PhotoImage(Image.open(
            './Img/letter_n.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        o = ImageTk.PhotoImage(Image.open(
            './Img/letter_o.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        p = ImageTk.PhotoImage(Image.open(
            './Img/letter_p.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        r = ImageTk.PhotoImage(Image.open(
            './Img/letter_r.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        s = ImageTk.PhotoImage(Image.open(
            './Img/letter_s.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        t = ImageTk.PhotoImage(Image.open(
            './Img/letter_t.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        u = ImageTk.PhotoImage(Image.open(
            './Img/letter_u.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))
        w = ImageTk.PhotoImage(Image.open(
            './Img/letter_w.jpg').resize((block_size * 3 // 5, block_size * 3 // 5), Image.ANTIALIAS))

        switcher = {'c': c, 'e': e, 'h': h, 'm': m, 'n': n, 'o': o, 'p': p,
                    'r': r, 's': s, 't': t, 'u': u, 'w': w}
        arr_img = []

        word = 'hunt the wumpus'
        for i, letter in enumerate(word):
            if letter == ' ':
                continue
            else:
                arr_img += [Label(self.master, image=switcher[letter])]
                arr_img[-1].place(x=block_size // 2 + 1 + block_size * 10,
                                  y=block_size + block_size * 3 // 5 * i)

        word = 'score'
        for i, letter in enumerate(word):
            arr_img += [Label(self.master, image=switcher[letter])]
            arr_img[-1].place(x=block_size * 12 + block_size * 3 // 5 * i,
                              y=block_size * 2)

        play_but = Button(self.master, text='Play', command=self.play())
        play_but.place(x=block_size * 13, y=block_size * 5)

        self.window.pack()
        self.master.mainloop()


load_level()
root = Tk()
game = Game(root)
