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


def get_images_amount(body):
    imgs = body.find_all('img')
    fit_imgs = len(
        [x for x in imgs if x.get('width') and int(x.get('width')) >= 200]
    )
    return fit_imgs


def get_headers_amount(body):
    headers = body.find_all(re.compile('^h[1-6]$'))
    count = 0
    for header in headers:
        children = header.find_all(recursive=False)
        if children:
            children_content = [x.getText() for x in children if x.getText()]
            try:
                first_letter = children_content[0][0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
        else:
            try:
                first_letter = header.getText()[0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
    return count


def get_max_links_len(body):
    max_count = 0
    all_links = body.find_all('a')
    for link in all_links:
        current_count = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                current_count += 1
                max_count = max(current_count, max_count)
            else:
                current_count = 0
    return max_count


def get_lists_num(body):
    count = 0
    all_lists = body.find_all(['ul', 'ol'])
    for tag in all_lists:
        if not tag.find_parents(['ul', 'ol']):
            count += 1
    return count


def parse(start, end, path):
    bridge = shortest_path(start, end)
    out = {}
    for file in bridge:
        with open(os.path.join(path, file)) as data:
            soup = BeautifulSoup(data, "html.parser")
        body = soup.find(id="bodyContent")

        imgs = get_images_amount(body)
        headers = get_headers_amount(body)
        linkslen = get_max_links_len(body)
        lists = get_lists_num(body)
        out[file] = [imgs, headers, linkslen, lists]
    return out


parse('Stone_Age', 'Python_(programming_language)', 'wiki')
