from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.transaction_books import TransactionBooks, \
    TransactionBookDetails, TransactionBooksSchema
from api.models.books import Books
from api.models.wallet import Wallet, WalletTransaction
from api.utils.database import db
from datetime import datetime, date


def create_transaction_books_service(data):

    try:
        # ========= BEGIN TRANSACTION NUMBER
        tmp_today = date.today()
        tmp_today = datetime.strftime(tmp_today, '%Y-%m-%d').replace("-","")[2:]
        transaction_number = ""
        sequence_number = 1
        
        tmp_list_number = list()
        tmp_list_number.append(tmp_today)
        tmp_list_number.append("-")

        tmp_transaction = TransactionBooks.query.order_by(TransactionBooks.id.desc()).first()
        if not tmp_transaction:
            tmp_list_number.append(str(sequence_number).zfill(4))
        else:
            tmp_transaction = tmp_transaction.transaction_number[0:4]
            if tmp_transaction==tmp_today[0:4]:
                sequence_number = tmp_transaction.sequence_number + 1
                tmp_list_number.append(str(sequence_number).zfill(4))
            else:
                tmp_list_number.append(str(sequence_number).zfill(4))
            
        transaction_number = ''.join(tmp_list_number)
        # ========= END TRANSACTION NUMBER

        transaction_buy = TransactionBooks(data['user_id'],
                                           data['description'],
                                           sequence_number,
                                           transaction_number)

        total_all_price = 0
        for dict_data in data['books']:

            book = Books.query.get_or_404(int(dict_data['id']))
            total_buy = int(dict_data['total'])
            if book.stock >= total_buy:
                total_price = book.price * total_buy
                detail_trans = TransactionBookDetails(book_price=book.price,
                                                      total_buy=total_buy,
                                                      total_price=total_price,
                                                      book=book,
                                                      description='Testing')
                transaction_buy.details.append(detail_trans)
                total_all_price += total_price
                book.stock = book.stock - total_buy


        # BEGIN CHECK BALANCE
        wallet = Wallet.query.filter_by(user_id=data['user_id']).first()
        if wallet.wallet_balance >= total_all_price:

            wallet_transaction = WalletTransaction(wallet_id=wallet.id,
                                                   debit=0,
                                                   credit=total_all_price)
            wallet.wallet_balance = wallet.wallet_balance - total_all_price

            db.session.add(wallet_transaction)
            db.session.add(transaction_buy)
            db.session.commit()
            transaction_books_schema = TransactionBooksSchema()
            data_transaction = transaction_books_schema.dump(transaction_buy)
            return response_with(
                    resp.TRANSACTION_CREATED_SUCCESS_201,
                    value={
                        "data": data_transaction
                    })
        else:
            return response_with(resp.WALLET_LESS_THAN_TRANSACTION_422)
    except Exception as e:
        raise e
    
