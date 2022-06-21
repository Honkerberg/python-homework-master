"""
REST API.
"""
from asyncio.log import logger
from http import HTTPStatus
from flask import Flask, jsonify, request
from marshmallow import ValidationError

from app import db
from app.model import ArticleSchema
from app.service import get_articles_with_keywords

app = Flask(__name__)


# noinspection PyUnusedLocal
@app.teardown_request
def remove_db_session(exception=None):
    db.session.remove()


@app.route('/articles/find', methods=['POST'])
def find_articles():
    """
    If query in request.json is not valid, returns HTTP 422.
    If query is valid, returns result with articles matching given keywords.
    """
    # todo: implement validation of data received in request.json, get
    # keywords from the query
    article_schema = ArticleSchema(many=True)
    k = request.json['keywords']
    articles = get_articles_with_keywords(k)

    try:
        article_schema.validate(article_schema.dump(articles))
    except ValidationError as err:
        logger.warning(f"{err.messages}")
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    # todo: implement searching for articles by keywords in app.service.get_articles_with_keywords() and
    # todo: use it below. If no keywords were given, should return an empty
    # list.
    return jsonify({
        'articles': [
            {'text': i.header, 'url': i.url} for i in get_articles_with_keywords(k)
        ]
    }
    ), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
