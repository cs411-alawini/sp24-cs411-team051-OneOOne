```sql
CREATE TABLE User (
    userId INT NOT NULL AUTO_INCREMENT,
    userName VARCHAR(255) UNIQUE NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    PRIMARY KEY (userId)
);

CREATE TABLE Credentials (
    email VARCHAR(255) NOT NULL,
    userId INT UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

CREATE TABLE Category (
	userId INT NOT NULL,
    categoryId INT NOT NULL AUTO_INCREMENT,
    parentCategoryId INT,
    categoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (categoryId),
    FOREIGN KEY (parentCategoryId) REFERENCES Category(categoryId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

CREATE TABLE Attachment (
    attachmentId INT NOT NULL AUTO_INCREMENT,
    attachmentBlob LONGBLOB,

    PRIMARY KEY (attachmentId)
    
);

CREATE TABLE Transaction (
    txnId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    note TEXT ,
    paymentMethod VARCHAR(255),
    type VARCHAR(255) NOT NULL,
    userId INT NOT NULL,
    attachmentId INT UNIQUE, 
    categoryId INT,
    
    PRIMARY KEY (txnId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (categoryId) REFERENCES  Category(categoryId),
    FOREIGN KEY (attachmentId) REFERENCES Attachment(attachmentId)
);

CREATE TABLE MonthlyCategoryBudget (
    budgetId INT NOT NULL AUTO_INCREMENT,
    description TEXT ,
    amount DECIMAL(10, 2) NOT NULL,
    month DATE NOT NULL,
    categoryId INT NOT NULL,
    userId INT NOT NULL, 
    PRIMARY KEY (budgetId),

    FOREIGN KEY (categoryId) REFERENCES Category(categoryId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

CREATE TABLE Split (
    splitId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    note TEXT ,
    lenderId INT NOT NULL,
    PRIMARY KEY (splitId),
    FOREIGN KEY (lenderId) REFERENCES User(userId)
);

CREATE  TABLE Borrows(
    borrowerId INT  NOT NULL,
    splitId INT NOT NULL,
    Amount Decimal(10,2) NOT NULL,
    isPaid Bool NOT NULL,
PRIMARY KEY (borrowerId,splitId),
FOREIGN KEY (borrowerId) REFERENCES User(userId),
FOREIGN KEY (splitId) REFERENCES Split(splitId)
);
```


<img width="876" alt="Screenshot 2024-04-08 at 4 27 04 PM" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/02cd05c4-2d9a-4ecc-b4a9-b29970633796">

<img width="410" alt="Screenshot 2024-04-08 at 11 48 13 PM" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/55f3ddc9-f1a6-4469-b9ea-b5563741e5e1">

## Indexing

#### 1. For a given user, get their current month's category budgets and actual category expenses

```
SELECT categoryId, categoryName, budget, expense  
FROM (SELECT categoryId, amount as budget FROM MonthlyCategoryBudget 
	WHERE userId = 1 and YEAR(month) = 2024 and MONTH(month) = 5) as CurrentBudgets 
	NATURAL JOIN 
	(SELECT sum(amount) as expense, categoryId from Transaction 
	WHERE userId = 1  and YEAR(timestamp) = 2024 and MONTH(timestamp) = 5 group by categoryId) as Expenses
	NATURAL JOIN Category;
```
Result is 3 rows

<img width="535" alt="image" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/da331383-87bd-497b-b09c-f34bbd09416e">


##### Indexes
1. Default => cost = 553.14
   <img width="1433" alt="image" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/e98170b5-c521-40be-86b8-7faff4dfb995">
2. Add indexing on userId transaction => cost = 553.14
   <img width="1440" alt="image" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/80e6cd96-2593-4915-8dee-86d574b8b4d4">
3. Add indexing on userId on MonthlyCategoryBudget => cost = 553.14
   <img width="1440" alt="image" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/020e1f5c-1b57-4916-bbc4-b759f065ebec">
4. Add indexing on categoryId, userId on MonthlyCategoryBudget => cost = 149.97
   <img width="1434" alt="image" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/688994a2-55a1-4bdb-a4dd-c1c8692a7841">


The default behaviour of the query shows that it is looking up Transaction table for userId key. Therefore it was the first candidate for indexing, but after adding indexing on Transaction for userId attribute we did not see any improvement in the performance. Next, the query was looking up on MonthlyCategoryBudget on userId. Similarly, adding an index on userId to MonthlyCategoryBudget did not improve the performance. The previous both indexes do not enhance the performance because in userId is a foreign key in both tables and indexing is already present in the database. Next, we tried a composite index of (userId and categoryId) on MonthlyCategoryBudget because they are being accessed together in the WHERE clause. This index significantly reduces the cost to 149.97 from previous 553.14. Hence, the composite index of (userId and categoryId) on MonthlyCategoryBudget gives the best performance amongst the tried indexes.






