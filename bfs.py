from collections import deque
from wikipedia_article_processor import fetch_wiki_article_and_get_neighboring_articles


class BFSNode:
    def __init__(self, parent: 'BFSNode', article: str, distance_from_root: int) -> None:
        self.parent = parent
        self.article = article
        self.distance_from_root = distance_from_root

    def __repr__(self) -> str:
        return self.article

    def get_path_from_bfs_nodes(tail: 'BFSNode') -> list[str]:
        path = []
        while tail:
            path.append(tail.article)
            tail = tail.parent
        path.reverse()
        return path


def bfs(
    start_article: str,
    goal_article: str,
    MAX_ARTICLES_TO_SEARCH: int,
    MAX_WIKI_PATH_LENGTH: int
) -> list[str]:

    root = BFSNode(None, start_article, 0)
    found: set[str] = set()
    # de: Deque['BFSNode'] = deque()
    de: deque['BFSNode'] = deque()

    # add start:
    found.add(start_article)
    de.append(root)

    while len(de):
        curr_article_node = de.popleft()
        # print("Current article:", curr_article_node.article)
        if curr_article_node.article == goal_article:
            return BFSNode.get_path_from_bfs_nodes(curr_article_node)

        if curr_article_node.distance_from_root == MAX_WIKI_PATH_LENGTH:
            continue

        # search for 'neighbors' and add them to the deque:
        for link in fetch_wiki_article_and_get_neighboring_articles(curr_article_node.article):
            if (len(found) < MAX_ARTICLES_TO_SEARCH) and (link not in found):
                found.add(link)
                de.append(BFSNode(curr_article_node, link, curr_article_node.distance_from_root + 1))

    if len(found) == MAX_ARTICLES_TO_SEARCH:
        print("Reached MAX_ARTICLES_TO_SEARCH! No more articles will be processed.")

    return []
