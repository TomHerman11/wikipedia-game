import asyncio
from collections import deque  # for bfs
# from queue import Queue
from bfs import BFSNode
from wikipedia_article_processor import fetch_wiki_article_and_get_neighboring_articles


class AsyncBFSNode:
    async_tasks: list[asyncio.Task] = []

    def __init__(self, bfs_node_parent: 'BFSNode', article: str, distance_from_root: int) -> None:
        self.bfsNode = BFSNode(bfs_node_parent, article, distance_from_root)
        self.q = asyncio.Queue()

        # 'fire and forget' fetching & processing neighboring articles:
        AsyncBFSNode.async_tasks.append(asyncio.create_task(self.fetch_and_process()))

    # async def create_AsyncBFSNode(bfs_node_parent: 'BFSNode', article: str, distance_from_root: int) -> None:
    #     node = AsyncBFSNode(bfs_node_parent, article, distance_from_root)
    #     node.fetch_and_process()  # don't await.
    #     return node

    async def fetch_and_process(self):
        links = fetch_wiki_article_and_get_neighboring_articles(self.bfsNode.article)
        await self.q.put(links)

    async def get_neighboring_articles(self) -> list[str]:
        a = await self.q.get()  # will block until receives value
        return a


async def async_bfs(
    start_article: str,
    goal_article: str,
    MAX_ARTICLES_TO_SEARCH: int,
    MAX_WIKI_PATH_LENGTH: int
) -> list[str]:

    root = AsyncBFSNode(None, start_article, 0)
    found: set[str] = set()
    de: deque['AsyncBFSNode'] = deque()

    # add start:
    found.add(start_article)
    de.append(root)
    path = []

    while len(de):
        curr_article_node = de.popleft()
        # print("Current article:", curr_article_node.bfsNode.article)
        if curr_article_node.bfsNode.article == goal_article:
            path = BFSNode.get_path_from_bfs_nodes(curr_article_node.bfsNode)
            break

        if curr_article_node.bfsNode.distance_from_root == MAX_WIKI_PATH_LENGTH:
            continue

        # search for 'neighbors' and add them to the deque:
        for link in await curr_article_node.get_neighboring_articles():
            if (len(found) < MAX_ARTICLES_TO_SEARCH) and (link not in found):
                found.add(link)
                de.append(
                    AsyncBFSNode(
                        curr_article_node.bfsNode, link, curr_article_node.bfsNode.distance_from_root + 1
                    )
                )

    for t in AsyncBFSNode.async_tasks:
        t.cancel()

    print('len(found):', len(found))
    return path
