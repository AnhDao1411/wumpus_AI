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
        agent = [(r, c) for r, row in enumerate(cave)
                 for c, room in enumerate(row) if room == 'A'][0]
    if len(cave) != size:
        raise Exception('Not enough Row')
    for r in cave:
        if len(r) != size:
            raise Exception('Not enough Col')
    return size, cave, wum, pit, briz, sten, bri_ste, gold, agent


class Agent:
    def __init__(self, window, pos):
        self.window = window
        self.up1 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/up1.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.up2 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/up2.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.down1 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/down1.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.down2 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/down2.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.left = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/left.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.right = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/right.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.step = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/step.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        self.row, self.col = pos
        # direction (Up, Down, Left, Right)
        self.dirc = 'r'
        # current image
        self.current = self.right
        self.window.image += [self.up1, self.up2, self.down1, self.down2,
                              self.left, self.right, self.step]

    def appear(self):
        self.window.create_image(room_size // 2 + room_size * self.col + 1,
                                 room_size // 2 + room_size * self.row + 1,
                                 anchor=NW, image=self.step)

        self.img = self.window.create_image(room_size // 2 + room_size * self.col + 1,
                                            room_size // 2 + room_size * self.row + 1,
                                            anchor=NW, image=self.current)

    def kb_move(self):
        self.ev = Label(self.window, text='last key pressed: ')
        self.ev.place(x=room_size * 12, y=room_size * 9)
        self.ev.bind('<w>', self.wasd)
        self.ev.bind('<a>', self.wasd)
        self.ev.bind('<s>', self.wasd)
        self.ev.bind('<d>', self.wasd)

        self.ev.focus_set()
        self.ev.bind('<1>', lambda event: ev.focus_set())

    def wasd(self, event):
        self.ev.configure(text='last key pressed: ' + event.keysym)
        if event.keysym == 'w':  # up
            if self.dirc != 'u':
                self.dirc = 'u'
                return self.move(self.up1)
            else:
                if self.cur == self.up1:  # if already facing up
                    return self.move(self.up2)
                return self.move(self.up1)
        elif event.keysym == 's':  # down
            if self.dirc != 'd':
                self.dirc = 'd'
                return self.move(self.down1)
            else:
                if self.cur == self.down1:  # if already facing down
                    return self.move(self.down2)
                return self.move(self.down1)
        elif event.keysym == 'a':  # left
            if self.dirc != 'l':
                self.dirc = 'l'
            return self.move(self.left)
        elif event.keysym == 'd':  # right
            if self.dirc != 'r':
                self.dirc = 'r'
            return self.move(self.right)

    def move(self, img):
        self.window.delete(self.img)
        self.cur = img
        self.img = self.window.create_image(room_size // 2 + room_size * self.col + 1,
                                            room_size // 2 + room_size * self.row + 1,
                                            anchor=NW, image=self.cur)


class Wumpus:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wumpus.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


class Pit:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/hole.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


class Stence:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/smoke.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


class Gold:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/gold.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


class Breeze:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wind.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


class Briste:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/mix.png').resize((room_size - 3, room_size - 3), Image.ANTIALIAS))
        window.image += [self.img]

    def appear(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)


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
        self.size, self.cave, wum, pit, bree, sten, briste, gold, ag = load_level()
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('Wumpus')
        self.window = Canvas(self.master, width=room_size * 16,
                             height=room_size * 11, bg='#fffcb7')
        self.window.image = []
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
        self.agent = Agent(self.window, ag)
        self.wumpus = [Wumpus(self.window, wp) for wp in wum]
        self.pit = [Pit(self.window, p) for p in pit]
        self.bree = [Breeze(self.window, b) for b in bree]
        self.sten = [Stence(self.window, s) for s in sten]
        self.briste = [Briste(self.window, s) for s in briste]
        self.gold = [Gold(self.window, g) for g in gold]

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
        self.agent.appear()
        [w.appear(self.window) for w in self.wumpus]
        [pit.appear(self.window) for pit in self.pit]
        [bri.appear(self.window) for bri in self.bree]
        [s.appear(self.window) for s in self.sten]
        [g.appear(self.window) for g in self.gold]
        [bs.appear(self.window) for bs in self.briste]
        self.agent.kb_move()
    # click reset button

    def reset(self):
        pass


load_level()
root = Tk()
game = Game(root)
