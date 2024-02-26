## Conceptual and Logical Design

### 1 UML Diagram
![expense_manager_UML](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/4e3c8435-53e0-4bf5-b42c-eeaaac67c2af)

### 2 Entities

#### 2.1 Transactions
  This is the central entity that represents all the expenses and income with additional information regarding the payment method and type of expense.
  
  Assumptions:
  - The given attributes are assumed to be limited to the following values
      - PaymentMethod: [‘Cash, ’Credit Card’, ‘Debit Card’, ‘Zelle’]
      - Type: [‘Income’, ‘Expense’]
  - A subcategory can be added to a transaction if and only its parent category is present in the category field.






#### 2.2 Categories
This entity represents the categories that a transaction belongs to.

  ##### Assumptions:
  - A transaction can have one category at max.


#### 2.3 Subcategory
This entity represents the subcategories for the transactions at first glance it might seem that it could be merged with the categories entity but the reason we promoted it to be a separate entity is due to the fact that some of the subcategories are shared by multiple categories. For example, the subcategory "Groceries" can be present in both Categories “Household” and “Travel”.

  ##### Assumptions:
  - At most one subcategory can be added to a transaction.

#### 2.4 Attachment
The Attachment entity represents the receipts or any other transaction-related documents in image or PDF format.

  ##### Assumptions:
  - There could be 0 or 1 attachment for a given transaction.

#### 2.5 CategoryBudget
This represents a category-wise budget recurring every month.

  ##### Assumptions:
  - The budget for each category remains constant every month unless edited by the user. 

#### 2.6 BillReminders
The reminders are stored in this entity with the recurrence of the reminders handled using a cron expression.

  ##### Assumptions:
  - The attribute recurrence is assumed to contain one of the following values:
    - Monthly
    - Bi-weekly
    - Weekly
	

### 3 Relations

- A Transaction might have 0 or 1 attachment associated with it.
- A Transaction can also have 0 or 1 category.
- A Transaction can have 0 or 1 subcategory provided that the category field is populated.
- A Category can have 0 or n different subcategories associated with it.
- A Category can have 0 or 1 Budget associated with it.



### 4 Normalization
The functional dependencies are -
1. TransactionId -> Title, Timestamp, Amount,  PaymentMethod, Comment, Type
2. CategoryId, SubcategoryId -> Name
3. BudgetId -> Description, Amount
4. ReminderId -> Name, Recurrence, Description

A relation is in 3NF if at least one of the following conditions holds in every non-trivial function dependency X –> Y -
* X is a super key.
* Y is a prime attribute (each element of Y is part of some candidate key).

A relation is in BCNF if -
* The relation is in 3NF.
* X should be a superkey for every functional dependency X−>Y in a given relation. 

Every LHS in the FD’s is the primary key of the relation ( Subcategory is a weak entity dependent on Category so its primary key is [CategoryId, SubcategoryId]) and two attribute relations are always in BCNF so the schema is in BCNF form.


### 5 Relational Schema 
Transaction(Id: INT [PK],
Title: VARCHAR(X),
Amount: REAL,
Timestamp: DATETIME,
Note: VARCHAR(X),
PaymentMethod: VARCHAR(X),
Type: VARCHAR(X),
CategoryId: INT [FK to Category.CategoryId],
SubCategoryId: INT [FK to SubCategory.SubCategoryId],
AttachmentId: INT [FK to Attachment.AttachmentId])

Category(CategoryId: INT [PK], Name: VARCHAR(X))

CategoryBudget(BudgetId: INT [PK],
Description: VARCHAR(X),
Amount: DECIMAL,
CategoryId: INT [FK to Category.CategoryId])

Attachment(AttachmentId: INT [PK], Blob: BLOB)

SubCategory(SubCategoryId: INT [PK], Name: VARCHAR(X))


BillReminder(ReminderId: INT [PK],
Name: VARCHAR(X),
Recurrence: VARCHAR(X),
Description: VARCHAR(X))

