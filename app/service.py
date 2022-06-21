"""
Service layer.
"""
import logging
from typing import List

from app.model import Article
from app import db

logger = logging.getLogger(__name__)


def get_articles_with_keywords(keywords: List[str]) -> List[Article]:
    """
    Returns all articles from DB where at least one of given keywords is in article's header.
    The newest articles will be first. If no keywords were given, should return an empty list.
    """
    # todo: implement using db.session.query()
    result = []
    for k in keywords:
        keyword_search = db.session.query(
            Article.header,
            Article.url).filter(
            Article.header.like(
                "%" +
                f"{k}" +
                "%")).order_by(
                Article.timestamp.desc())
        if keyword_search is None:

            return result
        else:
            for r in keyword_search:
                result.append(r)
                result = list(dict.fromkeys(result))
    return result


def save_article_if_new(a: Article) -> None:
    """Saves an article, if it is not in our DB already. Existence is checked by URL of the article."""
    # todo: implement using db.session.query(), db.session.add(),
    # db.session.commit() etc.

    new = db.session.query(Article).filter_by(header=a.header).first()
    if new:
        logger.warning(
            f"This article '{new.header}' is in database already, skipping...")
    else:
        db.session.add(a)
        logger.info(f"New article added")
        db.session.commit()
