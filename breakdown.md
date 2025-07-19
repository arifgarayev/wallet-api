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

