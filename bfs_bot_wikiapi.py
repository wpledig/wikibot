

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


def get_article(prompt_text):
    """
    Used for searching for articles based on user input
    :param prompt_text: text to prompt the user for input
    """
    return_article = None
    # make sure article is valid before being returned
    while not return_article:
        # get user input
        query = input(prompt_text)
        # if something inputted, use it
        if query:
            search_results = wikipedia.search(query, 1)
            # if search returns results
            if search_results:
                return_article = search_results[0]
                # make sure page is not disambiguation
                try:
                    wikipedia.summary(return_article, 1)
                except wikipedia.DisambiguationError:
                    print("Be more specific!")
                    return_article = None
            # throw error if search doesn't work
            else:
                print("Invalid search, try again!")
        # if nothing inputted, choose random article
        else:
            return_article = wikipedia.random()
    print("Found article:", return_article)
    return return_article


# to run the program:
start_title = get_article("Start article:")
end_title = get_article("End article:")

bfs_results = bfs(start_title, end_title)
print(bfs_results[0])
print(" --> ".join(bfs_results[1]))


