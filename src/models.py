import peewee

from src.database_manager import Database

database = Database()

class ResponseCodes(peewee.Model):
    """
    This is the model of response codes table and it will contain response code and description of that code.
    """
    code = peewee.PrimaryKeyField()
    description = peewee.CharField()

    class Meta:
        database = database.db
        db_table = "responses_codes"

class Transactions(peewee.Model):
    """
    This is the model of transaction table and it will contain all data of every transaction.
    """
    transaction_id = peewee.CharField(primary_key=True)
    amount = peewee.IntegerField()
    currency = peewee.CharField()
    card_type = peewee.CharField()
    card_number = peewee.CharField()
    time = peewee.DateTimeField()
    resp_code = peewee.IntegerField()
    txn_status = peewee.CharField(choices=["success", "failure"])

    class Meta:
        database = database.db
        db_table = "transactions"
