from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class AuthorsCatalog(Base):
    __tablename__ = 'authors_catalog'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    books = relationship('Books', back_populates='author')
    #publishers = relationship('PublishersCatalog', back_populates='authors')

    def __init__(self, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'{self.id} {self.first_name} {self.last_name}'

    @hybrid_property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class GenresCatalog(Base):
    __tablename__ = 'genres_catalog'
    id = Column(Integer, primary_key=True)
    genre = Column(String(20))
    books = relationship('Books', back_populates='genre')

    def __init__(self, genre=None):
        self.genre = genre

    def __repr__(self):
        return f'{self.genre}'


class PublishersCatalog(Base):
    __tablename__ = 'publishers_catalog'
    id = Column(Integer, primary_key=True)
    publisher = Column(String(30))
  #  book = relationship('Books', backref='publisher')
    books = relationship('Books', back_populates='publisher')
    #authors = relationship('AuthorsCatalog', back_populates='publishers')

    def __init__(self, publisher=None):
        self.publisher = publisher

    def __repr__(self):
        return f'{self.publisher}'


class Thumbs(Base):
    __tablename__ = 'thumbs'
    id = Column(Integer, primary_key=True)
    image = Column(String(512))
    # book = relationship('Books', backref='thumb')

    def __init__(self, image=None):
        self.image = image

    def __repr__(self):
        return f'{self.id} {self.image}'


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)

    author_id = Column(Integer, ForeignKey('authors_catalog.id'))
    author = relationship('AuthorsCatalog', lazy='joined', innerjoin=True, back_populates="books")

    genre_id = Column(Integer, ForeignKey('genres_catalog.id'))
    genre = relationship('GenresCatalog', back_populates="books")

    publisher_id = Column(Integer, ForeignKey('publishers_catalog.id'))
    publisher = relationship('PublishersCatalog', back_populates='books')

    thumb_id = Column(Integer, ForeignKey('thumbs.id'))
    thumb = relationship('Thumbs', backref='book')

    _full_name = association_proxy('authors_catalog','full_name')

    def __init__(self, name=None, author_id=None, genre_id=None, publisher_id=None, thumb_id=None):
        self.name = name
        self.author_id = author_id
        self.genre_id = genre_id
        self.publisher_id = publisher_id
        self.thumb_id = thumb_id

    def __repr__(self):
        return f'{self.id} {self.name} {self.author} {self.genre} {self.publisher} {self.thumb_id}'


class BooksView(Base):
    __tablename__ = 'book_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)
    author = Column(String(41),nullable=False)
    genre = Column(String(20))
    publisher = Column(String(30))
    image = Column(String(512))

    def __init__(self, name=None, author=None, genre=None, publisher=None, image=None):
        self.name = name
        self.author = author
        self.genre = genre
        self.publisher = publisher
        self.image = image

    def __repr__(self):
        return f'{self.id} {self.name} {self.author} {self.genre} {self.publisher} {self.image}'

