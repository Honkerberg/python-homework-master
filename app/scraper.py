"""
Web scraping service.
"""
import logging
import time

from app.news import IdnesScraper, IhnedScraper, BbcScraper
from app.service import save_article_if_new
from app.model import Article

logger = logging.getLogger(__name__)
SCRAPERS = [IdnesScraper(), IhnedScraper(), BbcScraper()]


def scrape_news():
    """Gets articles from news servers and saves new ones into our DB.
    If any scraper fails, it must be logged but continue in operation.
    """
    for scraper in SCRAPERS:
        logger.info(f"Scraping news using {type(scraper).__name__}")
        # todo implement logic using already implemented scrapers and
        # app.service.save_article_if_new()

        for n in scraper.get_headers():
            a = Article(header=n.header, url=n.url)
            save_article_if_new(a)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='{asctime} {levelname:<8} {name}:{module}:{lineno} - {message}',
        style='{')
    # todo: implement regular calling of scrape_news()

    while True:
        timer = 60
        logger.info(f"New load of articles incoming!")
        scrape_news()
        logger.info(f"{timer} seconds until next scrape!")
        time.sleep(timer)
