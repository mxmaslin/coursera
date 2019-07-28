from bs4 import BeautifulSoup
import re
import os


def get_href_page_names(page_name):
    try:
        with open(os.path.join('wiki', page_name)) as file:
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
            raw_a = soup.find_all('a', href=True)
            page_names = [
                x['href'].strip('/wiki/')
                for x in raw_a
                if x['href'].startswith('/wiki')
            ]
            return page_names
    except FileNotFoundError:
        return []


def bfs_paths(start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(get_href_page_names(vertex)) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def shortest_path(start, goal):
    try:
        return next(bfs_paths(start, goal))
    except StopIteration:
        return None


def parse(start, end, path):
    bridge = shortest_path(start, end)

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 20  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out
