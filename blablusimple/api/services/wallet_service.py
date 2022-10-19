from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import Users, UsersSchema
from api.models.wallet import Wallet, WalletTransaction, \
    WalletSchema, WalletTransactionSchema
from api.utils.database import db


def top_up_wallet_service(data):
    try:
        if data['top_up'] <= 0:
            return response_with(resp.TOTAL_TOP_LESS_THAN_ZERO_422)

        debit = float(data['top_up'])
        wallet = Wallet.query.filter_by(user_id=data['user_id']).first()
        wallet_transaction = WalletTransaction(wallet_id=wallet.id,
                                               debit=debit,
                                               credit=0)
        db.session.add(wallet_transaction)
        wallet.wallet_balance = wallet.wallet_balance + debit
        db.session.commit()

        return response_with(
            resp.TOP_UP_CREATED_SUCCESS_201,
            value={
                "data": {
                    "user": wallet.user.username,
                    "top_up": debit
                }
            })

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


def get_wallet_user_service(user_id):
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    return response_with(
            resp.SUCCESS_200,
            value={
                "data": {
                    "user": wallet.user.username,
                    "email": wallet.user.email,
                    "balance": wallet.wallet_balance
                }
            })
