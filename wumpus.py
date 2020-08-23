from tkinter import *
from PIL import Image, ImageTk
room_size = 60
img_size = room_size // 5 * 3


def load_level():
    file = "../wumpus/Data/map1.txt"
    with open(file) as f:
        size = int(f.readline())
        cave = [[room for room in row.strip().split('.')]
                for row in f.readlines()]
        wum = [(r, c) for r, row in enumerate(cave)
               for c, room in enumerate(row) if room == 'W']
        pit = [(r, c) for r, row in enumerate(cave)
               for c, room in enumerate(row) if room == 'P']
        briz = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if room == 'B']
        sten = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if room == 'S']
        bri_ste = [(r, c) for r, row in enumerate(cave)
                   for c, room in enumerate(row) if room == 'BS']
        gold = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if room == 'G']
    if len(cave) != size:
        raise Exception('Not enough Row')
    for r in cave:
        if len(r) != size:
            raise Exception('Not enough Col')
    return size, cave, wum, pit, briz, sten, bri_ste, gold


class Wumpus:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wumpus.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)
    # plus 1 to make pic in middle


class Pit:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/hole.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)
        # plus 1 to make in middle


class Stence:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/smoke.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)


class Gold:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/gold.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)


class Breeze:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wind.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)


class Briste:
    def __init__(self, master, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/mix.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.label = Label(master, image=self.img)

    def appear(self):
        self.label.place(x=room_size // 2 + room_size * self.col + 1,
                         y=room_size // 2 + room_size * self.row + 1)


class Game(Frame):
    def __init__(self, master=None):
        c = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_c.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        e = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_e.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        h = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_h.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        m = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_m.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        n = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_n.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        o = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_o.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        p = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_p.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        r = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_r.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        s = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_s.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        t = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_t.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        u = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_u.jpg').resize((img_size, img_size), Image.ANTIALIAS))
        w = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/letter_w.jpg').resize((img_size, img_size), Image.ANTIALIAS))
# ------------------------------

        Frame.__init__(self, master)
        self.size, self.cave, wum, pit, bree, sten, briste, gold = load_level()
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('Wumpus')
        self.window = Canvas(self.master, width=room_size * 16,
                             height=room_size * 11, bg='#fffcb7')
        # Columns table
        [self.window.create_line(room_size // 2 + c * room_size, room_size // 2,
                                 room_size // 2 + c * room_size, room_size // 2 + room_size * 10) for c in range(self.size + 1)]
        # Rows table
        [self.window.create_line(room_size // 2, room_size // 2 + r * room_size,
                                 room_size // 2 + room_size * 10, room_size // 2 + r * room_size) for r in range(self.size + 1)]

# Text in game
        switcher = {'c': c, 'e': e, 'h': h, 'm': m, 'n': n, 'o': o, 'p': p,
                    'r': r, 's': s, 't': t, 'u': u, 'w': w}
        arr_img = []

        word = 'hunt the wumpus'
        for i, letter in enumerate(word):
            if letter == ' ':
                continue
            else:
                arr_img += [Label(self.master, image=switcher[letter])]
                arr_img[-1].place(x=room_size // 2 + 1 + room_size * 10,
                                  y=room_size + img_size * i)

        word = 'score'
        for i, letter in enumerate(word):
            arr_img += [Label(self.master, image=switcher[letter])]
            arr_img[-1].place(x=room_size * 12 + img_size * i,
                              y=room_size * 2)

# Variable
        self.wumpus = [Wumpus(self.master, wp) for wp in wum]
        self.pit = [Pit(self.master, p) for p in pit]
        self.bree = [Breeze(self.master, b) for b in bree]
        self.sten = [Stence(self.master, s) for s in sten]
        self.briste = [Briste(self.master, s) for s in briste]
        self.gold = [Gold(self.master, g) for g in gold]

        # Button
        play_but = Button(self.master, width=20,
                          text='Play', command=self.play)
        play_but.place(x=room_size * 12, y=room_size * 6)

        res_but = Button(self.master, width=20,
                         text='Reset', command=self.reset)
        res_but.place(x=room_size * 12, y=room_size * 6 + img_size)

        # Dont know yet
        self.window.pack()
        self.master.mainloop()

    # click play button
    def play(self):
        self.wumpus[0].appear()
        [pit.appear() for pit in self.pit]
        [bri.appear() for bri in self.bree]
        [s.appear() for s in self.sten]
        [g.appear() for g in self.gold]
        [bs.appear() for bs in self.briste]
    # click reset button

    def reset(self):
        pass


load_level()
root = Tk()
game = Game(root)
