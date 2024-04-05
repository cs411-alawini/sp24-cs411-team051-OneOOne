
User (
    userId : INT [PK],
    userName : VARCHAR(X),
    firstName : VARCHAR(X),
    lastName : VARCHAR(X),
);

UserCredentials (
    userId : INT [PK],
    email : VARCHAR(X),
    passwordsHash : VARCHAR(X) [FK to user.userId],
);

Transaction (
    txnId : INT [PK],
    title : VARCHAR(X),
    timestamp : DATETIME,
    note : VARCHAR(X),
    amount : REAL, 
    categoryId : INT [FK to Category.categoryId],
    paymentMethod : [‘Cash, ’Credit Card’, ‘Debit Card’, ‘Zelle’],
	transactionType : [‘Income’, ‘Expense’],
    attachmentId : INT [FK to Attachment.AttachmentId],
    userId : INT [FK to user.userId]
);

Attachment(
	AttachmentId: INT [PK],
	Blob: BLOB,
);

Category(
	categoryId : INT [PK],
    userId : INT [FK to user.userId],
    parentCategoryId : INT [FK to Category.categoryId]
	categoryName : VARCHAR(X)
);

Split (
    splitId : INT [PK],
    title : VARCHAR(X),
    timestamp : DATETIME,
    amount : REAL,
    note : VARCHAR(X),
    lenderId : INT [FK to user.userId]
);


Borrower (
    borrowerId : INT [FK to user.userId],
    splitId : INT [FK to Split.splitId],
    amount : REAL,
    isPaid : BOOLEAN
    (borrowerId, splitId) : [PK]
);








