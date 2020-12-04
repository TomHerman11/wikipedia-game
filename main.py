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
        apply_workaround_aiohttp_bug()
        printPath(
            await async_bfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    # *** 'ASYNC' DFS: (please read function's documentation) ***
    elif (algorithm == "async_dfs"):
        apply_workaround_aiohttp_bug()
        printPath(
            await async_dfs(start_article, goal_article, MAX_ARTICLES_TO_SEARCH, MAX_WIKI_PATH_LENGTH)
        )

    else:
        print("Please make sure you typed correctly which search algorithm should be used :)")


def apply_workaround_aiohttp_bug():
    ########## TEMP WORKAROUND DUE TO 'aiohttp' BUG ##########
    # See: https://github.com/aio-libs/aiohttp/issues/4324
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
        return wrapper
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
    ########## TEMP WORKAROUND DUE TO 'aiohttp' BUG ##########


if __name__ == "__main__":
    asyncio.run(main())
