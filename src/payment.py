import datetime
import random

import settings
from src.database_manager import Database
from src.models import Transactions

database = Database()


def get_random_response_code():
    """
    This function is used to get a random response code from.
    :return:
    """
    return random.choice(settings.RESPONSE_CODES)


def initiate_payment(amount, currency, card_type, card_details):
    """
    This function will be used to communicate with bank server based on given params.
    :param amount:
    :param currency:
    :param card_type:
    :param card_details:
    :return boolean and resp_code:
    """
    resp_code = get_random_response_code()

    if str(resp_code).startswith('1'):
        return True, resp_code

    return False, resp_code


def get_transaction_data(amount, currency, txn_id, card, type):
    """
    This function is used to get the transaction data.
    :param amount:
    :param currency:
    :param txn_id:
    :param card:
    :param type:
    :return transaction_data:
    """
    transaction_time = str(datetime.datetime.now())
    status, resp_code = initiate_payment(amount, currency, txn_id, card, type)

    Transactions.insert(transaction_id=txn_id, amount=amount, currency=currency, card_type=type, time=transaction_time,
                        resp_code=resp_code, txn_status="success" if status else "failure").execute()

    transaction_data = {
        "amount": amount,
        "currency": currency,
        "type": type,
        "card": {
            "number": card.number,
        },
        "txn_id": txn_id,
        "status": "success" if status else "failure",
        "time": str(datetime.datetime.now()),
        "resp_code": resp_code
    }

    return transaction_data
