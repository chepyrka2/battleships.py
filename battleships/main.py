
import arcade as a
import arcade.gui as ag
import arcade.color as ac
import math as m

click_sound = a.load_sound('sounds/clicksoundeffect.mp3')
miss_sound = a.load_sound('sounds/cannon-water-splash.mp3')
hit_sound = a.load_sound('sounds/explosion_old.mp3')
kill_sound = a.load_sound('sounds/kill.m4a')
win_sound = a.load_sound('sounds/victory_fanfare.mp3')
song = a.load_sound('sounds/Aphex--online-audio-convert.com.wav')

mediaplayer = song.play(0.3, loop=True)

celldef = {None: None, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}

firstplayerboard = [['']*10 for x in range (10)]
secondplayerboard = [['']*10 for x in range (10)]
firstplayerguessboard = [['']*10 for x in range (10)]
secondplayerguessboard = [['']*10 for x in range (10)]

shipsize = 1
volumes = [0, 0.2, 0.3, 0.5, 0.7, 1]
volumeindex = 5
volume = volumes[volumeindex]

ships1 = []
ships2 = []

background = a.load_texture("sprites/e5527200664b93c1474bcc79f06bd999.jpg")

class ShipPlace(a.Sprite):
    def __init__(self, x ,y, sizee, ori, id):
        if sizee == 1:
            self.spritepath = 'sprites/1cell.png'
        elif sizee == 2:
            self.spritepath = 'sprites/2cell.png'
        elif sizee == 3:
            self.spritepath = 'sprites/3cell.png'
        elif sizee == 4:
            self.spritepath = 'sprites/4cell.png'
        if ori == 'vertical':
            self.ang = 90
        elif ori == 'horizontal':
            self.ang = 0
        self.startx = x
        self.starty = y
        self.x=x
        self.y=y
        self.ssize=sizee
        self.ori = ori
        self.id = id
        self.is_put = False
        self.is_pressed = False
        self.margin = sizee*25-25

        self.cells = []
        if self.ori == 'vertical':
            self.xmargin = 0
            self.ymargin = self.margin
        else:
            self.ymargin = 0
            self.xmargin = self.margin
        super().__init__(self.spritepath, shipsize, center_x=x, center_y=y, angle=self.ang)

    def check(self, x, y, id):
        def is_empty(nx, ny):
            if nx < 0 or nx >= 10 or ny < 0 or ny >= 10:
                return False
            if id == 1:
                return firstplayerboard[ny][nx] == ''
            elif id == 2:
                return secondplayerboard[ny][nx] == ''
            return False

        for i in range(self.ssize):
            if self.ori == 'horizontal':
                nx = x + i
                ny = y
            else:
                nx = x
                ny = y + i
            if not is_empty(nx, ny):
                return False
        return True


    def place(self, x, y):

        if not self.check(x, y, self.id):
            self.center_y = self.starty
            self.center_x = self.startx
            return
        if self.ori == 'horizontal' and x + self.ssize > 10:
            self.center_y = self.starty
            self.center_x = self.startx
            return

        if self.ori == 'vertical' and y + self.ssize > 10:
            self.center_y = self.starty
            self.center_x = self.startx
            return
        if self.id == 1:
            for i in range(self.ssize):
                if self.ori == 'horizontal':
                    nx = x + i
                    ny = y
                else:
                    nx = x
                    ny = y + i
                self.cells.append([ny, nx])
                firstplayerboard[ny][nx] = 'S'

            for i in range(-1, self.ssize + 1):
                for j in [-1, 0, 1]:
                    if self.ori == 'horizontal':
                        bx = x + i
                        by = y + j
                    else:
                        bx = x + j
                        by = y + i
                    if 0 <= bx < 10 and 0 <= by < 10 and firstplayerboard[by][bx] == '':
                        firstplayerboard[by][bx] = '.'
        else:
            for i in range(self.ssize):
                if self.ori == 'horizontal':
                    nx = x + i
                    ny = y
                else:
                    nx = x
                    ny = y + i
                self.cells.append([ny, nx])
                secondplayerboard[ny][nx] = 'S'

            for i in range(-1, self.ssize + 1):
                for j in [-1, 0, 1]:
                    if self.ori == 'horizontal':
                        bx = x + i
                        by = y + j
                    else:
                        bx = x + j
                        by = y + i
                    if 0 <= bx < 10 and 0 <= by < 10 and secondplayerboard[by][bx] == '':
                        secondplayerboard[by][bx] = '.'
        print("Поставлен корабль:", self.cells)
        print("На доске:", firstplayerboard if self.id == 1 else secondplayerboard)
        if self.id == 1:
            ships1.append(self.cells)
        else:
            ships2.append(self.cells)
        self.is_put = True
        print("После размещения:")
        print("ships1 =", ships1)
        print("ships2 =", ships2)
        click_sound.play(volume)





class MainWin(a.Window):
    def __init__(self, w, h, t):
        super().__init__(w, h, t)
        self.w = w
        self.h = h
        self.mv = MenuView()
        self.cv1 = ChoseView(1)
        self.cv2 = ChoseView(2)
        self.gv1 = GameView(1)
        self.gv2 = GameView(2)
        self.show_view(self.mv)
        self.cv1.window = self



class MenuView(a.View):
    def __init__(self):
        super().__init__()
        self.w = self.window.width
        self.h = self.window.height
        self.manager = ag.UIManager()
        self.manager.enable()
        button = ag.UIFlatButton(text="Играть")
        self.manager.add(button)

        @button.event("on_click")
        def ts(x):
            click_sound.play(volume)
            self.window.show_view(self.window.cv1)
    def on_draw(self):
        self.clear()
        a.set_background_color(ac.WHITE)
        a.draw_text("Морской бой", self.w//2, self.h//2, ac.BLACK, 20)
        self.manager.draw()
        a.draw_text('Esc - выход из игры (работает везде)', 0, 479, ac.BLACK, 20)
        a.draw_text(f'Громкость: {volume}. ↓ - понизить громкость, ↑ - повыысить', 100, 5, ac.BLACK, 16)
    def on_key_press(self, key, mods):
        global volumeindex, volume
        if key == a.key.ESCAPE:
            a.close_window()
            mediaplayer.pause()
            exit(13)
        if key == a.key.UP:
            if volumeindex < 5:
                volumeindex += 1
                volume = volumes[volumeindex]
                click_sound.play(volume)
        if key == a.key.DOWN:
            if volumeindex > 0:
                volumeindex -= 1
                volume = volumes[volumeindex]
                click_sound.play(volume)
    def on_update(self, delta_time):
        global volume
        volume = volumes[volumeindex]

class ChoseView(a.View):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.manager = ag.UIManager()
        self.manager.enable()
        self.xmouse = 0
        self.ymouse = 0
        self.shiplist = a.SpriteList()
        self.onef = ShipPlace(50, 30, 1, 'horizontal', self.id)
        self.ones = ShipPlace(100, 30, 1, 'horizontal', self.id)
        self.onet = ShipPlace(50, 80, 1, 'horizontal', self.id)
        self.onefo = ShipPlace(100, 80, 1, 'horizontal', self.id)
        self.twof = ShipPlace(60, 140, 2, 'horizontal', self.id)
        self.twos = ShipPlace(160, 140, 2, 'horizontal', self.id)
        self.twot = ShipPlace(60, 190, 2, 'horizontal', self.id)
        self.threef = ShipPlace(80, 250, 3, 'horizontal', self.id)
        self.threes = ShipPlace(80, 300, 3, 'horizontal', self.id)
        self.four = ShipPlace(110, 420, 4, 'horizontal', self.id)
        self.shiplist.append(self.onef)
        self.shiplist.append(self.ones)
        self.shiplist.append(self.onet)
        self.shiplist.append(self.onefo)
        self.shiplist.append(self.twof)
        self.shiplist.append(self.twos)
        self.shiplist.append(self.twot)
        self.shiplist.append(self.threef)
        self.shiplist.append(self.threes)
        self.shiplist.append(self.four)

    def reset(self):
        global firstplayerboard, secondplayerboard, ships2, ships1
        if self.id == 1:
            firstplayerboard = [[''] * 10 for x in range(10)]
            ships1.clear()
        else:
            secondplayerboard = [['']*10 for x in range (10)]
            ships2.clear()
        for ship in self.shiplist:
            ship.center_x = ship.startx
            ship.center_y = ship.starty
            ship.ori = 'horizontal'
            ship.angle = 0
            ship.ymargin = ship.margin
            ship.xmargin = 0
            ship.is_put = False
            ship.cells = []

        click_sound.play(volume)



    def draw_board(self):
        cellsize = self.window.h / 10
        margin = 0.5 * (self.window.w - 10 * cellsize)
        a.draw_lbwh_rectangle_filled(margin, 0, cellsize * 10, cellsize * 10, ac.BUD_GREEN)
        for i in range(10):
            a.draw_lbwh_rectangle_outline(margin + i * cellsize, 0, cellsize, 10 * cellsize, ac.WHITE, 3)
        for i in range(10):
            a.draw_lbwh_rectangle_outline(margin, i * cellsize, 10 * cellsize, cellsize, ac.WHITE, 3)

    def on_draw(self):
        self.clear()
        a.set_background_color(ac.WHITE)
        a.draw_texture_rect(
            background,
            a.LBWH(0, 0, 1000, 500),
        )
        self.manager.draw()
        self.draw_board()
        self.shiplist.draw()
        a.draw_text(self.id, 975, 400, ac.WHITE, 14)
        a.draw_text('Backspace - обнулить доску', 751, 80, ac.WHITE, 13)
        a.draw_text('Enter - закончить расстановку', 751, 50, ac.WHITE, 13)


    def closest_cell_raw(self):
        cellsize = self.window.h / 10
        margin = 0.5 * (self.window.w - 10 * cellsize)
        x = m.ceil((self.xmouse - margin) / cellsize)

        if (x < 1) or (x > 10):
            x = None

        try:

            y = m.ceil(self.ymouse / cellsize)
            if (y < 1)  or (y > 10):
                y = None
        except BaseException as e:
            y = m.ceil(self.ymouse / cellsize)

        if (x == None) or (y == None):
            x = None
            y = None

        return [celldef[y], x]

    def on_mouse_motion(self, x, y, dx, dy):
        self.xmouse = x
        self.ymouse = y
    def on_update(self, delta_time):
        if self.id == 1:
            pass
        else:
            pass
        for ship in self.shiplist:
            if ship.is_pressed == True:
                if ship.ori == 'horizontal' :
                    ship.center_y = self.ymouse
                    ship.center_x = self.xmouse + ship.margin
                else:
                    ship.center_x = self.xmouse
                    ship.center_y = self.ymouse + ship.margin
        for ship in self.shiplist:
            if ship.ori == 'vertical':
                ship.ang = 0
            elif ship.ori == 'horizontal':
                ship.ang = 90

    def on_mouse_press(self, x, y, btn, mods):
        click_sound.play(volume)
        for ship in self.shiplist:
            if (ship.collides_with_point((x, y))) and (not ship.is_put) :
                ship.is_pressed = True

    def on_mouse_release(self, x, y, btn, mods):
        for ship in self.shiplist:
            if ship.is_pressed:
                ship.is_pressed = False

                if self.closest_cell_raw() != [None, None]:

                    cellsize = self.window.h / 10
                    margin = 0.5 * (self.window.w - 10 * cellsize)
                    grid_x = int((x - margin) // cellsize)
                    grid_y = int(y // cellsize)
                    

                    if ship.ori == 'horizontal':
                        ship.center_x = margin + grid_x * cellsize + (cellsize * ship.ssize) / 2
                        ship.center_y = grid_y * cellsize + cellsize / 2
                    else:
                        ship.center_x = margin + grid_x * cellsize + cellsize / 2
                        ship.center_y = grid_y * cellsize + (cellsize * ship.ssize) / 2
                    ship.place(grid_x, grid_y)

                else:
                    ship.center_x = ship.startx
                    ship.center_y = ship.starty


    def on_key_press(self, key, mods):
        is_complete = True
        if key == a.key.R:
            for ship in self.shiplist:
                if ship.is_pressed:
                    if ship.ori == 'vertical':
                        ship.ori = 'horizontal'
                        ship.angle = 0
                        ship.ymargin = ship.margin
                        ship.xmargin = 0
                    else:
                        ship.ori = 'vertical'
                        ship.angle = 90
                        ship.ymargin = 0
                        ship.xmargin = ship.margin
            click_sound.play(volume)
        if key == a.key.BACKSPACE:
            self.reset()
        if key == a.key.ESCAPE:
            a.close_window()
            mediaplayer.pause()
            exit(13)
        if key == a.key.ENTER:
            click_sound.play(volume)
            for ship in self.shiplist:
                if not ship.is_put:
                    is_complete = False
            if is_complete:
                if self.id == 1:
                    self.window.show_view(self.window.cv2)

                else:
                    self.window.show_view(self.window.gv1)
        if key == a.key.E:
            if self.id == 1:
                self.window.show_view(self.window.cv2)

            else:
                self.window.show_view(self.window.gv1)



class GameView(a.View):

    def __init__(self, id):
        super().__init__()
        self.id = id

        if self.id == 1:
            self.myboard = firstplayerboard
            self.enemyboard = secondplayerboard
            self.guessboard = firstplayerguessboard
            self.enemyships = ships2
        if self.id == 2:
            self.myboard = secondplayerboard
            self.enemyboard = firstplayerboard
            self.guessboard = secondplayerguessboard
            self.enemyships = ships1
        self.xmouse = 0
        self.ymouse = 0
        self.delay_timer = 0
        self.waiting = False
        self.delay_timer2 = 0
        self.waiting2 = False
        self.win = WinView(self.id)
    def on_show_view(self):
        print(firstplayerboard)
        print(secondplayerboard)
    def check_death(self, ship):
        for y, x in ship:
            if self.enemyboard[y][x] != 'X':
                return False
        print(firstplayerboard)
        print(secondplayerboard)
        return True
    def check_board(self):
        for y in self.enemyboard:
            for x in y:
                if x == 'S':
                    return False
        return True

    def draw_board(self):
        cellsize = self.window.h / 10
        margin = 0.5 * (self.window.w - 10 * cellsize)
        a.draw_lbwh_rectangle_filled(margin, 0, cellsize * 10, cellsize * 10, ac.BUD_GREEN)
        for y in range(10):
            for x in range(10):
                # self.print_board(self.guessboard)
                symbol = self.guessboard[y][x]
                if symbol == 'X':
                    a.draw_lbwh_rectangle_filled(margin + x * cellsize, cellsize * y, cellsize, cellsize, ac.RED)
                elif symbol == '.':
                    a.draw_lbwh_rectangle_filled(margin + x * cellsize, cellsize * y, cellsize, cellsize, ac.LIGHT_BLUE)
                elif symbol == '-':
                    a.draw_lbwh_rectangle_filled(margin + x * cellsize, cellsize * y, cellsize, cellsize, ac.BLACK)
                a.draw_lbwh_rectangle_outline(margin + x * cellsize, cellsize * y, cellsize, cellsize, ac.WHITE, 3)

    def on_draw(self):
        self.clear()
        a.draw_texture_rect(
            background,
            a.LBWH(0, 0, 1000, 500),
        )

        self.draw_board()
        a.draw_text(self.id, 20, 400, ac.WHITE, 16)
        a.set_background_color(ac.WHITE)
    def on_mouse_press(self, x, y, btn, mods):
        print(firstplayerboard)
        print(secondplayerboard)
        played = False
        cellsize = self.window.h / 10
        margin = 0.5 * (self.window.w - 10 * cellsize)
        grid_x = int((x - margin) // cellsize)
        grid_y = int(y // cellsize)
        if not self.waiting:
            if ((grid_x >= 10) or (grid_x < 0)) or ((grid_y >= 10) or (grid_y < 0)):
                return
            if self.guessboard[grid_y][grid_x] != '':
                return
            print("Попытка выстрела по:", grid_y, grid_x)
            print("Враг. поле:", self.enemyboard[grid_y][grid_x])
            if self.enemyboard[grid_y][grid_x] == 'S':
                self.guessboard[grid_y][grid_x] = 'X'
                self.enemyboard[grid_y][grid_x] = 'X'
                if self.check_board():
                    self.window.show_view(self.win)
                for ship in self.enemyships:
                    if self.check_death(ship):
                        played = True
                        for cell in ship:
                            self.enemyboard[cell[0]][cell[1]] = '-'
                            self.guessboard[cell[0]][cell[1]] = '-'
                if played:
                    kill_sound.play(volume)
                else:
                    hit_sound.play(volume)

            else:
                self.guessboard[grid_y][grid_x] = '.'
                self.waiting = True
                miss_sound.play(volume)
    def on_update(self, delta_time):
        if self.waiting:
            self.delay_timer += delta_time
            if self.delay_timer > 1.2:
                self.waiting = False
                self.delay_timer = 0

                if self.id == 1:
                    self.window.show_view(self.window.gv2)
                else:
                    self.window.show_view(self.window.gv1)

    def on_key_press(self, key, mods):
        if key == a.key.ESCAPE:
            a.close_window()
            mediaplayer.pause()
            exit(13)

class WinView(a.View):
    def __init__(self, id):
        super().__init__()
        self.id = id
    def on_show_view(self):
        win_sound.play(volume)
    def on_draw(self):
        self.clear()
        a.set_background_color(ac.WHITE)
        a.draw_text(f'Победил игрок {self.id}!', 500-30*(len('Победил игрок 1!')//2), 250, ac.BLACK, 30, align='center')
    def on_key_press(self, key, mods):
        if key == a.key.ESCAPE:
            a.close_window()
            mediaplayer.pause()

win = MainWin(1000, 500, "Battleships")
a.run()