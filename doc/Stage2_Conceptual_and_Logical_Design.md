## Conceptual and Logical Design

### 1 UML Diagram
![expense_manager_UML](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/9f29daa0-49ba-45eb-8d15-4591170f41a6)


### 2 Entities

#### 2.1 Transaction
  This is the central entity that represents all financial exchange with additional information like the payment method and type of exchange.
  
  Assumptions:
  - The given attributes are assumed to be limited to the following values
      - PaymentMethod: [‘Cash, ’Credit Card’, ‘Debit Card’, ‘Zelle’]
      - Type: [‘Income’, ‘Expense’]
  - Amount can't be negative.

#### 2.2 Category
This entity represents the categories that a transaction belongs to eg. household, healthcare etc. We are providing hierarchical nesting of categories by introducing parentId in this table, where each category may have a parent category. This will allow the user to drill down expenses into subcategories.
 eg. 
 | id |parentId| category |
|--|--|--|
| 0 |null|Household  |
|1|0|Rent|

Here Rent is a subcategory of Household.
  ##### Assumptions:
  - At most one category can be added to a transaction.
  - There would be only one level of nesting, ie subcategories would not have any further subcategories.


#### 2.3 Attachment
The Attachment entity represents the receipts or any other transaction-related documents in image or PDF format.

##### Assumptions:
  - There could be 0 or 1 attachment for a given transaction.

#### 2.4 MonthlyCategoryBudget
This represents a category-wise budget for a month and year.
For eg. User can set a budget of 80$ for dining out for the month of May 2024

  ##### Assumptions:
  - Amount can't be negative.

#### 2.5  User
The user details such as username, first and last name are stored in this entity.

  ##### Assumptions:
  - Username and emailId is unique to a user

#### 2.6  Credentials
This entity is used to store password and email for handling the login process. This entity is separated from the user entity for allowing quicker access for authentication. This design promotes better security practices by enabling more granular access controls.


#### 2.7  Split
This is a central entity for handling the expense sharing functionality. It stores details regarding the split such as timestamp, amount, lender, etc.

  ##### Assumptions:
  - Amount can't be negative.
  - Each shared expense has atleast 1 borrower.


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
  passwords : VARCHAR(X)
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
	attachmentId: INT [PK],
	attachmentBlob: BLOB,
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
  userId : INT [FK to user.userId],
  month : DATE
)

Split (
  splitId : INT [PK],
  title : VARCHAR(X),
  timestamp : DATETIME,
  amount : REAL,
  note : VARCHAR(X),
  lenderId : INT [FK to user.userId]
)


Borrows (
  borrowerId : INT [FK to user.userId],
  splitId : INT [FK to Split.splitId],
  amount : REAL,
  isPaid : BOOL
  (borrowerId, splitId) : [PK]
)
```

