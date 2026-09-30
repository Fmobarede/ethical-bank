Ethical Bank System

An object-oriented banking application built with Python, Tkinter, and Oracle Database. The system provides core banking operations while demonstrating OOP concepts such as encapsulation, inheritance, abstraction, and polymorphism.

Features
User login and authentication
Account creation and management
Balance enquiry
Deposits and withdrawals
Fund transfers
Transaction history
Loan information
Admin operations
Oracle Database integration
Object-oriented banking models
Technologies
Python
Tkinter — Graphical User Interface
Oracle Database — Data storage
oracledb — Oracle database connectivity
python-dotenv — Environment variable management
Project Structure
ethical-bank/
├── accounts.py
├── bank_app.py
├── bank_gui.py
├── db_connect.py
├── login.py
├── test_db.py
├── static/
├── sql/
├── templates/
├── .env
└── .gitignore

.env contains local database credentials and should never be committed to GitHub.

Setup
1. Clone the repository
git clone https://github.com/Fmobarede/ethical-bank.git
cd ethical-bank
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install oracledb python-dotenv
Oracle Database Configuration

The application uses an Oracle database with the following connection format:

Host: localhost
Port: 1521
Service: XEPDB1

Create a .env file in the project root:

ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=localhost:1521/XEPDB1

Replace the username and password with your local Oracle database credentials.

Make sure the required database tables have been created before running the application.

Running the Application

Activate the virtual environment:

venv\Scripts\activate

Then run the GUI application:

python bank_gui.py

To test the Oracle database connection:

python test_db.py
Security

Database credentials are loaded from environment variables and .env is excluded through .gitignore.

Never commit database passwords or other sensitive credentials to GitHub.

Author
Fmobarede
