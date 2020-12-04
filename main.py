import asyncio

from bfs import bfs
from dfs import dfs
from async_bfs import async_bfs
from async_dfs import async_dfs


MAX_ARTICLES_TO_SEARCH = 1000000
MAX_WIKI_PATH_LENGTH = 3  # including 'start' and 'goal'


def printPath(path: list[str]) -> None:
    print(' -> '.join(path))


async def main() -> None:
    # receive (and edit if needed) the start and goal articles
    start_article = input("Please type the start article: ").lower()
    goal_article = input("Please type the goal article: ").lower()
    if not start_article or not goal_article:
        return
    algorithm = input("Please type which search algorithm should be used (BFS, DFS, async_BFS, async_DFS): ").lower()

    # *** BFS: ***
    if (algorithm == "bfs"):
        printPath(
            bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    # *** DFS: ***
    elif (algorithm == "dfs"):
        printPath(
            dfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    # *** 'ASYNC' BFS: (please read function's documentation) ***
    elif (algorithm == "async_bfs"):
        printPath(
            await async_bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    # *** 'ASYNC' DFS: (please read function's documentation) ***
    elif (algorithm == "async_dfs"):
        printPath(
            await async_dfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    else:
        print("Please make sure you typed correctly which search algorithm should be used :)")

if __name__ == "__main__":
    asyncio.run(main())
