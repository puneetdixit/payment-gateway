PORT = 5000

DB_HOST = "localhost"
DB_PORT = 3306
DB_USERNAME = "root"
DB_PASSWORD = "Puneet@321"
DB_NAME = "payment_gateway"



UPDATE_RESPONSE_CODES = True

RESPONSE_CODES = {
    101: "Payment success 1",
    102: "Payment success 2",
    201: "Invalid card number",
    202: "Insufficient funds",
    203: "Invalid CVV number"
}

