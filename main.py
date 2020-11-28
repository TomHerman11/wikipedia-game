import time

from bfs import bfs
from dfs import dfs
from async_bfs import async_bfs
import asyncio


def printPath(path: list[str]) -> None:
    print(' -> '.join(path))


async def main() -> None:
    MAX_ARTICLES_TO_SEARCH = 1000000
    MAX_WIKI_PATH_LENGTH = 3  # including 'start' and 'goal'

    # receive (and edit if needed) the start and goal articles
    start_article = input("Please enter the start article: ").lower()
    goal_article = input("Please enter the goal article: ").lower()
    if not start_article or not goal_article:
        return

    # *** BFS: ***
    # printPath(
    #     bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    # )

    # *** DFS: ***
    printPath(
        dfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    )

    # *** 'ASYNC' BFS: (read function's documentation) ***
    # printPath(
    #     await async_bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    # )


if __name__ == "__main__":
    asyncio.run(main())
