# SpendSmart
## Description 
Our project aims to develop a comprehensive expense manager application designed to simplify and streamline personal finance management for users. With a user-friendly interface and robust features, our application will empower individuals to track their expenses, set budgets, and achieve their financial goals with ease. Users will have the flexibility to manually input their expenses, ensuring accurate and up-to-date financial data at their fingertips.

Furthermore, our expense manager application will offer advanced functionalities such as customizable expense categories, real-time currency conversion, and expense analysis to provide users with valuable insights into their spending habits and financial trends. The application will also provide a budget functionality in order to motivate the user to limit their spending within the provided amount. With features like bill reminders (eg Pay rent on 1st of each month) our application will serve as a trusted companion in navigating the complexities of personal finance management efficiently.

## Creative component
Analytics are important in expense manager applications as they provide users with insights of their spending habits and trends. By analyzing the data, users can identify areas where they may be overspending, track progress towards their financial goals, and make informed decisions about budgeting and saving in the future. Analytics also help users understand how their expenses fluctuate over time (week, month etc) or categories (utilities, eating out etc), allowing them to adjust their financial habits accordingly.

Implementing analytics in our application can be challenging due to several reasons:
1. Complexity : Financial data can be complex and diverse, including various types of transactions, currencies, and categories. Aggregating and processing this data accurately would required meticulously written algorithms with lots of testing. This would require to use SQL principles like procedures, transactions, constraints, and triggers.
2. User Experience: Analytics features must be presented in a user-friendly and easy to understand manner to be effective. Designing informative visualizations and reports that are easy to understand and navigate can be challenging.
3. Optimization: Analyzing large volumes of data efficiently without compromising application performance requires optimization techniques and scalable infrastructure.

Nevertheless, adding analytics capabilities to expense manager application is crucial to giving customers the useful information they need to improve their financial well-being and achieve their goals.

## Usefulness
This expense manager application is highly beneficial as it provides users with a user-friendly platform to track their expenses, set budgets, and gain insights into their spending habits. With features like expense categorization, real-time currency conversion, and expense analysis, users can efficiently manage their finances and make informed decisions. The application also offers convenience through bill reminders, ensuring users stay organized and on top of their financial commitments. Overall, this application empowers individuals to take control of their finances, promoting financial awareness and responsible money management.

## Realness
We are going to use the following realworld dataset with some augmentation to test our application - 
1. https://www.kaggle.com/datasets/tharunprabu/my-expenses-data
    a. Format - csv
    b. Cardinality - 278
    c. Data - Date, Account	Category, Subcategory, Note, Income/Expense, Amount, Currency, Balance
2. @adityabandal's expense data from Oct 2021 to Oct 2023
    a. Format - csv
    b. Cardinality - 295
    c. Data - Date,	Category, Subcategory, Comment, Debit/Credit, Amount, Currency, Balance    
CSV files are present in doc/Datasets folder

## Functionality
Our expense manager application offers a comprehensive suite of features to empower users in managing their finances efficiently. Users can seamlessly add expenses and income manually, specifying categories and subcategories for accurate tracking. Additionally, our application provides flexibility by allowing users to view and edit categories and subcategories according to their preferences, ensuring personalized financial management.

Furthermore, users can leverage powerful analytics tools to gain insights into their spending habits. By analyzing expenses based on categories, subcategories, weeks, and months, users can identify trends and areas for improvement. Moreover, our application enables users to set monthly budget goals, with built-in alerts to notify users if they exceed their budget limits. Additionally, users can schedule reminders for bill payments, facilitating timely payments and reducing the risk of late fees. With these robust features, our expense manager application serves as a reliable companion in achieving financial stability and success.

## Low fidelity UI mockup

### Home Page
![1](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/07430d36-2c59-4514-951f-f10c5924cc00)

### Add Transaction
![2](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/77af91e5-86c3-4959-8fed-ef43fc6c517d)

### Insight Page
![3](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/95d71a46-4517-4c6a-ab7a-f4bfe516a8b1)

### Transaction History
![4](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/45b02061-894a-4db1-9848-abfe7266d308)

### Track Budget
![Home Page](https://github.com/cs411-alawini/sp24-cs411-team051-OneOOne/assets/68540700/cc6498f0-0b50-46f7-bd0f-bdcc683928cd)



## Work distribution
1. Aaditya Bodke (Frontend) - Data modelling, UI Design, template creation, reminders and budget
2. Prathamesh Bhosale (Frontend) - Data modelling, Data insertion, Analytics and API developmemt
3. Sasi Pavan Chowdary Surapaneni (Backend) - Data modelling,  triggers and prcedures creation
4. Aditya Bandal (Backend) - Data modelling, Tables creation, indexing, optimization

