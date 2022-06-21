"""
ORM definitions.
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

from marshmallow import Schema, fields, post_load

Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'

    id: int = Column(Integer, primary_key=True)
    header: str = Column(String, nullable=False, index=True)
    url: str = Column(String, nullable=False, index=True)
    timestamp: datetime = Column(
        TIMESTAMP(
            timezone=True),
        nullable=False,
        default=func.now(),
        index=True)

    def __str__(self):
        return f"Article(id={self.id}, header={self.header}, url={self.url})"


class ArticleSchema(Schema):
    header = fields.Str(required=True)
    url = fields.Str(required=True)

    @post_load
    def get_article(self, data, **kwargs):
        return Article(**data)
