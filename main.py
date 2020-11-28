import time

from bfs import bfs
from dfs import dfs
from async_bfs import async_bfs
import asyncio


async def main() -> None:
    MAX_ARTICLES_TO_SEARCH = 5000
    MAX_WIKI_PATH_LENGTH = 3  # including 'start' and 'goal'

    # receive (and edit if needed) the start and goal articles
    start_article = input("Please enter the start article: ").lower()
    goal_article = input("Please enter the goal article: ").lower()
    if not start_article or not goal_article:
        return

    # *** BFS: ***
    # start = time.time()
    # print(
    #     bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    # )
    # print("Total time bfs (seconds):", time.time()-start)

    # *** ASYNC FETCH BFS: ***
    start = time.time()
    print(
        await async_bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    )
    print("Total time async_bfs (seconds):", time.time()-start)

    # *** DFS: ***
    # start = time.time()
    # print(
    #     dfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
    # )
    # print("Total time dfs (seconds):", time.time()-start)


if __name__ == "__main__":
    asyncio.run(main())
