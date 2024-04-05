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
The functional dependencies are -
1. TransactionId -> Title, Timestamp, Amount,  PaymentMethod, Comment, Type
2. CategoryId, SubcategoryId -> Name
3. BudgetId -> Description, Amount
4. ReminderId -> Name, Recurrence, Description
(Note: FD's for two attribute relations are not shown here)

A relation is in 3NF if at least one of the following conditions holds in every non-trivial function dependency X –> Y -
* X is a super key.
* Y is a prime attribute (each element of Y is part of some candidate key).

A relation is in BCNF if -
* The relation is in 3NF.
* X should be a superkey for every functional dependency X−>Y in a given relation. 

Every LHS in the FD’s is the primary key of the relation ( Subcategory is a weak entity dependent on Category so its primary key is [CategoryId, SubcategoryId]) and two attribute relations are always in BCNF so the schema is in BCNF form.


### 5 Relational Schema 
```
Transaction(
	Id: INT [PK],
	Title: VARCHAR(X),
	Amount: REAL,
	Timestamp: DATETIME,
	Note: VARCHAR(X),
	PaymentMethod: [‘Cash, ’Credit Card’, ‘Debit Card’, ‘Zelle’],
	Type: [‘Income’, ‘Expense’],
	CategoryId: INT [FK to Category.CategoryId],
	SubCategoryId: INT [FK to SubCategory.SubCategoryId],
	AttachmentId: INT [FK to Attachment.AttachmentId]
)

Category(
	CategoryId: INT [PK],
	Name: VARCHAR(X)
)

CategoryBudget(
	BudgetId: INT [PK],
	Description: VARCHAR(X),
	Amount: DECIMAL,
	CategoryId: INT [FK to Category.CategoryId]
)

Attachment(
	AttachmentId: INT [PK],
	Blob: BLOB
)

SubCategory(
	SubCategoryId: INT [PK],
	Name: VARCHAR(X)
)


BillReminder(
	ReminderId: INT [PK],
	Name: VARCHAR(X),
	Recurrence: ['Monthly', 'Bi-weekly', 'Weekly'],
	Description: VARCHAR(X)
)
```

