# FETCH AND PARSE HTML
import re
import requests
from bs4 import BeautifulSoup
import time

WIKIPEDIA_DOMAIN_NAME = 'https://en.wikipedia.org'
WIKIPEDIA_ARTICLE_DIV_CLASS = 'mw-parser-output'
WIKIPEDIA_ARTICLE_PATH_PREFIX = '/wiki/'


# fetches an article from Wikipedia and returns a model (BeautifulSoup) of the HTML page:
#
def fetch_wiki_article(article_title: str) -> BeautifulSoup:
    # add '_' instead of whitespaces if needed
    article_title = '_'.join(article_title.split())

    start = time.time()
    print("Fetching:", article_title)
    url = WIKIPEDIA_DOMAIN_NAME + WIKIPEDIA_ARTICLE_PATH_PREFIX + article_title
    page = requests.get(url)

    print(" Fetched:", article_title, "||", "time:", time.time()-start)

    return BeautifulSoup(page.content, 'html.parser')


def get_neighboring_articles(article_html_model: BeautifulSoup) -> list[str]:
    # get the article's div from the whole page:
    article_content_div = article_html_model.find('div', class_=WIKIPEDIA_ARTICLE_DIV_CLASS)
    if not article_content_div:
        return []

    # get all links to other 'neighboring' articles, from within the article:
    neighboring_articles_links = article_content_div.find_all(name='a', href=re.compile('^/wiki/(?!File:)((?!Template)|(?!Wikipedia)|(?!Help)|(?!Special).)*$'))

    # filter out duplicates:
    unique_neighboring_articles_links = set()
    for article_link in neighboring_articles_links:
        unique_neighboring_articles_links.add(article_link['href'].lower())

    # 'href' values start the the '/wiki/' prefix. remove it:
    return [link.removeprefix(WIKIPEDIA_ARTICLE_PATH_PREFIX) for link in unique_neighboring_articles_links]


def fetch_wiki_article_and_get_neighboring_articles(article_title: str) -> list[str]:
    return get_neighboring_articles(fetch_wiki_article(article_title))
