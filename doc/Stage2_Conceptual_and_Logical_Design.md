## Conceptual and Logical Design

### 1 UML Diagram
![expense_manager_UML](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/9f29daa0-49ba-45eb-8d15-4591170f41a6)


### 2 Entities

#### 2.1 Transaction
  This is the central entity that represents all the expenses and income with additional information regarding the payment method and type of expense.
  
  Assumptions:
  - The given attributes are assumed to be limited to the following values
      - PaymentMethod: [‘Cash, ’Credit Card’, ‘Debit Card’, ‘Zelle’]
      - Type: [‘Income’, ‘Expense’]
  - A subcategory can be added to a transaction if and only its parent category is present in the category field.
  - Amount can't be negative.

#### 2.2 Category
This entity represents the categories and subcategories that a transaction belongs to.
To achieve this we are adding a parentCategoryId attribute which will be null for categories and have the respective categoryId, of it's parent category, for a subcategory.
  ##### Assumptions:
  - A transaction can have one category at max.
  - At most one subcategory can be added to a transaction.


#### 2.3 Attachment
The Attachment entity represents the receipts or any other transaction-related documents in image or PDF format.

  ##### Assumptions:
  - There could be 0 or 1 attachment for a given transaction.

#### 2.4 MonthlyCategoryBudget
This represents a category-wise budget changing every month.

  ##### Assumptions:
  - The Month is an integer having values between 1 and 12.
  - Amount can't be negative.

#### 2.5  User
The user details such as username, first and last name are stored in this entity.

  ##### Assumptions:
  - Username is unique to a user

#### 2.6  Credentials
This entity is used to store password and email for handling the login process. This entity is separated from the user entity for allowing quicker access for authentication.


#### 2.7  Split
This is a central entity for handling the splitting functionality. It stores details regarding the split such as timestamp, amount, etc.

  ##### Assumptions:
  - Amount can't be negative.


### 3 Relations

- A Transaction might have 0 or 1 attachment associated with it. An Attachment has exactly 1 transaction associated with it. (One to One Relationship)
- A Transaction can also have 0 or 1 category. A Category can be associated with 0 or n transactions. (One to Many Relationship)
- A Category can have 0 or n Budgets associated with it. A budget is associated with exactly 1 category. (Many to One Relationship)
- A user creates 0 or n monthly budgets. A Budget is associated with exactly 1 user. (Many to One Relationship)
- A user has exactly 1 credential. A credential is associated with exactly 1 user. (One to One Relationship)
- A user adds 0 or n transactions. A transaction is associated with exactly 1 user.(Many to One Relationship)
- A user can lend in 0 or n splits. A split has exactly 1 user as lender. (Many to One Relationship)
- A user can borrow from 0 or n splits. A split can involve 1 or n users as borrowers. (Many to Many Relationship). This relationship has amount and isPaid (boolean) as attributes.

### 4 Normalization
The functional dependencies are-
1. userId -> userName, firstName, lastName
2. email -> password
3. txnId -> title, timestamp, amount, paymentMethod, note, type
4. attachmentId -> blob
5. categoryId -> parentCategoryId, categoryName
6. splitId -> title, timestamp, amount, note
7. budgetId -> description, amount, month

A relation is in 3NF if at least one of the following conditions holds in every non-trivial function dependency X –> Y :
* X is a super key.
* Y is a prime attribute (each element of Y is part of some candidate key).

A relation is in BCNF if -
* The relation is in 3NF.
* X should be a superkey for every functional dependency X−>Y in a given relation. 

Every LHS in the FD’s is the primary key of the relation and two attribute relations are always in BCNF so the schema is in BCNF form.


### 5 Relational Schema 
```
User (
  userId : INT [PK],
  userName : VARCHAR(X),
  firstName : VARCHAR(X),
  lastName : VARCHAR(X),
)

UserCredentials (
  userId : INT [FK to user.userId],
  email : VARCHAR(X) [PK],
  passwordsHash : VARCHAR(X)
)

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
)

Attachment(
	AttachmentId: INT [PK],
	Blob: BLOB,
)

Category(
	categoryId : INT [PK],
  userId : INT [FK to user.userId],
  parentCategoryId : INT [FK to Category.categoryId],
	categoryName : VARCHAR(X)
)

MonthlyCategoryBudget(
	budgetId: INT [PK],
	description: VARCHAR(X),
	amount: DECIMAL,
	categoryId: INT [FK to Category.categoryId],
  month : INT [1 to 12]
)

Split (
  splitId : INT [PK],
  title : VARCHAR(X),
  timestamp : DATETIME,
  amount : REAL,
  note : VARCHAR(X),
  lenderId : INT [FK to user.userId]
)


Borrower (
  borrowerId : INT [FK to user.userId],
  splitId : INT [FK to Split.splitId],
  amount : REAL,
  isPaid : BOOLEAN
  (borrowerId, splitId) : [PK]
)
```

