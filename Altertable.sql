ALTER TABLE Book_Loans
ADD Late INT;
ALTER Table Library_Branch
Add Late_Fee Int;




UPDATE Book_Loans
SET Late = 
    CASE
    WHEN julianday(returned_date) > julianday(due_date) THEN 1
    ELSE 0
END;


Update Library_branch
Set Late_Fee=2;
