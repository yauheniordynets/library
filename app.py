from flask import Flask, render_template, request, redirect
from models import Books, Thumbs, GenresCatalog, PublishersCatalog, AuthorsCatalog,BooksView
from database import *
from sqlalchemy.sql.expression import and_
from werkzeug.utils import secure_filename
import uuid
import os

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.route('/', methods=['GET', 'POST'])
def index():
    data = session.query(BooksView).all()
    if request.method == 'POST':
        queryform = request.form['name']
        column = request.form['column']
        query = session.query(BooksView).filter(getattr(BooksView, column).contains(queryform)).all()
        return render_template('index.html', data=query)
    return render_template('index.html', data=data)


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        genres = session.query(GenresCatalog).all()
        return render_template('addbook.html', data=genres)
    if request.method == 'POST':
        try:
            # Get data from inputs
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            title = request.form['title']
            genre = request.form['genre']
            publisher_title = request.form['publisher']
            file = request.files['file']
            # # get file and create filepath
            filename = secure_filename(file.filename)
            getfilepath = str(uuid.uuid4())
            # Check if book by author and publisher exists
            book = session.query(Books).join(AuthorsCatalog).filter(
                Books.name == title).filter(
                and_(AuthorsCatalog.first_name == first_name, AuthorsCatalog.last_name == last_name)).filter(
                Books.publisher.has(PublishersCatalog.publisher == publisher_title)).one_or_none()
            if book is not None:
                print('Book by this author and publisher already added')
                return redirect('/')

            filepath = os.path.join('static/', getfilepath)
            fullpath = os.path.join(filepath, filename)
            newthumb = Thumbs(fullpath)
            session.add(newthumb)
            session.flush()
            os.mkdir(filepath)
            file.save(fullpath)

            # Check if book by author exists
            book_by_author = (session.query(Books).join(AuthorsCatalog).filter(
                Books.name == title)).filter(
                and_(AuthorsCatalog.first_name == first_name, AuthorsCatalog.last_name == last_name)).one_or_none()
            print(book)
            if book_by_author is None:
                print('Creating new book by this author')
                new_book = Books(name=title)
            # Check if author exists
            author = session.query(AuthorsCatalog).filter(
                and_(AuthorsCatalog.first_name == first_name, AuthorsCatalog.last_name == last_name)).one_or_none()

            if author is None:
                print('Creating new Author')
                author = AuthorsCatalog(first_name=first_name, last_name=last_name)
                session.add(author)
            # Check if publisher exists
            publisher = session.query(PublishersCatalog).filter(PublishersCatalog.publisher == publisher_title).one_or_none()

            if publisher is None:
                print('Creating new publisher')
                publisher = PublishersCatalog(publisher=publisher_title)
                session.add(publisher)

            new_book.author = author
            new_book.publisher = publisher
            new_book.genre_id = session.query(GenresCatalog.id).filter(GenresCatalog.genre == genre).one()[0]
            new_book.thumb_id = newthumb.id
            # new_book = Books(author, genre_id, publisher_id, thumb_id) Додумаю
            session.add(new_book)
            session.commit()
        except:
            session.rollback()
            print('error')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
