import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rajanandini@12",
        database="ecommerce_db"
    )
    return conn