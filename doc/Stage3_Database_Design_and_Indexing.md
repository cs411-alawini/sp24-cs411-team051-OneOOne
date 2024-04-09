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



