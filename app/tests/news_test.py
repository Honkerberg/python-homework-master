import re

from app.news import IdnesScraper, IhnedScraper, BbcScraper, NewsScraper


def check_provider(provider: NewsScraper):
    articles = provider.get_headers()
    assert len(articles) > 0
    for a in articles:
        assert len(a.header) > 0
        assert a.header.strip() == a.header
        assert re.fullmatch(r'http(s)?://.*', a.url)


def test_idnes():
    check_provider(IdnesScraper())


def test_ihned():
    check_provider(IhnedScraper())


def test_bbc():
    check_provider(BbcScraper())
