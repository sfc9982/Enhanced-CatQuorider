import pygame as pg
import random


def main():

    pg.init()
    screen = pg.display.set_mode((800, 600))
    myFont1 = pg.font.Font(None, 120)
    icon = pg.image.load("cat.png")
    pg.display.set_icon(icon)
    pg.display.set_caption("圈住小猫")
    fps = 30
    fclock = pg.time.Clock()

    white = 255, 255, 255
    black = 0, 0, 0
    green = 200, 255, 100
    green_gray = 120, 155, 0
    blue = 0, 0, 255
    red = 255, 0, 0
    textImage1 = myFont1.render('you lost!', True, red)
    textImage2 = myFont1.render('you win!', True, blue)
    position = [50, 60]
    radius = 25
    crcs = []
    wins = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 21: 0, 22: 0, 32: 0, 33: 0, 43: 0, 44: 0, 54: 0, 55: 0, 65: 0,
            66: 0, 76: 0, 77: 0, 87: 0, 88: 0, 98: 0, 99: 0, 109: 0, 110: 0, 111: 0, 112: 0, 113: 0, 114: 0, 115: 0, 116: 0, 117: 0, 118: 0, 119: 0, 120: 0}
    done = False

    class crc:
        def __init__(self, x, y, alive):
            self.x = x
            self.y = y
            self.num = self.x + self.y * 11
            self.alive = alive
            position[1] = 60 + y * 50
            if y % 2 == 0:
                position[0] = 100 + x * 58
            else:
                position[0] = 130 + x * 58
            pg.draw.circle(screen, green, position, radius)
            pg.display.update()

        def Draw_crc(self, _x, _y, aly):
            self.y = _y
            self.x = _x
            if (self.y % 2) == 0:
                position[0] = 100 + self.x * 58
            else:
                position[0] = 130 + self.x * 58
            position[1] = 60 + self.y * 50
            if self.alive == 0 and aly == 1:
                pg.draw.circle(screen, green_gray, position, radius)
            elif aly == 2:
                pg.draw.circle(screen, black, position, radius)
            elif aly == 0:
                pg.draw.circle(screen, green, position, radius)
            self.alive = aly
            pg.display.update()

        def is_crc_aly(self):
            if self.alive == 0:
                return 1
            else:
                return 0

    class cat:
        def __init__(self, pos):
            self.pos = pos
            self.num = pos[0] + pos[1]*11
            self.done = False
            self._last = 60

        def get_pass(self, num):
            ways = []
            gi = [1, -1, 11, -11]
            for i in gi:
                if crc.is_crc_aly(crcs[num + i]):
                    ways.append(crcs[num+i])
            if self.pos[1] % 2 == 0:
                if crc.is_crc_aly(crcs[num+10]):
                    ways.append(crcs[num+10])
                if crc.is_crc_aly(crcs[num-12]):
                    ways.append(crcs[num-12])
            else:
                if crc.is_crc_aly(crcs[num+12]):
                    ways.append(crcs[num+12])
                if crc.is_crc_aly(crcs[num-10]):
                    ways.append(crcs[num-10])
            return ways

        def get_map(self):
            open = {}
            pp = []
            ppp = []
            s = self.num
            p = self.get_pass(s)
            open[s] = 0

            for i in range(0, len(p)):
                if wins.__contains__(p[i].num) and p[i].num != self._last:
                    return p[i].num, open
                open[p[i].num] = s
                pp.append(p[i].num)
            for rr in range(0, 15):
                for i in range(0, len(pp)):
                    if not (wins.__contains__(pp[i])):
                        p = self.get_pass(pp[i])
                        for j in range(0, len(p)):
                            if not (open.__contains__(p[j].num)):
                                if wins.__contains__(p[j].num) and p[j].num != self._last:
                                    return pp[i], open
                                open[p[j].num] = pp[i]
                                ppp.append(p[j].num)
                del pp[:]
                for i in range(0, len(ppp)):
                    if not (wins.__contains__(ppp[i])):
                        p = self.get_pass(ppp[i])
                        for j in range(0, len(p)):
                            if not (open.__contains__(p[j].num)):
                                if wins.__contains__(p[j].num) and p[j].num != self._last:
                                    return ppp[i], open
                                open[p[j].num] = ppp[i]
                                pp.append(p[j].num)
                del ppp[:]
            return None

        def cat_mov(self):
            if self.num == 60 or self.get_map() == None:
                if self.num < 11 or self.num > 109 or self.num % 11 == 0 or self.num % 11 == 10:
                    screen.blit(textImage1, (100, 100))
                    self.done = True
                else:
                    paths = self.get_pass(self.num)
                    if len(paths) == 0:
                        screen.blit(textImage2, (100, 100))
                        self.done = True
                    else:
                        s = random.randint(0, len(paths)-1)
                        crc.Draw_crc(crcs[self.num],
                                     self.pos[0], self.pos[1], 0)
                        self.pos[0] = paths[s].x
                        self.pos[1] = paths[s].y
                        self.num = self.pos[0] + self.pos[1] * 11
                        crc.Draw_crc(paths[s], self.pos[0], self.pos[1], 2)
            else:
                way, opens = self.get_map()
                path = way
                if opens.__contains__(way):
                    if opens[way] != 0:
                        while opens[way] != 0:
                            path = way
                            way = opens[way]
                crc.Draw_crc(crcs[self.num], self.pos[0], self.pos[1], 0)
                self._last = self.num
                self.num = path
                self.pos[0] = path % 11
                self.pos[1] = int(path / 11)
                crc.Draw_crc(crcs[path], self.pos[0], self.pos[1], 2)
                if self.num < 11 or self.num > 109 or self.num % 11 == 0 or self.num % 11 == 10:
                    screen.blit(textImage1, (100, 100))
                    self.done = True

    screen.fill(white)
    for j in range(0, 11):
        for i in range(0, 11):
            r = crc(i, j, 0)
            crcs.append(r)
    rand = random.randint(3, 13)
    for pp in range(0, rand):
        rands = random.randint(0, 120)
        if rands != 60:
            r_x = rands % 11
            r_y = int(rands / 11)
            crc.Draw_crc(crcs[rands], r_x, r_y, 1)
    cat = cat([5, 5])
    s = cat.pos[0] + cat.pos[1] * 11
    crc.Draw_crc(crcs[s], cat.pos[0], cat.pos[1], 2)

    while done == False:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
            elif e.type == pg.MOUSEBUTTONUP:
                if cat.done == False:
                    if e.button == 1:
                        if e.pos[1] > 35 and e.pos[1] < 585 and e.pos[0] > 75 and e.pos[0] < 753:
                            _y = int((e.pos[1] - 35) / 50)
                            if (_y % 2) == 0:
                                _x = int((e.pos[0] - 75) / 58)
                            else:
                                _x = int((e.pos[0] - 115) / 58)
                            if _x < 11:
                                f = _y*11+_x
                                if(crc.is_crc_aly(crcs[f]) == 1):
                                    crc.Draw_crc(crcs[f], _x, _y, 1)
                                    cat.cat_mov()
                else:
                    done = True
        pg.display.update()
        fclock.tick(fps)
    main()


if __name__ == "__main__":
    main()
