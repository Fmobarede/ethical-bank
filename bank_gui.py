import tkinter as tk
# COLORS
BG_COLOR = "#EAF4F4"
BUTTON_COLOR = "#9CC53C"
BUTTON_TEXT = "white"
HEADER_COLOR = "#295326"
FRAME_COLOR = "#FFFFFF"
TF_COLOR = "#CCCCCCA5"
BACK_COLOR = "#3F7A4192"
NORM_COLOR = "#346867"
from tkinter import messagebox
from tkinter import ttk
from bank_app import get_connection
from accounts import SavingsAccount, CurrentAccount
from PIL import Image, ImageTk

role = "USER"





class LoginScreen:
    def login_screen(self):
        
        login_win = tk.Tk()

        login_win.title("Ethical Bank Login")
        login_win.geometry("400x350")
        login_win.configure(bg=BG_COLOR)

        login_frame = tk.Frame(
            login_win,
            bg="white",
            padx=20,
            pady=20
        )

        login_frame.pack(pady=20)

        tk.Label(
            login_frame,
            text="ETHICAL BANK LOGIN",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=15)

        tk.Label(
            login_frame,
            text="Username",
            bg="white"
        ).pack()

        username_entry = tk.Entry(login_frame)
        username_entry.pack(pady=5)

        tk.Label(
            login_frame,
            text="Password",
            bg="white"
        ).pack()

        password_entry = tk.Entry(
            login_frame,
            show="*"
        )
        password_entry.pack(pady=5)

        def process_login():

            username = username_entry.get()
            password = password_entry.get()

            conn = get_connection()
            cur = conn.cursor()

            try:

                cur.execute("""
                    SELECT role
                    FROM staff_users
                    WHERE username = :u
                    AND password = :p
                """, u=username, p=password)

                result = cur.fetchone()

                if result:

                    global role
                    role = result[0]

                    messagebox.showinfo(
                        "Success",
                        "Login successful!"
                    )

                    login_win.destroy()

                    menu.open_main_menu()

                else:

                    messagebox.showerror(
                        "Login Failed",
                        "Invalid username or password"
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:
                cur.close()
                conn.close()

        tk.Button(
            login_frame,
            text="🔐 Login",
            width=20,
            height=2,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Arial", 11, "bold"),
            command=process_login
        ).pack(pady=20)

        login_win.mainloop()



def style_tables():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Treeview",
        rowheight=30,
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 11, "bold")
    )

class CustomerOperations:
    
    def balance_window(self):

        win = tk.Toplevel(root)
        win.title("Check Balance")
        win.geometry("350x250")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )
        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Check Balance",
            bg="white",
            fg=HEADER_COLOR,
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Account Number",
            bg="white"
        ).pack()

        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        def check_balance():

            acc_no = acc_entry.get()

            conn = get_connection()
            cur = conn.cursor()

            try:

                cur.execute("""
                    SELECT balance
                    FROM accounts
                    WHERE account_number = :a
                """, a=acc_no)

                result = cur.fetchone()

                if result:

                    messagebox.showinfo(
                        "Balance",
                        f"Current Balance: ₦{result[0]:,.2f}"
                    )

                else:

                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:

                cur.close()
                conn.close()

        tk.Button(
            frame,
            text="Check Balance",
            bg=BUTTON_COLOR,
            fg="white",
            command=check_balance
        ).pack(pady=15)

    
    def deposit_window(self):

        win = tk.Toplevel(root)
        win.title("Deposit")
        win.geometry("350x320")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Deposit Funds",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Account Number",
            bg="white"
        ).pack()

        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        tk.Label(
            frame,
            text="Amount",
            bg="white"
        ).pack()

        amt_entry = tk.Entry(frame)
        amt_entry.pack(pady=5)

        # Deposit function
        def process_deposit():

            acc_no = acc_entry.get()

            try:
                amount = float(amt_entry.get())

            except:
                messagebox.showerror(
                    "Error",
                    "Invalid amount"
                )
                return

            if amount <= 0:

                messagebox.showerror(
                    "Error",
                    "Amount must be greater than zero"
                )
                return

            conn = get_connection()
            cur = conn.cursor()

            try:

                # CHECK ACCOUNT STATUS
                cur.execute("""
                    SELECT balance, status, account_type
                    FROM accounts
                    WHERE account_number = :a
                """, a=acc_no)

                result = cur.fetchone()
                balance = result[0]

               

                if not result:
                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )
                    return

                balance = result[0]
                status = result[1]
                account_type = result[2]

                
                if account_type == "SAVINGS":

                    account = SavingsAccount(
                        acc_no,
                        "Customer",
                        balance
                    )

                else:

                    account = CurrentAccount(
                        acc_no,
                        "Customer",
                        balance
                    )
                

                if status == "FROZEN":

                    messagebox.showerror(
                        "Blocked",
                        "Account is frozen"
                    )
                    return

                if status == "CLOSED":

                    messagebox.showerror(
                        "Blocked",
                        "Account is closed"
                    )
                    return

                # DEPOSIT
                account.deposit(amount)

                cur.execute("""
                    UPDATE accounts
                    SET balance = :bal
                    WHERE account_number = :a
                """,
                bal=account.get_balance(),
                a=acc_no
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Deposit successful!"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:

                cur.close()
                conn.close()
        # Submit button
        tk.Button(
            win,
            text="deposit",
            width=20,
            height=2,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Arial", 11, "bold"),
            command=process_deposit
        ).pack(pady=20)

    def withdraw_window(self):

        win = tk.Toplevel(root)
        win.title("Withdraw")
        win.geometry("350x320")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Withdraw Funds",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(frame, text="Account Number", bg="white").pack()
        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        tk.Label(frame, text="Amount", bg="white").pack()
        amt_entry = tk.Entry(frame)
        amt_entry.pack(pady=5)

        # Withdraw function
        def process_withdraw():

            acc_no = acc_entry.get()

            try:
                amount = float(amt_entry.get())

            except:
                messagebox.showerror(
                    "Error",
                    "Invalid amount"
                )
                return

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Amount must be greater than zero"
                )
                return

            conn = get_connection()
            cur = conn.cursor()

            try:

                # Check balance
                cur.execute("""
                    SELECT balance, status, account_type
                    FROM accounts
                    WHERE account_number = :a
                """, a=acc_no)

                result = cur.fetchone()

                if not result:

                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )
                    return

                balance = result[0]
                status = result[1]
                account_type = result[2]

                if account_type == "SAVINGS":
                    account = SavingsAccount(
                        acc_no,
                        "Customer",
                        balance
                    )
                else:
                    account = CurrentAccount(
                        acc_no,
                        "Customer",
                        balance
                    )

                if not account.withdraw(amount):

                    messagebox.showerror(
                        "Error",
                        "Insufficient balance"
                    )
                    return

                # Withdraw
                cur.execute("""
                UPDATE accounts
                    SET balance = :bal
                    WHERE account_number = :a
                """,
                bal=account.get_balance(),
                a=acc_no)

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Withdrawal successful!"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:
                cur.close()
                conn.close()

        # Button
        tk.Button(
            frame,
            text="Withdraw",
            width=20,
            height=2,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Arial", 11, "bold"),
            command=process_withdraw
        ).pack(pady=15)

    
    def transfer_window(self):

        win = tk.Toplevel(root)
        win.title("Transfer Money")
        win.geometry("400x420")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Transfer Funds",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(frame, text="Sender Account", bg="white").pack()
        sender_entry = tk.Entry(frame)
        sender_entry.pack(pady=5)

        tk.Label(frame, text="Receiver Account", bg="white").pack()
        receiver_entry = tk.Entry(frame)
        receiver_entry.pack(pady=5)

        tk.Label(frame, text="Amount", bg="white").pack()
        amount_entry = tk.Entry(frame)
        amount_entry.pack(pady=5)

        # Transfer function
        def process_transfer():

            sender = sender_entry.get()
            receiver = receiver_entry.get()

            try:
                amount = float(amount_entry.get())

            except:
                messagebox.showerror(
                    "Error",
                    "Invalid amount"
                )
                return

            if sender == receiver:

                messagebox.showerror(
                    "Error",
                    "Cannot transfer to same account"
                )
                return

            if amount <= 0:

                messagebox.showerror(
                    "Error",
                    "Amount must be greater than zero"
                )
                return

            conn = get_connection()
            cur = conn.cursor()

            try:

                # CHECK SENDER
                cur.execute("""
                    SELECT balance, status
                    FROM accounts
                    WHERE account_number = :s
                """, s=sender)

                sender_data = cur.fetchone()

                if not sender_data:

                    messagebox.showerror(
                        "Error",
                        "Sender account not found"
                    )
                    return

                sender_balance = sender_data[0]

                sender_account = SavingsAccount(
                    sender,
                    "Sender",
                    sender_balance
                )

                if not sender_account.withdraw(amount):

                    messagebox.showerror(
                        "Error",
                        "Insufficient balance"
                    )

                    return
                
                cur.execute("""
                UPDATE accounts
                SET balance = :bal
                WHERE account_number = :s
                """,
                bal=sender_account.display_balance(),
                s=sender)
                



                

                receiver_account = SavingsAccount(
                    receiver,
                    "Receiver",
                    receiver_balance
                )

                receiver_account.deposit(amount)

                cur.execute("""
                UPDATE accounts
                SET balance = :bal
                WHERE account_number = :r
                """,
                bal=receiver_account.display_balance(),
                r=receiver)
                sender_status = sender_data[1]

                if sender_status == "FROZEN":

                    messagebox.showerror(
                        "Blocked",
                        "Sender account is frozen"
                    )
                    return

                if sender_status == "CLOSED":

                    messagebox.showerror(
                        "Blocked",
                        "Sender account is closed"
                    )
                    return

                if sender_balance < amount:

                    messagebox.showerror(
                        "Error",
                        "Insufficient balance"
                    )
                    return

                # CHECK RECEIVER
                cur.execute("""
                    SELECT status
                    FROM accounts
                    WHERE account_number = :r
                """, r=receiver)

                receiver_data = cur.fetchone()

                receiver_balance = receiver_data[0]
                receiver_status = receiver_data[1]

                if not receiver_data:

                    messagebox.showerror(
                        "Error",
                        "Receiver account not found"
                    )
                    return

                receiver_status = receiver_data[0]

                if receiver_status == "FROZEN":

                    messagebox.showerror(
                        "Blocked",
                        "Receiver account is frozen"
                    )
                    return

                if receiver_status == "CLOSED":

                    messagebox.showerror(
                        "Blocked",
                        "Receiver account is closed"
                    )
                    return

                # DEDUCT SENDER
                cur.execute("""
                UPDATE accounts
                    SET balance = :bal
                    WHERE account_number = :s
                """,
                bal=sender_account.get_balance(),
                s=sender
                )

                # CREDIT RECEIVER
                cur.execute("""
                    UPDATE accounts
                    SET balance = :bal
                    WHERE account_number = :r
                """,
                bal=receiver_account.get_balance(),
                r=receiver
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Transfer successful!"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:

                cur.close()
                conn.close()



        # Button
        tk.Button(
        frame,
        text="Transfer",
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        command=process_transfer
    ).pack(pady=15)

    
    def create_account_window(self):

        win = tk.Toplevel(root)
        win.title("Create Account")
        win.geometry("450x500")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Create New Account",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(frame, text="Customer ID", bg="white").pack()
        cid_entry = tk.Entry(frame)
        cid_entry.pack()

        tk.Label(frame, text="Branch ID", bg="white").pack()
        bid_entry = tk.Entry(frame)
        bid_entry.pack()

        tk.Label(frame, text="Account Number", bg="white").pack()
        acc_entry = tk.Entry(frame)
        acc_entry.pack()

        tk.Label(frame, text="Customer Name", bg="white").pack()
        name_entry = tk.Entry(frame)
        name_entry.pack()

        tk.Label(frame, text="Initial Deposit", bg="white").pack()
        bal_entry = tk.Entry(frame)
        bal_entry.pack()

        
        # Create function
        def process_create():

            try:

                customer_id = int(cid_entry.get())
                branch_id = int(bid_entry.get())
                acc_no = acc_entry.get()
                name = name_entry.get()
                balance = float(bal_entry.get())

                conn = get_connection()
                cur = conn.cursor()

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
                """,
                cid=customer_id,
                bid=branch_id,
                acc=acc_no,
                bal=balance,
                name=name)

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Account created successfully!"
                )

                cur.close()
                conn.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )


        tk.Button(
        frame,
        text="Create Account",
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        command=process_create
    ).pack(pady=20)

####stop

##adminnnnnn
class AdminOperations:
     
    def admin_dashboard(self):

        win = tk.Toplevel(root)

        win.title("Admin Dashboard")
        win.geometry("400x350")

        tk.Label(
            win,
            text="ADMIN DASHBOARD",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        conn = get_connection()
        cur = conn.cursor()

        try:

            # Total accounts
            cur.execute("""
                SELECT COUNT(*)
                FROM accounts
            """)

            total_accounts = cur.fetchone()[0]

            # Total balance
            cur.execute("""
                SELECT SUM(balance)
                FROM accounts
            """)

            total_balance = cur.fetchone()[0]

            # Total transactions
            cur.execute("""
                SELECT COUNT(*)
                FROM transactions
            """)

            total_transactions = cur.fetchone()[0]

            # Active accounts
            cur.execute("""
                SELECT COUNT(*)
                FROM accounts
                WHERE status = 'ACTIVE'
            """)

            active_accounts = cur.fetchone()[0]

            # Labels
            tk.Label(
                win,
                text=f"Total Accounts: {total_accounts}",
                font=("Arial", 12)
            ).pack(pady=10)

            tk.Label(
                win,
                text=f"Total Balance: {total_balance}",
                font=("Arial", 12)
            ).pack(pady=10)

            tk.Label(
                win,
                text=f"Total Transactions: {total_transactions}",
                font=("Arial", 12)
            ).pack(pady=10)

            tk.Label(
                win,
                text=f"Active Accounts: {active_accounts}",
                font=("Arial", 12)
            ).pack(pady=10)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cur.close()
            conn.close()
        # Button
        tk.Button(
            win,
            text="Create Account",
            command=customer.create_account_window
        ).pack(pady=20)

        
    def close_account_window(self):

        win = tk.Toplevel(root)
        win.title("Close Account")
        win.geometry("350x250")

        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Close Account",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Account Number",
            bg="white"
        ).pack()

        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        def process_close():

            acc_no = acc_entry.get()

            conn = get_connection()
            cur = conn.cursor()

            try:

                cur.execute("""
                    UPDATE accounts
                    SET status = 'CLOSED'
                    WHERE account_number = :a
                """, a=acc_no)

                if cur.rowcount == 0:

                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )

                    return

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Account status changed to CLOSED"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:
                cur.close()
                conn.close()

        tk.Button(
        frame,
        text="Close Account",
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        command=process_close
    ).pack(pady=15)


     
    def view_all_accounts(self):

        win = tk.Toplevel(root)

        win.title("All Accounts")
        win.geometry("1000x500")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
        frame,
        text="🏦 ALL BANK ACCOUNTS",
        font=("Arial", 16, "bold"),
        bg="white",
        fg=HEADER_COLOR
        ).pack(pady=10)

        # Search label
        tk.Label(
            frame,
            text="Search Customer Name",
            bg="white"
        ).pack()

        # Search entry
        search_entry = tk.Entry(frame)
        search_entry.pack(pady=5)

        # TREEVIEW STYLE
        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )

        # Table columns
        columns = (
            "Account ID",
            "Account Number",
            "Customer Name",
            "Balance",
            "Status"
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )
        tree.pack(fill="both", expand=True, pady=10)

    def transaction_history_table(self):

        win = tk.Toplevel(root)

        win.title("Transaction History")
        win.geometry("1100x500")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="📜 TRANSACTION HISTORY",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        # TREEVIEW STYLE
        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )

        # Table columns
        columns = (
            "Transaction ID",
            "Account ID",
            "Type",
            "Amount",
            "Date"
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )
        tree.pack(fill="both", expand=True, pady=10)

        # Headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)

        tree.pack(fill="both", expand=True)

        conn = get_connection()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT transaction_id,
                    account_id,
                    transaction_type,
                    amount,
                    transaction_date
                FROM transactions
                ORDER BY transaction_date DESC
            """)

            rows = cur.fetchall()

            for row in rows:
                tree.insert("", tk.END, values=row)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cur.close()
            conn.close()

    def freeze_account(self):

        win = tk.Toplevel(root)
        win.title("Freeze Account")
        win.geometry("350x250")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Freeze Account",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Account Number",
            bg="white"
        ).pack()

        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        def process_freeze():

            acc_no = acc_entry.get()

            conn = get_connection()
            cur = conn.cursor()

            try:

                cur.execute("""
                    UPDATE accounts
                    SET status = 'FROZEN'
                    WHERE account_number = :a
                """, a=acc_no)

                if cur.rowcount == 0:

                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )

                    return

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Account frozen successfully!"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:
                cur.close()
                conn.close()

        tk.Button(
        frame,
        text="Freeze Account",
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        command=process_freeze
    ).pack(pady=15)

    def unfreeze_account(self):

        win = tk.Toplevel(root)
        win.title("Unfreeze Account")
        win.geometry("350x250")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(
            win,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Unfreeze Account",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=HEADER_COLOR
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Account Number",
            bg="white"
        ).pack()

        acc_entry = tk.Entry(frame)
        acc_entry.pack(pady=5)

        def process_unfreeze():

            acc_no = acc_entry.get()

            conn = get_connection()
            cur = conn.cursor()

            try:

                cur.execute("""
                    UPDATE accounts
                    SET status = 'ACTIVE'
                    WHERE account_number = :a
                """, a=acc_no)

                if cur.rowcount == 0:

                    messagebox.showerror(
                        "Error",
                        "Account not found"
                    )

                    return

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Account unfrozen successfully!"
                )

            except Exception as e:

                conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:
                cur.close()
                conn.close()

        tk.Button(
        frame,
        text="Unfreeze Account",
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        command=process_unfreeze
    ).pack(pady=15)

def on_enter(e):
    e.widget["bg"] = "#21867A"

def on_leave(e):
    e.widget["bg"] = BUTTON_COLOR



class MainMenu:
    def open_main_menu(self):

        global root

        root = tk.Tk()
        root.configure(bg=BG_COLOR)
        style_tables()

        root.title("Ethical Bank System")
        root.state("zoomed")


        header = tk.Frame(
            root,
            bg=HEADER_COLOR,
            height=80
        )
        header.pack(fill="x")

            

        tk.Label(
            header,
            text="🏦 ETHICAL BANK SYSTEM",
            bg=HEADER_COLOR,
            fg="white",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)

            # =========================
            # BANK STATISTICS SECTION
            # =========================

        stats_frame = tk.Frame(
            root,
            bg=BG_COLOR
        )

        stats_frame.pack(pady=15)

        conn = get_connection()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT COUNT(*)
                FROM accounts
            """)
            total_accounts = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM accounts
                WHERE status = 'ACTIVE'
            """)
            active_accounts = cur.fetchone()[0]

            cur.execute("""
                SELECT NVL(SUM(balance),0)
                FROM accounts
            """)
            total_balance = cur.fetchone()[0]

        except Exception as e:

            total_accounts = 0
            active_accounts = 0
            total_balance = 0

        finally:

            cur.close()
            conn.close()

        # Total Accounts Card
        card1 = tk.Frame(
            stats_frame,
            bg="white",
            padx=20,
            pady=10,
            relief="solid",
            bd=1
        )

        card1.pack(side="left", padx=10)

        tk.Label(
            card1,
            text="Total Accounts",
            bg="white",
            fg=HEADER_COLOR,
            font=("Arial", 10, "bold")
        ).pack()

        tk.Label(
            card1,
            text=str(total_accounts),
            bg="white",
            font=("Arial", 16, "bold")
        ).pack()


        # Active Accounts Card
        card2 = tk.Frame(
            stats_frame,
            bg="white",
            padx=20,
            pady=10,
            relief="solid",
            bd=1
        )

        card2.pack(side="left", padx=10)

        tk.Label(
            card2,
            text="Active Accounts",
            bg="white",
            fg=HEADER_COLOR,
            font=("Arial", 10, "bold")
        ).pack()

        tk.Label(
            card2,
            text=str(active_accounts),
            bg="white",
            font=("Arial", 16, "bold")
        ).pack()


        # Total Balance Card
        card3 = tk.Frame(
                stats_frame,
                bg="white",
                padx=20,
                pady=10,
                relief="solid",
                bd=1
            )

        card3.pack(side="left", padx=10)

        tk.Label(
            card3,
            text="Total Balance",
            bg="white",
            fg=HEADER_COLOR,
            font=("Arial", 10, "bold")
        ).pack()

        tk.Label(
            card3,
            text=f"₦{total_balance:,.2f}",
            bg="white",
            font=("Arial", 16, "bold")
        ).pack()


            # =========================
            # LOGO SECTION
            # =========================

        content_frame = tk.Frame(
            root,
            bg=BG_COLOR
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )



            ##ediie

        menu_container = tk.Frame(
            content_frame,
            bg=BG_COLOR
        )

        menu_container.pack(
            side="left",
            padx=20,
            anchor="n"
        )


        canvas = tk.Canvas(
            content_frame,
            bg=BG_COLOR,
            highlightthickness=0,
            width=350      # fixed width
        )

        scrollbar = tk.Scrollbar(
            content_frame,
            orient="vertical",
            command=canvas.yview
        )

            ##############
        logo_frame = tk.Frame(
            content_frame,
            bg="white",
            padx=20,
            pady=20
        )

        logo_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=40
        )


        image = Image.open(
            r"C:\Users\HP\Desktop\ethbnksys.png"
        )

        image = image.resize((400, 400))

        logo_photo = ImageTk.PhotoImage(image)

        logo_label = tk.Label(
            logo_frame,
            image=logo_photo,
            bg="white"
        )

        logo_label.image = logo_photo
        logo_label.pack()

        tk.Label(
            logo_frame,
            text="Banking with Integrity",
            font=("Arial", 12, "italic"),
            bg="white",
            fg="#666666"
        ).pack(pady=5)

        scrollable_frame = tk.Frame(
            canvas,
            bg=FRAME_COLOR
        )

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="left",
            fill="y"
        )





            # NORMAL BUTTONS
        tk.Label(
            scrollable_frame,
            text="CUSTOMER OPERATIONS",
            font=("Arial", 13, "bold"),
            bg=FRAME_COLOR,
            fg=HEADER_COLOR
        ).pack(pady=10)

        def create_button(parent, text, command):

            btn = tk.Button(
                parent,
                text=text,
                width=25,
                height=2,
                bg=BUTTON_COLOR,
                fg="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                command=command
            )

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            return btn

        create_button(
                scrollable_frame,
                "🏦 Create Account",
                customer.create_account_window
            ).pack(pady=8)


        create_button(
            scrollable_frame,
            "Check Balance",
            customer.balance_window
        ).pack(pady=8)
            

        create_button(
            scrollable_frame,
            "💰 Deposit",
            customer.deposit_window
        ).pack(pady=8)
            
        create_button(
            scrollable_frame,
            "💸 Withdraw",
            customer.  withdraw_window
        ).pack(pady=8)

        create_button(
            scrollable_frame,
            "🔁 Transfer",
            customer.transfer_window
        ).pack(pady=8)


        create_button(
            scrollable_frame,
            "📜 History",
            admin.transaction_history_table
        ).pack(pady=8)
    

        create_button(
            scrollable_frame,
            "View All Accounts",
            admin.view_all_accounts
        ).pack(pady=8)
    

        # ADMIN ONLY
        if role == "ADMIN":

            tk.Label(
                scrollable_frame,
                text="ADMIN OPERATIONS",
                font=("Arial", 13, "bold"),
                bg=FRAME_COLOR,
                fg=HEADER_COLOR
            ).pack(pady=10)


            create_button(
                scrollable_frame,
                "📊 Admin Dashboard",
                admin.admin_dashboard
            ).pack(pady=8)
            
    
            create_button(
                scrollable_frame,
                "Close Account",
                admin.close_account_window
            ).pack(pady=8)     
            

            create_button(
                scrollable_frame,
                "❄️ Freeze Account",
                admin.freeze_account
            ).pack(pady=8)

            create_button(
                scrollable_frame,
                "🔄 Unfreeze Account",
                admin.unfreeze_account
            ).pack(pady=8)
        

        # EXIT BUTTON
        create_button(
            scrollable_frame,
            "🚪 Exit",
            root.quit
        ).pack(pady=8)




    
        root.mainloop()


# OBJECTS
login = LoginScreen()
customer = CustomerOperations()
admin = AdminOperations()
menu = MainMenu()

# Start Application
login.login_screen()