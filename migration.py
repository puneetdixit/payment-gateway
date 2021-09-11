from src.database_manager import Database
import src.models

database = Database()


print("Going to Drop tables...")
database.db.drop_tables((src.models.ResponseCodes, src.models.Transactions))
print("Tables dropped successfully")
print("Going to create tables")
database.db.create_tables((src.models.ResponseCodes, src.models.Transactions))
print("Tables created successfully")
