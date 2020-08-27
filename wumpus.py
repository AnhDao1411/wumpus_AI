from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import time
room_size = 60
img_size = room_size // 5 * 3


def load_level():
    file = "../wumpus/Data/map1.txt"
    with open(file) as f:
        size = int(f.readline())
        cave = [[room for room in row.strip().split('.')]
                for row in f.readlines()]
        wum = [(r, c) for r, row in enumerate(cave)
               for c, room in enumerate(row) if 'W' in room]
        pit = [(r, c) for r, row in enumerate(cave)
               for c, room in enumerate(row) if room == 'P']
        briz = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if 'B' in room]
        sten = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if 'S' in room]
        gold = [(r, c) for r, row in enumerate(cave)
                for c, room in enumerate(row) if 'G' in room]
        agent = [(r, c) for r, row in enumerate(cave)
                 for c, room in enumerate(row) if room == 'A'][0]
    if len(cave) != size:
        raise Exception('Not enough Row')
    for r in cave:
        if len(r) != size:
            raise Exception('Not enough Col')
    return size, cave, wum, pit, briz, sten, gold, agent


class Wumpus:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wumpus.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        window.image += [self.img]
        self.signal = [(self.row - 1, self.col), (self.row + 1, self.col),
                       (self.row, self.col - 1), (self.row, self.col + 1)]

    def display(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)

    def appear(self, window, row, col):
        if row == self.row and col == self.col:
            self.display(window)
            return True
        return False

    def delete(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False

    def same_sig(self, coor):
        for s in self.signal:
            if coor == s:
                return True
        return False

    def check(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False


class Pit:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/hole.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        window.image += [self.img]
        self.signal = [(self.row - 1, self.col), (self.row + 1, self.col),
                       (self.row, self.col - 1), (self.row, self.col + 1)]

    def display(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)

    def appear(self, window, row, col):
        if row == self.row and col == self.col:
            self.display(window)
            return True
        return False

    def check(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False


class Stence:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/smoke.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        window.image += [self.img]
        self.temp = None

    def display(self, window):
        self.temp = window.create_image(room_size // 2 + room_size * self.col + 1,
                                        room_size // 2 + room_size * self.row + 1,
                                        anchor=NW, image=self.img)

    def appear(self, window, row, col):
        if row == self.row and col == self.col:
            self.display(window)
            return True
        return False

    def delete(self, window, row, col):
        if row == self.row and col == self.col:
            window.delete(self.temp)
            window.delete(self.img)
            return True
        return False

    def check(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False


class Gold:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/gold.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        window.image += [self.img]
        self.temp = None

    def display(self, window):
        self.temp = window.create_image(room_size // 2 + room_size * self.col + 1,
                                        room_size // 2 + room_size * self.row + 1,
                                        anchor=NW, image=self.img)

    def appear(self, window, row, col):
        if row == self.row and col == self.col:
            self.display(window)
            return True
        return False

    def delete(self, window, row, col):
        if row == self.row and col == self.col:
            window.delete(self.temp)
            window.delete(self.img)
            return True
        return False

    def check(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False


class Breeze:
    def __init__(self, window, pos):
        self.row, self.col = pos
        self.img = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/wind.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        window.image += [self.img]

    def display(self, window):
        window.create_image(room_size // 2 + room_size * self.col + 1,
                            room_size // 2 + room_size * self.row + 1,
                            anchor=NW, image=self.img)

    def appear(self, window, row, col):
        if row == self.row and col == self.col:
            self.display(window)
            return True
        return False

    def check(self, row, col):
        if row == self.row and col == self.col:
            return True
        return False


class Agent:
    def __init__(self, window, pos, size):
        self.limit = size
        self.window = window
        self.up1 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/up1.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.up2 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/up2.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.down1 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/down1.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.down2 = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/down2.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.left = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/left.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.right = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/right.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
        self.row, self.col = pos
        self.row_og, self.col_og = self.row, self.col
    # direction (Up, Down, Left, Right)
        self.dirc = 'r'
        # current image
        self.current = self.right
        self.window.image += [self.up1, self.up2, self.down1, self.down2,
                              self.left, self.right]

    def appear(self):
        self.img = self.window.create_image(room_size // 2 + room_size * self.col + 1,
                                            room_size // 2 + room_size * self.row + 1,
                                            anchor=NW, image=self.current)

    def is_turn(self, sym):
        if (sym == 'w' and self.dirc != 'u') or (sym == 's' and self.dirc != 'd') or (sym == 'a' and self.dirc != 'l') or (sym == 'd' and self.dirc != 'r'):
            return True
        return False

    def direction(self, sym):
        if sym == 'w':  # up
            if self.dirc != 'u':
                self.dirc = 'u'
                return self.move(self.up1, self.row, self.col)
            else:
                if self.cur == self.up1:  # if already facing up
                    return self.move(self.up2, self.row - 1, self.col)
                return self.move(self.up1, self.row - 1, self.col)
        elif sym == 's':  # down
            if self.dirc != 'd':
                self.dirc = 'd'
                return self.move(self.down1, self.row, self.col)
            else:
                if self.cur == self.down1:  # if already facing down
                    return self.move(self.down2, self.row + 1, self.col)
                return self.move(self.down1, self.row + 1, self.col)
        elif sym == 'a':  # left
            if self.dirc != 'l':
                self.dirc = 'l'
                return self.move(self.left, self.row, self.col)
            return self.move(self.left, self.row, self.col - 1)
        elif sym == 'd':  # right
            if self.dirc != 'r':
                self.dirc = 'r'
                return self.move(self.right, self.row, self.col)
            return self.move(self.right, self.row, self.col + 1)

    def move(self, img, row, col):
        self.window.delete(self.img)
        self.cur = img

        if -1 < row < self.limit and -1 < col < self.limit:
            if row != self.row or col != self.col:
                self.row = row
                self.col = col

        self.img = self.window.create_image(room_size // 2 + room_size * self.col + 1,
                                            room_size // 2 + room_size * self.row + 1,
                                            anchor=NW, image=self.cur)

    def shoot(self):
        return self.dirc


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
        self.step = ImageTk.PhotoImage(Image.open(
            '../wumpus/Img/step.png').resize((room_size - 1, room_size - 1), Image.ANTIALIAS))
# ------------------------------
        Frame.__init__(self, master)
        self.size, self.cave, wum, pit, bree, sten, gold, ag = load_level()
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title('Wumpus')
        self.window = Canvas(self.master, width=room_size * 16,
                             height=room_size * 11, bg='#bea998')
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
        arr_img = [self.step]

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
        self.agent = Agent(self.window, ag, self.size)
        self.wumpus = [Wumpus(self.window, wp) for wp in wum]
        self.pit = [Pit(self.window, p) for p in pit]
        self.bree = [Breeze(self.window, b) for b in bree]
        self.sten = [Stence(self.window, s) for s in sten]
        self.gold = [Gold(self.window, g) for g in gold]
        self.point = 0
        self.t_point = self.window.create_text(
            room_size * 13 + img_size, room_size * 2 + img_size * 2, anchor='center', font=('Purisa', 40), text=str(0))
# Button
        play_but = Button(self.master, width=20,
                          text='Play as Human', command=self.play)
        play_but.place(x=room_size * 12, y=room_size * 6)

        auto_but = Button(self.master, width=20,
                          text='Play as Machine', command=self.auto)
        auto_but.place(x=room_size * 12, y=room_size * 7)

        # Dont know yet
        self.window.pack()
        self.master.mainloop()
# end init

    def play(self):
        self.path(self.agent.row, self.agent.col)
        self.agent.appear()
        self.dis_point(0)

        self.kb_move()

    def auto(self):
        self.path(self.agent.row, self.agent.col)
        self.agent.appear()
        self.dis_point(0)

    def dis_point(self, p):
        self.window.delete(self.t_point)
        self.point += p
        self.t_point = self.window.create_text(
            room_size * 13 + img_size, room_size * 2 + img_size * 2, anchor='center', font=('Purisa', 40), text=str(self.point))
# movement

    def kb_move(self):
        self.ev = Label(self.window)
        self.ev.place(x=room_size * 12, y=room_size * 9)
        self.ev.bind('<w>', self.wasd)
        self.ev.bind('<a>', self.wasd)
        self.ev.bind('<s>', self.wasd)
        self.ev.bind('<d>', self.wasd)
        self.ev.bind('<space>', self.wasd)
        self.ev.bind('<Return>', self.wasd)

        self.ev.focus_set()
        self.ev.bind('<Button-1>', lambda event: self.ev.focus_set())

    def check_wum(self, row, col):
        for i, w in enumerate(self.wumpus):
            if w.delete(row, col):  # if kill wumpus
                w = self.wumpus.pop(i)
                for s in w.signal:  # wumpus stench
                    for wum in self.wumpus:
                        if wum.same_sig(s):  # same stence
                            break
                    else:  # if no other stench in the same place
                        self.sten = [st for st in self.sten if not st.delete(
                            self.window, s[0], s[1])]
                return

    def check_step(self, row, col):
        for w in self.wumpus:
            if w.appear(self.window, row, col):
                self.dis_point(-1000)
                return True
        for p in self.pit:
            if p.appear(self.window, row, col):
                self.dis_point(-1000)
                return True
        for b in self.bree:
            if b.appear(self.window, row, col):
                break
        for s in self.sten:
            if s.appear(self.window, row, col):
                break
        for g in self.gold:
            if g.appear(self.window, row, col):
                break

    def path(self, row, col):
        if -1 < row < self.size and -1 < col < self.size:
            self.window.create_image(room_size // 2 + room_size * col + 1,
                                     room_size // 2 + room_size * row + 1,
                                     anchor=NW, image=self.step)

    def wasd(self, event):
        end = False
        if event.keysym == 'space':
            dr = self.agent.shoot()
            self.dis_point(-100)
            if dr == 'u':  # up
                self.check_wum(self.agent.row - 1, self.agent.col)
            elif dr == 'd':  # down
                self.check_wum(self.agent.row + 1, self.agent.col)
            elif dr == 'l':  # left
                self.check_wum(self.agent.row, self.agent.col - 1)
            elif dr == 'r':  # right
                self.check_wum(self.agent.row, self.agent.col + 1)
        elif event.keysym == 'Return':
            for g in self.gold:
                if g.delete(self.window, self.agent.row, self.agent.col):
                    self.dis_point(100)
                self.gold = [g for g in self.gold if not g.delete(
                    self.window, self.agent.row, self.agent.col)]
        elif not self.agent.is_turn(event.keysym):  # walk into anther room
            self.dis_point(-10)
            if event.keysym == 'w':  # up
                self.path(self.agent.row - 1, self.agent.col)
                end = self.check_step(self.agent.row - 1, self.agent.col)

            elif event.keysym == 's':  # down
                self.path(self.agent.row + 1, self.agent.col)
                end = self.check_step(self.agent.row + 1, self.agent.col)
            elif event.keysym == 'a':  # left
                self.path(self.agent.row, self.agent.col - 1)
                end = self.check_step(self.agent.row, self.agent.col - 1)
            elif event.keysym == 'd':  # right
                self.path(self.agent.row, self.agent.col + 1)
                end = self.check_step(self.agent.row, self.agent.col + 1)
        self.agent.direction(event.keysym)
        if end:
            messagebox.showerror('End Game', 'You Lost')
            self.window.delete('all')
            # Columns table
            [self.window.create_line(room_size // 2 + c * room_size, room_size // 2,
                                     room_size // 2 + c * room_size, room_size // 2 + room_size * 10) for c in range(self.size + 1)]
            # Rows table
            [self.window.create_line(room_size // 2, room_size // 2 + r * room_size,
                                     room_size // 2 + room_size * 10, room_size // 2 + r * room_size) for r in range(self.size + 1)]
            self.master.destroy()
# auto

    def collide(self, row, col):  # return value of the room
        t = self.maze[row][col]

        if 'W' in t:  # can change
            for w in self.wumpus:
                if w.check(row, col):
                    return 'W'
        if 'P' in t:
            return 'P'
        res = ''
        if 'B' in t:
            res += 'B'
        if 'S' in t:  # can change
            for s in self.sten:
                if s.check(row, col):
                    res += 'S'
                    break
        if 'G' in t:  # can change
            for g in self.gold:
                if g.check(row, col):
                    res += 'G'
                    break
        return res

    def run(self):
        map = [[(0, 0, 0) for _ in range(self.size)] for _ in range(self.size)]
        prio = [(self.agent.row, self.agent.col)]
        dirc = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # l, r, u, d
        path = []  # coor + action
        # action: right, left, up, down, walk, die, gold, shoot
        # action is the status of the wumpus at the end of the decision
        stat = 'r'

        while prio:
            # bfs
            r, c = prio[-1][0], prio[-1][1]
            room = collide(r, c)
            # 0 - pit, 1 - wumpus
            if 'W' in room or 'P' in room:
                path += [[(r, c), 'Die']]
                break
            # not out of maze
            area = [d for d in dirc if -1 < r + d[0] <
                    self.size and -1 < c + d[1] < self.size]

            if not map[r][c][2]:  # unvisited
                if 'B' in room:
                    for rt, ct in area:
                        map[r + rt][c + ct][0] += 1
                if 'S' in room:
                    for rt, ct in area:
                        map[r + rt][c + ct][1] += 1
                if 'G' in room:
                    path += [[(r, c), 'Gold']]
            # [coor, num of stench near]

            map[r][c][2] = 1  # visited

            wumpus = [[(r, c), map[r][c][1]] for c in range(self.size)
                      for r in range(self.size) if map[r][c][1] > 0]
            pit = [[(r, c), map[r][c][0]] for c in range(self.size)
                   for r in range(self.size) if map[r][c][0] > 0]

            # for i, (rt, ct) in enumerate(area):
            #     if map[r - rt][c - ct][1] > 1: # 2 stench nearby
            #         if (i == 0 and stat == 'l') or (i == 1 and stat == 'r') or (i == 2 and stat == 'u') or (i == 3 and stat == 'd'):
            #             path += [[(r, c), 'Shoot']]
            #         else:
            #             if i == 0:
            #                 path += [[(r, c), 'Left']]
            #                 path += [[(r, c), 'Shoot']]
            #             elif i == 1:
            #                 path += [[(r, c), 'Right']]
            #                 path += [[(r, c), 'Shoot']]
            #             elif i == 2:
            #                 path += [[(r, c), 'Up']]
            #                 path += [[(r, c), 'Shoot']]
            #             elif i == 3:
            #                 path += [[(r, c), 'Down']]
            #                 path += [[(r, c), 'Shoot']]


load_level()
root = Tk()
game = Game(root)
