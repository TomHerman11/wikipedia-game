import asyncio
from wikipedia_article_processor import async_fetch_wiki_article_and_get_neighboring_articles


# DFS:
async def async_dfs(
    start_article: str,
    goal_article: str,
    MAX_ARTICLES_TO_SEARCH: int,
    MAX_WIKI_PATH_LENGTH: int
) -> list[str]:
    '''
    At each node, the recursive calls are executed asynchronously, in order to not waste time
    while waiting for a response from Wikipedia.
    Once a result is found, all others recursive calls are canceled.
    '''

    async def DFS_helper(curr_article: str, goal_article: str, path: list[str]) -> list[str]:
        path = path + [curr_article]
        if curr_article == goal_article:
            await q.put(path)
            return

        if len(path) < MAX_WIKI_PATH_LENGTH:
            sub_searches_tasks = []
            for link in await async_fetch_wiki_article_and_get_neighboring_articles(curr_article):
                if (len(found) < MAX_ARTICLES_TO_SEARCH) and (link not in found):
                    found.add(link)
                    curr_task = asyncio.create_task(DFS_helper(link, goal_article, path))
                    sub_searches_tasks.append(curr_task)
                    all_search_tasks.append(curr_task)

            await asyncio.gather(*sub_searches_tasks)
        return

    found: set[str] = set()
    q: asyncio.Queue[str] = asyncio.Queue()
    all_search_tasks: list[asyncio.task] = []

    # start the DFS:
    main_task = asyncio.create_task(DFS_helper(start_article, goal_article, []))

    finished, unfinished = await asyncio.wait(
        [
            main_task,  # if this is finished first, we did not find a path (given the restrictions)
            asyncio.create_task(q.get())  # if this is finished first, we found a valid path!
        ],
        return_when=asyncio.FIRST_COMPLETED
    )

    dfs_result = []
    for x in finished:
        dfs_result = x.result() or dfs_result
        for task in all_search_tasks:
            task.cancel()

        for task in unfinished:
            task.cancel()

    if len(found) == MAX_ARTICLES_TO_SEARCH:
        print("Reached MAX_ARTICLES_TO_SEARCH! No more articles will be processed.")

    return dfs_result
