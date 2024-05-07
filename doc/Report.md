# Report


## Changes in Proposal

Initially, we planned to create an expense management app that allows the user to track their spending for a single user. However, later on, we upgraded it to support
multiple users and to allow users to split bills with other users.


## Usefullness of Application

We think that the application we developed is useful because of the features we included, such as expense tracking, categorizing expenses, budget setting, insightful
visual analytics, and bill splitting. These features make it easy to keep track of spending and budgeting. 


## Changes in Dataset

We added support for multiple users and bill-splitting features to our application, which required us to change the schema. We generated a realistic dataset because our
initial datasets did not have multiple users and bill-splitting data.


## Changes in ER diagram

We added 2 major entities to our ER diagram, namely Users and Splits and a relationship between them Borrows. This led to three new tables in our database. The rest of 
the ER diagram remained the same. The new entities and relationships allowed us to implement more features and perform complex queries and data analysis to improve user experience.


## Change in functionalities

We added support for multiple users to our application. Along with this we also added a bill-splitting feature. This allowed us to provide a more robust experience to users by 
providing all money-tracking features in a single application. We removed a feature of bill reminders, as we felt that the value it added was not worth the effort it needed to set 
up a batch job on the server. 


## Benefit of using advanced database programs in our application

1. We added all the logic for complex queries (like analytics and splits) and updated the data in stored procedures. The backend of the application just calls these stored procedures 
with parameters. This helps us to keep the functionalities modular and the backend clean. Also, if anything needs to be changed, we can just update the stored procedures,
without needing any code changes in our application.
2. Moreover, we also have added triggers to automatically update databases in some special cases instead of explicitly executing queries from the backend. This reduces the load on 
the backend and reduces access to the database.
3. The SQL transaction we have implemented helps us to keep the database consistent and provide correct data to our users.
We also have implemented attribute level check constraints to avoid any abnormal inserts in our database, ensuring consistent data to the users. 


## Technical challenges encountered

1. We did not find any appropriate dataset for our application which was sufficiently large. So, with TA’s approval, we generated realistic datasets. You can use python’s numpy, 
pandas library and random number generator to easily generate the data. But make sure that the generated data is realistic for eg. keeping bounds to personal expenses 
between 1 to 100 $ while generating expenses data. If you want to generate users, there are a lot of websites which can generate 1000s of random names. You can use these names 
to then generate usernames and email ids.
2. If the application makes multiple calls to the database for a single function, it slows down the application. So we should try to keep all the logic on the database and minimize
  calls to the database improving the performance of the application. In our experience stored procedure is a great way to achieve this level of abstraction.

## Other changes

No. All the changes are mentioned in the above sections.

## Future work

As part of future developments, we plan to include features such as adding friends to Split Bill, sending email reminders, and implementing an in-app payment method for settling 
debts with friends.

## Work division

- Aaditya Bodke  - Data modeling, UI Design, template creation, splits, and budget page logic.
- Prathamesh Bhosale -  Data modeling, Data insertion, Analytics and API development, implementing the budget page, registration page, and interactive plots in the analytics page for the application. 
- Aditya Bandal - Database schema, drawing ER diagram, generation of datasets using Python script, creating few stored procedures and triggers, implementing expenses and home page 
of the application, implementing user authentication.
- Sasi Pavan Chowdary Surapaneni - Data modeling, triggers and procedures creation

We have mentioned the broad division of the work above. However, each team member supported the other whenever others got stuck. Being roommates helped us review each 
others work easily and improve the quality of our work.






