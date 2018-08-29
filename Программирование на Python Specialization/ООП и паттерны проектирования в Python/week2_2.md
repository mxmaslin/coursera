# Создание иерархий классов

Вам предоставляется следующий код на языке Python

    import pygame
    import random
    import math

    SCREEN_DIM = (800, 600)

    # Функции для работы с векторами

    def sub(x, y):  # разность двух векторов
        return x[0] - y[0], x[1] - y[1]

    def add(x, y):  # сумма двух векторов
        return x[0] + y[0], x[1] + y[1]

    def length(x):  # длинна вектора
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def mul(v, k):  # умножение вектора на число
        return v[0] * k, v[1] * k

    def scal_mul(v, k):  # скалярное умножение векторов
        return v[0] * k, v[1] * k

    def vec(x, y):  # создание вектора по началу (x) и концу (y) направленного отрезка
        return sub(y, x)

    # "Отрисовка" точек
    def draw_points(points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)

    # Сглаживание ломаной

    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))

    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(get_point(base_points, i * alpha))
        return res

    def get_knot(points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append(mul(add(points[i], points[i + 1]), 0.5))
            ptn.append(points[i + 1])
            ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))
            res.extend(get_points(ptn, count))
        return res

    # Отрисовка справки
    def draw_help():
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(steps), "Current points"])
        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                          (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    # Персчитывание координат опорных точек
    def set_points(points, speeds):
        for p in range(len(points)):
            points[p] = add(points[p], speeds[p])
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    # Основная программа
    if __name__ == "__main__":
        pygame.init()
        gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        steps = 35
        working = True
        points = []
        speeds = []
        show_help = False
        pause = True
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
                        points = []
                        speeds = []
                    if event.key == pygame.K_p:
                        pause = not pause
                    if event.key == pygame.K_KP_PLUS:
                        steps += 1
                    if event.key == pygame.K_F1:
                        show_help = not show_help
                    if event.key == pygame.K_KP_MINUS:
                        steps -= 1 if steps > 1 else 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    points.append(event.pos)
                    speeds.append((random.random() * 2, random.random() * 2))
            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            draw_points(points)
            draw_points(get_knot(points, steps), "line", 3, color)
            if not pause:
                set_points(points, speeds)
            if show_help:
                draw_help()
            pygame.display.flip()
        pygame.display.quit()
        pygame.quit()
        exit(0)

Вам необходимо провести рефакторинг кода:

1. Реализовать класс 2-мерных векторов `Vec2d` — определить основные математические операции: сумма `Vec2d.__add__`, разность `Vec2d.__sub__`, умножение на скаляр и скалярное умножение (`Vec2d.__mul__`); добавить возможность вычислять длину вектора `a` через `len(a)`; добавить метод `int_pair` для получение пары (tuple) целых чисел.
2. Реализовать класс замкнутых ломаных `Polyline`, с возможностями: добавление в ломаную точки (`Vec2d`) c её скоростью; пересчёт координат точек (`set_points`); отрисовка ломаной (`draw_points`),
3. Реализовать класс `Knot` — потомок класса `Polyline` — в котором добавление и пересчёт координат инициируют вызов функции `get_knot` для расчёта точек кривой по добавляемым опорным.
4. Все классы должны быть самостоятельными и не использовать внешние функции.

Дополнительные задачи (для получения "положительной" оценки не обязательны):
1. Реализовать возможность удаления точки из кривой.
2. Реализовать возможность удаления/добавления точек сразу для нескольких кривых.
3. Реализовать возможность ускорения/замедления движения кривых.

**Решение**:

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
