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

    import pygame
    import random
    import math

    SCREEN_DIM = (800, 600)


    class Vec2d:
        def __init__(self, x_or_pair, y=None):
            if y == None:
                self.x = x_or_pair[0]
                self.y = x_or_pair[1]
            else:
                self.x = x_or_pair
                self.y = y

        def __add__(self, vec):
            return Vec2d(self.x + vec.x, self.y + vec.y)

        def __sub__(self, vec):
            return Vec2d(self.x - vec.x, self.y - vec.y)

        def __mul__(self, k):
            if isinstance(k, Vec2d):
                return self.x * k.x + self.y * k.y
            return Vec2d(self.x * k, self.y * k)

        def len(self, x):
            return (x.x ** 2 + x.y ** 2) ** .5

        def int_pair(self):
            return (int(self.x), int(self.y))


    class Polyline:
        def __init__(self):
            self.points = []
            self.speeds = []

        def add_point(self, point, speed):
            self.points.append(point)
            self.speeds.append(speed)

        def set_points(self):
            for i in range(len(self.points)):
                self.points[i] += self.speeds[i]
                if self.points[i].x > SCREEN_DIM[0] or self.points[i].x < 0:
                    self.speeds[i] = Vec2d(- self.speeds[i].x, self.speeds[i].y)
                if self.points[i].y > SCREEN_DIM[1] or self.points[i].y < 0:
                    self.speeds[i] = Vec2d(self.speeds[i].x, -self.speeds[i].y)

        def draw_points(self, points, width=3, color=(255, 255, 255)):
            for point in points:
                pygame.draw.circle(gameDisplay, color, point.int_pair(), width)


    class Knot(Polyline):    
        def __init__(self, count):
            super().__init__()
            self.count = count

        def add_point(self, point, speed):
            super().add_point(point, speed)
            self.get_knot()

        def set_points(self):
            super().set_points()
            self.get_knot()

        def get_point(self, points, alpha, deg=None):
            if deg is None:
                deg = len(points) - 1
            if deg == 0:
                return points[0]
            return points[deg]*alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

        def get_points(self, base_points):
            alpha = 1 / self.count
            res = []
            for i in range(self.count):
                res.append(self.get_point(base_points, i * alpha))
            return res

        def get_knot(self):
            if len(self.points) < 3:
                return []
            res = []
            for i in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
                res.extend(self.get_points(ptn))
            return res

        def draw_points(self, points, width=3, color=(255, 255, 255)):
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)
            

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


    if __name__ == "__main__":
        pygame.init()
        gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        steps = 35
        working = True
        polyline = Polyline()
        knot = Knot(steps)
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
                        polyline = Polyline()
                        knot = Knot(steps)
                    if event.key == pygame.K_p:
                        pause = not pause
                    if event.key == pygame.K_KP_PLUS:
                        steps += 1
                    if event.key == pygame.K_F1:
                        show_help = not show_help
                    if event.key == pygame.K_KP_MINUS:
                        steps -= 1 if steps > 1 else 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    polyline.add_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                    knot.add_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            polyline.draw_points(polyline.points)
            knot.draw_points(knot.get_knot(), 3, color)
            if not pause:
                polyline.set_points()
                knot.set_points()
            if show_help:
                draw_help()
            pygame.display.flip()
        pygame.display.quit()
        pygame.quit()
        exit(0)
