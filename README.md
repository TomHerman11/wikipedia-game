# wikipedia-game
How fast can you navigate from a 'start' article to a 'goal' article in Wikipedia?  
Given a 'start' article, you can only advance by clikcing on the links to other Wikipedia articles, within the article itself.

### Example
starting from the [Python (programming language) Wikipedia article](https://en.wikipedia.org/wiki/Python_(programming_language)), navigate to the [Afterlife Wikipedia article](https://en.wikipedia.org/wiki/Afterlife).


One possible answer:
[Python (programming language)](https://en.wikipedia.org/wiki/Python_(programming_language)) -> [Complex number](https://en.wikipedia.org/wiki/Complex_number) -> [Carl Friedrich Gauss](https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss) -> [Afterlife](https://en.wikipedia.org/wiki/Afterlife).


## This Project
Given a 'start' and 'goal' articles provided by the user, the code in this project uses the [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) or the [DFS](https://en.wikipedia.org/wiki/Depth-first_search) algorithms in order to find a solution path from the 'start' to the 'goal' articles, following the insrtucations above.

**Notes:**
1. There may be more than one possible path.
2. BFS will always find the shortest path (in regards to the number of 'jumps' from one article to another).
3. Since Wikipedia is huge and the search can take a lot of time, two changeable restrictions are applied:
    1. The amount of articles that will be processed in total, see `MAX_ARTICLES_TO_SEARCH` in `main.py`
    2. The maximum length of a possible path from the 'start' to 'goal' articles, see `MAX_WIKI_PATH_LENGTH` in `main.py`.


## How to Run
1. Create a Python Virtual Environment ('.venv'): `python -m venv .venv`
2. Install requirements: `pip install -r requirements.txt -y`
3. Uncomment from `main()` at `main.py` your preffered function to run (BFS / DFS)
4. Run `main.py` file.
5. The output may be empty if:
    1. A possible solution path does not exist.
    2. All of the possible solutions are longer than `MAX_WIKI_PATH_LENGTH`.
    3. The `MAX_ARTICLES_TO_SEARCH` bound was reached and the articles that were processed can not form a possible solution path. 

## Issues:
While searching, the code in this project fetches articles from Wikipedia and processes them.  
As more and more articles are being fetched, the response time from Wikipedia gets longer.  
This affects significantly on the total run time. One search with a possible solution of two 'jumps' can take a lot of precious minutes.

I tried to use `async_bfs` function in order to save time: fetch articles while they wait in the deque for their turn to be popped.  
When tested, the benefit of `async_bfs` is limited.