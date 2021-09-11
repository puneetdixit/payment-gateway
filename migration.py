from src.database_manager import Database
import src.models
import settings

database = Database()

def migrate_tables():
    print("Going to Drop tables...")
    database.db.drop_tables((src.models.ResponseCodes, src.models.Transactions))
    print("Tables dropped successfully")
    print("Going to create tables")
    database.db.create_tables((src.models.ResponseCodes, src.models.Transactions))
    print("Tables created successfully")

def create_response_code_values():
    for code, desc in settings.RESPONSE_CODES.items():
        src.models.ResponseCodes.insert(code=code, description=desc).execute()
    print("Responses added successfully")


migrate_tables()
if settings.UPDATE_RESPONSE_CODES:
    create_response_code_values()