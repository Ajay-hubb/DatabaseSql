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


CREATE VIEW BookLoanInfo AS
 SELECT BO.Card_No, BO.Name AS Borrower_name, BL.Date_out, BL.Due_Date,
 BL.Returned_Date, B.Title AS Book_title,
 (CASE
 WHEN (BL.Returned_date = 'NULL' OR BL.Returned_date IS NULL) THEN
 julianday(Date('now'))- julianday(Date_out)
 WHEN Returned_date > Date_out
 THEN julianday(BL.Returned_date)- julianday(BL.Date_out)
 ELSE
 0
 END
 ) AS TotalDays,
 (CASE
 WHEN (BL.Returned_date = 'NULL' OR BL.Returned_date IS NULL) AND
 (julianday(Date('now')) > julianday(BL.Due_date)) THEN
 (julianday(Date('now'))- julianday(BL.Due_date))
 WHEN
 julianday(BL.returned_date) > julianday(BL.due_date) THEN
 julianday(BL.returned_date)- julianday(BL.Due_date)
 ELSE
 0
 END) AS Late_days,
 BL.Branch_id,
 (
 CASE
WHEN (BL.Returned_date = 'NULL' OR BL.Returned_date IS NULL) AND
 (julianday(Date('now')) > julianday(BL.Due_date)) THEN
 (julianday(Date('now'))- julianday(BL.Due_date)) * LB.Late_fee
 WHEN
 julianday(BL.Returned_date) > julianday(BL.Due_date) THEN
 (julianday(BL.Returned_date)- julianday(BL.Due_date)) *
 LB.Late_fee
 ELSE
 0
 END) AS LateFeeBalance
 FROM Library_Branch LB JOIN Book_Loans BL ON LB.Branch_id =
 BL.Branch_id
 JOIN Borrower BO ON BL.Card_no = BO.Card_no JOIN Book B ON BL.Book_id =
 B.Book_id;
