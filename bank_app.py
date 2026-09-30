import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )


# ---------------- CREATE ACCOUNT ----------------
def create_account():
    conn = get_connection()
    cur = conn.cursor()

    try:
        customer_id = int(input("Enter Customer ID: "))
        branch_id = int(input("Enter Branch ID: "))
        acc_no = input("Enter Account Number: ")
        name = input("Enter Customer Name: ")
        balance = float(input("Initial Deposit: "))

        cur.execute("""
            INSERT INTO accounts (
                account_id,
                customer_id,
                branch_id,
                account_number,
                account_type,
                balance,
                status,
                created_at,
                customer_name
            )
            VALUES (
                account_seq.NEXTVAL,
                :cid,
                :bid,
                :acc,
                'SAVINGS',
                :bal,
                'ACTIVE',
                SYSDATE,
                :name
            )
        """, cid=customer_id,
             bid=branch_id,
             acc=acc_no,
             bal=balance,
             name=name)

        conn.commit()
        print("Account created successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- CHECK BALANCE ----------------
def view_balance():
    conn = get_connection()
    cur = conn.cursor()

    try:
        acc_no = input("Enter Account Number: ")

        cur.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = :a
        """, a=acc_no)

        result = cur.fetchone()

        if result:
            print("Balance:", result[0])
        else:
            print("Account not found")

    finally:
        cur.close()
        conn.close()


# ---------------- DEPOSIT ----------------
def deposit():
    conn = get_connection()
    cur = conn.cursor()

    try:
        acc_no = input("Enter Account Number: ")
        amount = float(input("Amount to Deposit: "))

        if amount <= 0:
            print("Invalid amount")
            return

        cur.execute("""
            UPDATE accounts
            SET balance = balance + :amt
            WHERE account_number = :a
        """, amt=amount, a=acc_no)

        if cur.rowcount == 0:
            print("Account not found")
            return

        conn.commit()
        print("Deposit successful!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- WITHDRAW ----------------
def withdraw():
    conn = get_connection()
    cur = conn.cursor()

    try:
        acc_no = input("Enter Account Number: ")
        amount = float(input("Amount to Withdraw: "))

        if amount <= 0:
            print("Invalid amount")
            return

        cur.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = :a
        """, a=acc_no)

        result = cur.fetchone()

        if not result:
            print("Account not found")
            return

        if result[0] < amount:
            print("Insufficient balance")
            return

        cur.execute("""
            UPDATE accounts
            SET balance = balance - :amt
            WHERE account_number = :a
        """, amt=amount, a=acc_no)

        conn.commit()
        print("Withdrawal successful!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- TRANSFER ----------------
def transfer_money():
    conn = get_connection()
    cur = conn.cursor()

    try:
        sender = input("Sender Account Number: ")
        receiver = input("Receiver Account Number: ")
        amount = float(input("Amount: "))

        if sender == receiver:
            print("Cannot transfer to same account")
            return

        if amount <= 0:
            print("Invalid amount")
            return

        # Check sender
        cur.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = :s
        """, s=sender)

        sender_data = cur.fetchone()

        if not sender_data:
            print("Sender account not found")
            return

        if sender_data[0] < amount:
            print("Insufficient balance")
            return

        # Check receiver
        cur.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = :r
        """, r=receiver)

        receiver_data = cur.fetchone()

        if not receiver_data:
            print("Receiver account not found")
            return

        # Transfer
        cur.execute("""
            UPDATE accounts
            SET balance = balance - :amt
            WHERE account_number = :s
        """, amt=amount, s=sender)

        cur.execute("""
            UPDATE accounts
            SET balance = balance + :amt
            WHERE account_number = :r
        """, amt=amount, r=receiver)

        conn.commit()
        print("Transfer successful!")

    except Exception as e:
        conn.rollback()
        print("Transfer failed:", e)

    finally:
        cur.close()
        conn.close()




 # ---------------- CLOSE ACCOUNT ----------------


def close_account():
    conn = get_connection()
    cur = conn.cursor()

    try:
        acc_no = input("Enter Account Number to Close: ")

        cur.execute("""
            DELETE FROM accounts
            WHERE account_number = :a
        """, a=acc_no)

        if cur.rowcount == 0:
            print("Account not found")
            return

        conn.commit()
        print("Account closed successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()



# ---------------- TRANSACTION HISTORY ----------------
def transaction_history():
    conn = get_connection()
    cur = conn.cursor()

    try:
        acc_no = input("Enter Account Number: ")

        cur.execute("""
            SELECT t.transaction_type,
                   t.amount,
                   t.transaction_date
            FROM transactions t
            JOIN accounts a
            ON t.account_id = a.account_id
            WHERE a.account_number = :acc
            ORDER BY t.transaction_date DESC
        """, acc=acc_no)

        records = cur.fetchall()

        if not records:
            print("No transactions found")
            return

        print("\n--- Transaction History ---")

        for row in records:
            print(
                "Type:", row[0],
                "| Amount:", row[1],
                "| Date:", row[2]
            )

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- STAFF LOGIN ----------------
def login():

    conn = get_connection()
    cur = conn.cursor()

    try:
        username = input("Username: ")
        password = input("Password: ")

        cur.execute("""
            SELECT role
            FROM staff_users
            WHERE username = :u
            AND password = :p
        """, u=username, p=password)

        result = cur.fetchone()

        if result:
            print("Login successful!")
            return result[0]   # returns role

        else:
            print("Invalid username or password")
            return None

    finally:
        cur.close()
        conn.close()


# ---------------- SEARCH ACCOUNT ----------------
def search_account():

    conn = get_connection()
    cur = conn.cursor()

    try:
        keyword = input("Enter Account Number or Customer Name: ")

        cur.execute("""
            SELECT account_number,
                   customer_name,
                   balance,
                   status
            FROM accounts
            WHERE account_number = :k
            OR LOWER(customer_name) LIKE LOWER(:name)
        """, k=keyword, name='%' + keyword + '%')

        records = cur.fetchall()

        if not records:
            print("No matching account found")
            return

        print("\n--- Search Results ---")

        for row in records:
            print(
                "Account:", row[0],
                "| Name:", row[1],
                "| Balance:", row[2],
                "| Status:", row[3]
            )

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- REPORTS DASHBOARD ----------------
def reports_dashboard():

    conn = get_connection()
    cur = conn.cursor()

    try:

        # Total accounts
        cur.execute("SELECT COUNT(*) FROM accounts")
        total_accounts = cur.fetchone()[0]

        # Total balance
        cur.execute("SELECT SUM(balance) FROM accounts")
        total_balance = cur.fetchone()[0]

        # Total transactions
        cur.execute("SELECT COUNT(*) FROM transactions")
        total_transactions = cur.fetchone()[0]

        print("\n===== BANK REPORTS DASHBOARD =====")
        print("Total Accounts:", total_accounts)
        print("Total Bank Balance:", total_balance)
        print("Total Transactions:", total_transactions)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- MENU ----------------
role = login()

if role:

    while True:

        print("\n===== ETHICAL BANK SYSTEM =====")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Close Account")
        print("7. Transaction History")
        print("8. Search Account")
        print("9. Reports Dashboard (ADMIN only)")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            view_balance()

        elif choice == "3":
            deposit()

        elif choice == "4":
            withdraw()

        elif choice == "5":
            transfer_money()

        elif choice == "6":

            if role != "ADMIN":
                print("Access denied. ADMIN only.")

            else:
                close_account()

        elif choice == "7":
            transaction_history()

        elif choice == "8":
             search_account()

        elif choice == "9":     
            if role != "ADMIN":
                print("Access denied. ADMIN only.")

            else:
                reports_dashboard()

        elif choice == "10":
            print("Thank you for using Ethical Bank!")
            break

        else:
            print("Invalid choice. Try again.")