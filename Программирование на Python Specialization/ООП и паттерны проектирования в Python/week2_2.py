import math
import pygame
import random
from polylines import Polyline, Knot
from vector import Vec2d

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        if type(x) is tuple:
            self.x = y[0] - x[0]
            self.y = y[1] - x[1]
        else:
            self.x = x
            self.y = y

    def __sub__(self, v):  # разность двух векторов
        return Vec2d(self.x - v.x, self.y - v.y)

    def __add__(self, v):  # сумма двух векторов
        return Vec2d(self.x + v.x, self.y + v.y)

    def __radd__(self, v):  # прибавить вектор
        self.x += v.x
        self.y += v.y

    def __len__(self):  # длина вектора
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, z):
        if type(z) is Vec2d:  # скалярное умножение вектора на число
            return self.x * z.x + self.y * z.y
        else:  # умножение вектора на число
            return Vec2d(z * self.x, z * self.y)

    def __rmul__(self, z):
        return Vec2d(z * self.x, z * self.y)

    def int_pair(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Polyline:

    def __init__(self, color=None):
        self.__points = []
        self.__speeds = []
        self.__N = 0
        self.color = pygame.Color(*(color or (255, 255, 255)))

    def add_point(self, point, speed):
        self.__points.append(point)
        self.__speeds.append(speed)
        self.__N += 1

    def add_points(self, points, speeds):
        self.__points.extend(points)
        self.__speeds.extend(speeds)
        self.__N += len(points)

    def remove_point(self):
        self.__points.pop()
        self.__speeds.pop()
        self.__N -= 1

    def clear(self):
        self.__points = []
        self.__speeds = []
        self.__N = 0

    def set_points(self, screen_width, screen_height, mul):
        for p in range(self.__N):
            self.__points[p] += mul * self.__speeds[p]
            if self.__points[p].x > screen_width or self.__points[p].x < 0:
                self.__speeds[p].x = - self.__speeds[p].x
            if self.__points[p].y > screen_height or self.__points[p].y < 0:
                self.__speeds[p].y = - self.__speeds[p].y

    # "Отрисовка" точек
    def draw_points(self, display, style="points", width=3):
        if style == "line":
            for p_n in range(-1, self.__N - 1):
                pygame.draw.line(display, self.color, self.__points[p_n].int_pair(
                ), self.__points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.__points:
                pygame.draw.circle(display, self.color, p.int_pair(), width)


# Сглаживание ломаной

class Knot(Polyline):
    def __init__(self, color=None, addition_points=5):
        Polyline.__init__(self)
        self.__points = []
        self.__speeds = []
        self.__N = 0
        self.__count = addition_points
        self.color = pygame.Color(*(color or (255, 255, 255)))

    def __set_count(self, x):
        self.__count = x if 0 < x < 30 else self.__count
        self.__get_knot()

    def __get_count(self):
        return self.__count

    addition_points = property(__get_count, __set_count)

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)

    def __get_points(self, base_points):
        alpha = 1 / self.__count
        res = []
        for i in range(self.__count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def __get_knot(self):
        Polyline.clear(self)
        if len(self.__points) < 3:
            return []
        for i in range(-2, len(self.__points) - 2):
            ptn = list()
            ptn.append((self.__points[i] + self.__points[i+1]) * 0.5)
            ptn.append(self.__points[i + 1])
            ptn.append((self.__points[i+1] + self.__points[i+2]) * 0.5)

            Polyline.add_points(self, self.__get_points(ptn), [])

    def add_point(self, point, speed):
        self.__points.append(point)
        self.__speeds.append(speed)
        self.__N += 1
        self.__get_knot()

    def remove_point(self):
        self.__points.pop()
        self.__speeds.pop()
        self.__N -= 1
        self.__get_knot()

    def set_points(self, screen_width, screen_height, mul):
        for p in range(self.__N):
            self.__points[p] += mul * self.__speeds[p]
            if self.__points[p].x > screen_width or self.__points[p].x < 0:
                self.__speeds[p].x = - self.__speeds[p].x
            if self.__points[p].y > screen_height or self.__points[p].y < 0:
                self.__speeds[p].y = - self.__speeds[p].y
        self.__get_knot()


def draw_help(lines, current):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["1 - 0", "Change line (current not white)"])
    data.append(["Del", "Remove last point (current not white)"])
    data.append(["Num*", "Increase speed"])
    data.append(["Num/", "Decrease speed"])
    data.append(["————————————————————————————————————", ""])
    data.append(["", "Current knot is " + str(current)])
    data.append([str(lines[current].addition_points), "addition points of current knot"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    knots = [Polyline()] + [Knot() for i in range(9)]
    current_knot = 1
    show_help = False
    pause = True
    speed = 1

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knots = [Knot() for i in range(9)]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knots[current_knot].addition_points += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MULTIPLY:
                    speed *= 2
                if event.key == pygame.K_KP_DIVIDE:
                    speed /= 2
                if event.key == pygame.K_KP_MINUS:
                    knots[current_knot].addition_points -= 1
                if event.key in range(48, 59):  # event.key is number
                    knots[current_knot].color = pygame.Color("white")
                    current_knot = event.key - 48
                if event.key == pygame.K_DELETE:
                    knots[current_knot].remove_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                knots[current_knot].add_point(Vec2d(*event.pos), Vec2d(
                    random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        knots[current_knot].color.hsla = (hue, 100, 50, 100)
        for k in knots:
            k.draw_points(gameDisplay, 'line')

            if not pause:
                k.set_points(*SCREEN_DIM, speed)
        if show_help:
            draw_help(knots, current_knot)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
