
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import *


def get_children(url):
    """
    Returns a list of all hyperlinked URLs on the Wikipedia page @ url
    :param url: Wikipedia page URL
    """
    # get website html body and parse it with bs4
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        print('URL error: ', url)
        return []

    # OPTIONAL: print out title and url of current website to see where it's at right now
    try:
        if soup.title:
            print(soup.title.string, url)
    except:
        print('title error: ')

    # get the content div from the article
    content = soup.find('div', class_='mw-content-ltr')

    if content:
        # filter out bad links from the list
        return list(content.find_all('a'))
    else:
        # if no content on the page, don't return anything
        return []


def find_path(parents, end_node, start_node):
    """
    Given a parents dictionary and an end and start node, constructs path from start to end
    :param parents: dictionary of parents returned by BFS
    :param end_node: end node of BFS
    :param start_node: start node of BFS
    :return: list representing path from start to end
    """
    path = [end_node]
    next_node = end_node

    while next_node != start_node:
        next_node = parents[next_node]
        path.append(next_node)

    path.reverse()
    return path


def bfs(start_url, end_url):
    """
    Runs BFS from start_url to end_url
    :return: Tuple of distance and path
    """
    # construct distance dictionary
    dist = defaultdict(lambda: float("inf"))
    dist[start_url] = 0

    # construct parent dictionary
    parent = dict()
    parent[start_url] = None

    # set up queue for BFS
    queue = deque()
    queue.append(start_url)

    # pretty generic BFS algorithm
    while queue:
        curnode = queue.popleft()
        nbrs = get_children(curnode)
        # get sub url for formatting
        cur_sub_url = urlparse(curnode).netloc
        for nbr in nbrs:
            # make sure hyperlinks only to other Wikipedia articles
            base_nbr = nbr.get('href')
            if base_nbr and base_nbr.startswith("/"):
                # format URLs appropriately
                formatted_nbr = "https://" + cur_sub_url + base_nbr
                if formatted_nbr == end_url:
                    parent[formatted_nbr] = curnode
                    return dist[curnode] + 1, find_path(parent, end_url, start_url)
                elif dist[formatted_nbr] == float('inf'):
                    dist[formatted_nbr] = dist[curnode] + 1
                    parent[formatted_nbr] = curnode
                    queue.append(formatted_nbr)


# to run the program:
bfs_results = bfs('Article 1', 'Article 2')
print(bfs_results[0])
print(bfs_results[1])


