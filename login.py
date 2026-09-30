import oracledb
import os
from dotenv import load_dotenv

# Reusable DB connection
def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )

def login():
    connection = get_connection()
    cursor = connection.cursor()

    print("=== EthicalBridge Bank Login ===")

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("""
        SELECT user_id, username, role
        FROM users
        WHERE username = :u AND password = :p
    """, u=username, p=password)

    user = cursor.fetchone()

    if user:
        print("\nLogin successful!")
        print("Welcome:", user[1])
        print("Role:", user[2])
    else:
        print("\nInvalid username or password")

    cursor.close()
    connection.close()

login()