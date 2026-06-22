import mysql.connector
def get_connection():
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root@122',
        database='flask_db'
    )
    return connection