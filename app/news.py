"""
News scrapers.
"""
import requests
import re

from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup as bs


@dataclass
class Article:
    """Represents an article from a news server."""
    header: str
    url: str


class NewsScraper:
    @abstractmethod
    def get_headers(self) -> List[Article]:
        """Returns a list of articles from the news server."""
        pass


class IdnesScraper(NewsScraper):
    def get_headers(self) -> List[Article]:

        url = 'https://idnes.cz'
        article = requests.get(url)
        soup = bs(article.content, 'html.parser')
        divs = soup.find_all(href=re.compile(r"\bidnes.cz"),
                             class_="art-link")

        l = []
        for lines in divs:
            target_link = lines.get('href')
            target_header = lines.h3.string.strip()
            l.append(Article(target_header, target_link))
        return l


class IhnedScraper(NewsScraper):
    def get_headers(self) -> List[Article]:

        url = 'https://ihned.cz'
        article = requests.get(url)
        soup = bs(article.content, 'html.parser')
        divs = soup.find_all(class_="article-box")

        l = []
        for lines in divs:
            target_link = lines.a.get('href')
            target_header = lines.h3.string.strip()
            if re.search(r"\A//", target_link):
                target_link = url.split('/')[0] + target_link
            l.append(Article(target_header, target_link))
        return l


class BbcScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        url = 'https://bbc.com'
        article = requests.get(url)
        soup = bs(article.content, 'html.parser')
        divs = soup.find_all(class_="media__title")

        l = []
        for link in divs:
            target_link = link.a.get('href')
            target_header = link.a.string.strip()
            if re.search("article", target_link):
                l.append(Article(target_header, target_link))
        return l
