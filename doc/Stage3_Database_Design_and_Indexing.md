```sql
CREATE TABLE Credentials (
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE Users (
    userId INT NOT NULL AUTO_INCREMENT,
    userName VARCHAR(255) NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (userId),
    FOREIGN KEY (email) REFERENCES Credentials(email)
);

CREATE TABLE Category (
	userId INT,
    categoryId INT NOT NULL AUTO_INCREMENT,
    parentCategoryId INT,
    categoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (categoryId),
    FOREIGN KEY (parentCategoryId) REFERENCES Category(categoryId),
    FOREIGN KEY (userId) REFERENCES Users(userId)
);



CREATE TABLE Attachments (
    attachmentId INT NOT NULL AUTO_INCREMENT,
    attachmentBlob LONGBLOB,
    PRIMARY KEY (attachmentId)
    
);


CREATE TABLE Transactions (
    txnId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    note TEXT ,
    paymentMethod VARCHAR(255),
    type VARCHAR(255),
    userId INT,
    attachmentId INT, 
    categoryId INT,
     PRIMARY KEY (txnId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (categoryId) REFERENCES  Category(categoryId),
    FOREIGN KEY (attachmentId) REFERENCES Attachments(attachmentId)
);


CREATE TABLE MonthlyCategoryBudget (
    budgetId INT NOT NULL AUTO_INCREMENT,
    description TEXT ,
    amount DECIMAL(10, 2) NOT NULL,
    month DATE NOT NULL,
    categoryId INT,
    userId INT, 
    PRIMARY KEY (budgetId),

    FOREIGN KEY (categoryId) REFERENCES Category(categoryId),
    FOREIGN KEY (userId) REFERENCES Users(userId)
);


CREATE TABLE Split (
    splitId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    note TEXT ,
    lenderId INT,
    PRIMARY KEY (splitId),
    FOREIGN KEY (lenderId) REFERENCES Users(userId)
);
CREATE  TABLE Borrows(
    borrowerId INT  NOT NULL,
    splitId INT NOT NULL,
    Amount Decimal(10,2),
    isPaid Bool ,
PRIMARY KEY (borrowerId,splitId),
FOREIGN KEY (borrowerId) REFERENCES Users(userId),
FOREIGN KEY (splitId) REFERENCES Split(splitId)
);
```


<img width="876" alt="Screenshot 2024-04-08 at 4 27 04 PM" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/02cd05c4-2d9a-4ecc-b4a9-b29970633796">

<img width="413" alt="Screenshot 2024-04-08 at 4 37 07 PM" src="https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/aefd9abf-8102-42c0-9f2e-da6dc76f0657">


