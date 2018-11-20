

import wikipedia
from collections import *


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


def bfs(s_title, e_title):
    """
    Runs BFS from start_url to end_url
    :return: Tuple of distance and path
    """
    # construct distance dictionary

    dist = defaultdict(lambda: float("inf"))
    dist[s_title] = 0

    # construct parent dictionary
    parent = dict()
    parent[s_title] = None

    # set up queue for BFS
    queue = deque()
    queue.append(s_title)

    # pretty generic BFS algorithm
    while queue:
        curtitle = queue.popleft()
        print(curtitle)
        try:
            nbr_links = wikipedia.page(curtitle).links
        except (wikipedia.DisambiguationError, wikipedia.PageError):
            print("Invalid page:", curtitle)
            nbr_links = []

        for nbr in nbr_links:
            if nbr == e_title:
                parent[nbr] = curtitle
                return dist[curtitle] + 1, find_path(parent, e_title, s_title)
            elif dist[nbr] == float('inf'):
                dist[nbr] = dist[curtitle] + 1
                parent[nbr] = curtitle
                queue.append(nbr)


# to run the program:
start_title = None
while not start_title:
    search_results = wikipedia.search(input("Start article:"))
    if search_results:
        start_title = search_results[0]
    else:
        print("Invalid search, try again!")

end_title = None
while not end_title:
    search_results = wikipedia.search(input("End article:"))
    if search_results:
        end_title = search_results[0]
    else:
        print("Invalid search, try again!")

print(start_title, end_title)

bfs_results = bfs(start_title, end_title)
print(bfs_results[0])
print(" --> ".join(bfs_results[1]))


