# payment-gateway

This is the server for payment-gateway in Python3 language using FastAPI Framework. MySql as a 
Database and Peewee ORM to communicate with the database.

# Steps to setup this server

1. Create a virtual enviroment with python3
2. Install requirements.txt file
3. Run python migration.py - It will migrate tables and add response codes value
4. Run python app.py


Your server will run on 127.0.0.1:5000 or you can change your server port from settings.py file. 


To connect with database change in settings.py file accordingly.
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USERNAME = "root"
    DB_PASSWORD = "abc@321"
    DB_NAME = "movies_data

# APIs
1. Go to http://127.0.0.1:5000/docs it will return openapi Swagger UI and there is an post request. Just try it out and fill all the required fields and execute command. It will give you response accordingly

2. To see all the transactions details just go to http://127.0.0.1:5000/transactions it will redirect you to a html page and will show you all transactions.