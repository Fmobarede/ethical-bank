import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )

    print("Connected to Oracle Database successfully!")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM loans")

    for row in cursor:
        print(row)

    cursor.close()
    connection.close()

except Exception as e:
    print("Connection failed:", e)