1. Create two database models
   1.1 Transaction
      1.1.1 id - int unique unsigned autoincrement; wallet_id (fkey) - int; txid - unique string (pkey); amount - decimal 18 precision
   1.2 Wallet 
      1.2.1 id (pkey); label - string; balance - decimal 18 precision (default 0, unsigned (nonegative))


2. Logic
    2.1 Wallet's Balance is the sum of all transaction amounts
    2.2 Transaction amount might be the negative number
    2.3 Wallet balance should never be the negative
    2.4 Transaction amount should not exceed wallet's balance amount

3. API design - CRUD
   1. Create Wallet (return id) - POST
   2. Read Wallet (details) - GET
   3. Read Wallets (list + pagination + sorting) - GET
   4. Update Wallet (by id) - PATCH
   5. Delete Wallet (by id) - DELETE
   6. Create Transaction (input wallet id) - POST
   7. Read Transaction (detail of one transaction by transaction ID) - GET
   8. Read Transactions (by wallet id) - GET
   9. Update Transaction (by transaction ID) - PATCH
   10. Delete Transaction (by transaction ID) - DELETE

4. TODO: Apply fixtures and mock data dump
5. Do not forget about enumerators and __init__.py __all__ = []

6. Transaction output serializer
   1. List of transactions with Wallet details in it