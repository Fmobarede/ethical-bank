import os
from dotenv import load_dotenv

load_dotenv()

# Connection details
username = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")
dsn = os.getenv("ORACLE_DSN")
host = "localhost"
port = 1521
service_name = "XEPDB1"

# Build the connection string
dsn = oracledb.makedsn(host, port, service_name=service_name)

try:
    # Connect
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    print("✅ Successfully connected to Oracle Database!")
    
    # Test a query
    cursor = connection.cursor()
    cursor.execute("SELECT first_name, last_name, email FROM customers")
    
    print("\n📋 Customers in database:")
    print("-" * 50)
    for row in cursor:
        print(f"  Name: {row[0]} {row[1]} | Email: {row[2]}")
    
    cursor.close()
    connection.close()
    print("\n✅ Connection test completed successfully!")
    
except oracledb.DatabaseError as e:
    error_obj = e.args[0]
    print(f"❌ Database Error: {error_obj.code} - {error_obj.message}")
    
except Exception as e:
    print(f"❌ Error: {e}")