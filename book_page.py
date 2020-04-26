from model import books

def get_book_details(isbn_no = None):
    if isbn_no is None:
        return None
    else:
        book = books.query.filter_by(ISBN_number=isbn_no).all()
        return book[0]