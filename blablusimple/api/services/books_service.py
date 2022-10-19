from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Books, BooksSchema
from sqlalchemy import text
from sqlalchemy import func


def books_list_service(page, per_page, search=str):
    try:
        fetch_book = Books.query.filter(func.lower(Books.title)
                                        .like('%'+search+'%')
                                        | func.lower(Books.description)
                                        .like('%'+search+'%'))\
            .order_by(Books.id.desc())\
            .paginate(page=page, per_page=per_page)

        list_books = list()
        for data in fetch_book.items:
            dict_data = {}
            dict_data['id'] = data.id
            dict_data['title'] = data.title
            dict_data['year'] = data.year
            dict_data['description'] = data.description
            list_books.append(dict_data)

        pagination = {
                "page": fetch_book.page,
                'pages': fetch_book.pages,
                'total_count': fetch_book.total,
                'prev_page': fetch_book.prev_num,
                'next_page': fetch_book.next_num,
                'has_next': fetch_book.has_next,
                'has_prev': fetch_book.has_prev,
            }

        return response_with(resp.SUCCESS_200,
                             value={"data": list_books},
                             pagination=pagination)
    except Exception as e:
        return response_with(
                resp.BAD_REQUEST_400,
                value={"data": []}
            )
