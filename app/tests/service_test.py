from app import db, service
from app.model import Article


def test_get_articles_with_keywords():
    # setup
    db.create_empty_db()
    db.session.add(Article(header='a b c', url=''))
    db.session.add(Article(header='b c d', url=''))
    db.session.add(Article(header='x y z', url=''))
    db.session.commit()

    # test
    assert not service.get_articles_with_keywords(keywords=['aaa'])

    assert service.get_articles_with_keywords(keywords=['a'])[0].header == 'a b c'
    assert service.get_articles_with_keywords(keywords=['d'])[0].header == 'b c d'
    assert service.get_articles_with_keywords(keywords=['y'])[0].header == 'x y z'

    assert 'a b c' in [a.header for a in service.get_articles_with_keywords(keywords=['b', 'c'])]
    assert 'b c d' in [a.header for a in service.get_articles_with_keywords(keywords=['b', 'c'])]
