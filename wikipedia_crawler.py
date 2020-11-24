# BFS:
from collections import deque

# DFS_WITH_THREADS:
import threading

# FETCH AND PARSE HTML
import re
import requests
from bs4 import BeautifulSoup

WIKIPEDIA_DOMAIN_NAME = 'https://en.wikipedia.org'
WIKIPEDIA_ARTICLE_DIV_CLASS = 'mw-parser-output'
MAX_ARTICLES_TO_SEARCH = 1000000
MAX_WIKI_PATH_LENGTH = 3  # including 'start' and 'goal'


def fetch_wiki_article(article_link: str) -> BeautifulSoup:
    url = WIKIPEDIA_DOMAIN_NAME + article_link
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_wiki_article_title(article_page: BeautifulSoup) -> str:
    return article_page.find(id='firstHeading').text


def get_wiki_article_links(article_page: BeautifulSoup) -> list[str]:
    # get the article's div from the whole page:
    article_div = article_page.find('div', class_=WIKIPEDIA_ARTICLE_DIV_CLASS)
    if not article_div:
        return []

    # get all links to other articles, within the article:
    all_article_links = article_div.find_all(name='a', href=re.compile('^/wiki/(?!File:)((?!Template)|(?!Wikipedia)|(?!Help).)*$'))

    unique_article_links = set()
    for article_link in all_article_links:
        unique_article_links.add(article_link['href'].lower())

    return list(unique_article_links)


def fetch_wiki_article_and_get_links(article_link):
    return get_wiki_article_links(fetch_wiki_article(article_link))


def printPath(path):
    print("Found Path: ", ' -> '.join(path))


# BFS:
def BFS(start_article: str, goal_article: str) -> bool:
    class BFSNode:
        def __init__(self, parent: 'BFSNode', article: str) -> 'BFSNode':
            self.parent = parent
            self.article = article

        def __repr__(self) -> str:
            return self.article

    def getPathFromBFSNodes(tail: 'BFSNode') -> list[str]:
        path = []
        while tail:
            path.append(tail.article)
            tail = tail.parent
        path.reverse()
        return path

    root = BFSNode(None, start_article)
    found = set()
    de = deque()

    # add start:
    found.add(start_article)
    de.append(root)

    while len(de):
        curr_article_node = de.popleft()
        if curr_article_node.article == goal_article:
            return getPathFromBFSNodes(curr_article_node)

        # search for 'neighbors' and add them to the deque:
        for link in (fetch_wiki_article_and_get_links(curr_article_node.article) or []):
            if (len(found) < MAX_ARTICLES_TO_SEARCH) and (link not in found):
                found.add(link)
                de.append(BFSNode(curr_article_node, link))

    return []


# DFS:
def DFS(start_article: str, goal_article: str) -> list[str]:
    def DFS_helper(curr_article: str, goal_article: str, path: list[str], found: set[str]) -> list[str]:
        if len(found) >= MAX_ARTICLES_TO_SEARCH:
            return []

        if (curr_article in found) or (len(path) > MAX_WIKI_PATH_LENGTH):
            return []

        found.add(curr_article)
        path.append(curr_article)

        if curr_article == goal_article:
            printPath(path)
            return path

        shortest_path = []
        for link in (fetch_wiki_article_and_get_links(curr_article) or []):
            curr_try = DFS_helper(link, goal_article, path, found)
            if (not shortest_path) or (len(curr_try) < len(shortest_path)):
                shortest_path = curr_try

        # pop 'curr_article', will not be in path
        path.pop()
        return shortest_path

    found = set()
    return DFS_helper(start_article, goal_article, [], found)


# DFS_WITH_THREADS:
def DFS_WITH_THREADS(start_article: str, goal_article: str) -> list[str]:
    found = set()
    res = [[]]
    lock_found = threading.Lock()
    lock_res = threading.Lock()

    def DFS_WITH_THREADS_helper(curr_article: str, goal_article: str, path: list[str]) -> None:
        # create a new array of 'path', each thread should have its own array (array is mutable):
        path = path + [curr_article]

        lock_found.acquire()
        lock_res.acquire()

        if (len(found) >= MAX_ARTICLES_TO_SEARCH) or (curr_article in found) or (len(path) > MAX_WIKI_PATH_LENGTH):
            lock_found.release()
            lock_res.release()
            return

        found.add(curr_article)
        lock_found.release()

        if curr_article == goal_article:
            printPath(path)
            if (not res[0]) or (len(path) < len(res[0])):
                res[0] = path
            lock_res.release()
            return

        lock_res.release()

        threads = []
        for link in (fetch_wiki_article_and_get_links(curr_article) or []):
            # passing a new array 'list(path)', since array is mutable.
            th = threading.Thread(target=DFS_WITH_THREADS_helper, args=(link, goal_article, path))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        return

    DFS_WITH_THREADS_helper(start_article, goal_article, [])
    return res[0]


def prepareWikiArticleToSearch(article: str) -> str:
    article = '_'.join(article.split())
    if not article.lower().startswith('/wiki/'):
        return '/wiki/' + article.lower()
    return article.lower()


# Main:
def main() -> None:
    #     articles_language = input(
    #         """Please enter the language of your articles as two characters.
    # Examples:
    # - English -> en
    # - Spanish -> es
    # - French -> fr
    # - etc.
    # Language: """)

    #     global WIKIPEDIA_DOMAIN_NAME
    #     WIKIPEDIA_DOMAIN_NAME = 'https://' + articles_language + '.wikipedia.org'

    # receive (and edit if needed) start and end articles
    start_article = prepareWikiArticleToSearch(input("Please enter a start article: "))
    goal_article = prepareWikiArticleToSearch(input("Please enter a goal article: "))
    if not start_article or not goal_article:
        return

    print(BFS(start_article, goal_article))
    # print(DFS(start_article, goal_article))
    # print(DFS_WITH_THREADS(start_article, goal_article))


if __name__ == "__main__":
    main()
