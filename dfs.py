from wikipedia_article_processor import fetch_wiki_article_and_get_neighboring_articles


# DFS:
def dfs(
    start_article: str,
    goal_article: str,
    MAX_ARTICLES_TO_SEARCH: int,
    MAX_WIKI_PATH_LENGTH: int
) -> list[str]:

    def DFS_helper(curr_article: str, goal_article: str, path: list[str], found: set[str]) -> list[str]:
        if (curr_article in found) or (len(found) >= MAX_ARTICLES_TO_SEARCH):
            return []

        found.add(curr_article)
        path.append(curr_article)

        if curr_article == goal_article:
            return path

        if len(path) < MAX_WIKI_PATH_LENGTH:
            for link in fetch_wiki_article_and_get_neighboring_articles(curr_article):
                curr_try = DFS_helper(link, goal_article, path, found)
                if curr_try:
                    return curr_try

        path.pop()
        return []

    found: set[str] = set()
    return DFS_helper(start_article, goal_article, [], found)
