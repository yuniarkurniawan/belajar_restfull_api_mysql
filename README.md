# belajar restfull-api menggunakan flask dan postgresql
This tutorial contains :
 1. User (create, email verification, token, login, avatar image),
 2. Wallet topup,
 3. Books list,
 4. Transaction (buy books based on balance wallet and stock of books).

The api use 3 tier architecture, you can see from structure below :

blablusimple
 |-- api/
 |   |--- __init__.py
 |   |--- config/
 |   |--- models/
 |   |--- routes/
 |   |--- services/
 |   |--- tests/
 |   |--- utils/
 |-- cover/
 |-- images/
 |-- .coverage
 |-- main.py
 |-- run.py

Each endpoint :
 1. Tested using unittest2, and make temporary sqlite file
 2. Coverage to see useable percentage of it
 
