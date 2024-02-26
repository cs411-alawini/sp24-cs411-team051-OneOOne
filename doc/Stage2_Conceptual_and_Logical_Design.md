## Conceptual and Logical Design

### UML Diagram
![expense_manager_UML](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/42375666/4e3c8435-53e0-4bf5-b42c-eeaaac67c2af)

### Normalization
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
