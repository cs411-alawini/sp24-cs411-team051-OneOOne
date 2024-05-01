DELIMITER //

CREATE PROCEDURE InsertMonthlyBudget(
    IN p_description TEXT,
    IN p_amount DECIMAL(10, 2),
    IN p_categoryId INT,
    IN p_userId INT,
    IN p_monthNumber INT,
    IN p_yearNumber INT
)
BEGIN
    DECLARE p_monthDate DATE;
    
    -- Construct the date using the month and year numbers
    SET p_monthDate = STR_TO_DATE(CONCAT(p_yearNumber, '-', p_monthNumber, '-01'), '%Y-%m-%d');
    
    -- Insert into MonthlyCategoryBudget
    INSERT INTO MonthlyCategoryBudget (description, amount, categoryId, userId, month)
    VALUES (p_description, p_amount, p_categoryId, p_userId, p_monthDate);
END//

DELIMITER ;


1. create a transaction for user


ALTER TABLE Transaction ADD CONSTRAINT chk_transaction_type CHECK (type IN ('Income', 'Expense'));
ALTER TABLE Transaction
    -> ADD CONSTRAINT chk_payment_method
    -> CHECK (paymentMethod IN ('Cash', 'Credit Card', 'Debit Card', 'Zelle'));



DELIMITER //

CREATE PROCEDURE getUserById(IN user_id INT)
BEGIN
    SELECT * FROM User WHERE userId = user_id;
END//

DELIMITER ;


SHOW CREATE PROCEDURE getUserById;

CALL getUserById(123);


DELIMITER //

CREATE TRIGGER update_borrows_trigger
AFTER UPDATE ON Borrows
FOR EACH ROW
BEGIN
    -- Declare variables
    DECLARE lender_name VARCHAR(255);
    
    -- Check if isPaid is updated from false to true
    IF OLD.isPaid = 0 AND NEW.isPaid = 1 THEN
        -- Select lender name based on lenderId
        SELECT firstName INTO lender_name
        FROM User
        WHERE userId = (SELECT lenderId FROM Split WHERE splitId = NEW.splitId);
        
        -- Insert transaction record
        INSERT INTO Transaction (title, amount, type, userId)
        VALUES (CONCAT("Payment for borrowed amount from ", lender_name), NEW.Amount, 'Expense', NEW.borrowerId);
    END IF;
END;
//

DELIMITER ;


SELECT firstName 
        FROM User
        WHERE userId = (SELECT lenderId FROM Split WHERE splitId =  1);


INSERT INTO Transaction (title, amount, type, userId)
        VALUES (CONCAT("Payment for borrowed amount from ","dsd"), 1, 'Expense', 1);



DELIMITER //

CREATE PROCEDURE GetUserInfo(IN userName VARCHAR(255))
BEGIN
    -- First query: Select user information from the User table
    SELECT 
        userId,
        firstName,
        lastName,
        email
    FROM 
        User
    WHERE 
        userName = userName;

    -- Second query: Select credentials information for the user
    SELECT 
        email,
        password
    FROM 
        Credentials
    WHERE 
        email = (SELECT email FROM User WHERE userName = userName);
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE GetMonthlyExpensePerCategorySorted(IN userId INT)
BEGIN
    SELECT 
        YEAR(t.timestamp) AS year,
        MONTH(t.timestamp) AS month,
        c.categoryId,
        c.categoryName,
        SUM(t.amount) AS monthly_expense
        coalesce(c.parentCategoryId, c.categoryId) as parentId
    FROM 
        Transaction t
    JOIN 
        Category c ON t.categoryId = c.categoryId
    WHERE 
        t.userId = 1
    GROUP BY 
        YEAR(t.timestamp),
        MONTH(t.timestamp),
        c.categoryId,
        c.categoryName
    ORDER BY 
        year DESC, 
        month DESC;
END //

DELIMITER ;


select coalesce(parentCategoryId, categoryId) as id from Category limit 15;



with categoryExpense as (with temp as (SELECT 
        t.timestamp,
        c.categoryId,
        c.parentCategoryId,
        c.categoryName,
        t.amount
        -- coalesce(parentCategoryId, categoryId) as parentId
        -- SELECT *
    FROM 
        Transaction t
    JOIN 
        Category c ON t.categoryId = c.categoryId
    WHERE 
        t.userId = 111)

        select coalesce(temp.parentCategoryId, temp.categoryId) as id,
            amount,
            timestamp, 
            temp.categoryName
            from temp join Category on temp.id = Category.categoryId;)

