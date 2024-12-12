CREATE TABLE IF NOT EXISTS PUBLISHER
(
    Publisher_name    VARCHAR(50)    NOT NULL,
    Phone             VARCHAR(12),
    Address           VARCHAR(50)    NOT NULL,
    PRIMARY KEY(Publisher_name, Address)
);



CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH
(
    Branch_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    Branch_name      VARCHAR(50)     NOT NULL,
    Branch_address   VARCHAR(50)     NOT NULL
);



CREATE TABLE IF NOT EXISTS BORROWER
(
    Card_No INTEGER PRIMARY KEY AUTOINCREMENT,
    Name                   VARCHAR(50)   NOT NULL,
    Address                VARCHAR(50)   NOT NULL,
    Phone                  VARCHAR(12)
);








CREATE TABLE IF NOT EXISTS BOOK
(
    Book_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    Title           VARCHAR(50)  NOT NULL,
    Publisher_name  VARCHAR(50)  NOT NULL,
    FOREIGN KEY(Publisher_name) REFERENCES PUBLISHER(Publisher_name)        
);




CREATE TABLE IF NOT EXISTS BOOK_AUTHORS
(
    Book_id         INT          NOT NULL,
    Author_name     VARCHAR(30)  NOT NULL,
    PRIMARY KEY(Author_name, Book_id),
    FOREIGN Key(Book_id) REFERENCES BOOK(Book_id)
);




CREATE TABLE IF NOT EXISTS BOOK_COPIES
(
    Book_id         INT         NOT NULL,
    Branch_id       INT         NOT NULL,
    No_Of_Copies    INT,
    PRIMARY KEY( Book_id, Branch_id),
    FOREIGN KEY(Branch_id) References  LIBRARY_BRANCH(Branch_id),
    FOREIGN KEY(Book_id) References BOOK(Book_id)
);




CREATE TABLE IF NOT EXISTS BOOK_LOANS
(
    Book_id         INT     NOT NULL,
    Branch_id       INT     NOT NULL,
    Card_no         INT,
    Date_out        TEXT    NOT NULL,
    Due_date        TEXT    NOT NULL,
    Returned_date   TEXT    NOT NULL,




    PRIMARY KEY(Book_id, Branch_id, Card_no),
    FOREIGN KEY(Branch_id) REFERENCES  LIBRARY_BRANCH(Branch_id),
    FOREIGN KEY(Card_no)   REFERENCES  BORROWER(Card_no),
    FOREIGN KEY(Book_id)   REFERENCES BOOK(Book_id)
);




 
 






 CREATE TABLE if not exists BOOK_LOANS (
    Book_Id     int NOT NULL,
    Branch_Id   int NOT NULL,
    Card_No int,
    Date_Out    TEXT,
    Due_Date    TEXT,
    Returned_Date   TEXT,


    Primary Key( Book_Id),
    Foreign Key(Branch_Id) References  Library_Branch(Branch_Id),
Foreign Key(Card_No) References  BORROWER(Card_No),
Foreign Key(Book_Id) References BOOK(Book_Id)
);




 CREATE TABLE if not exists BOOK_COPIES (
    Book_Id     int NOT NULL,
    Branch_Id   int NOT NULL,
    No_Of_Copies    int,
    Primary Key( Book_Id, Branch_Id),
    Foreign Key(Branch_Id) References  Library_Branch(Branch_Id),
    Foreign Key(Book_Id) References BOOK(Book_Id)
);


 CREATE TABLE if not exists BOOK_AUTHORS (
    Book_Id     int NOT NULL,
    Author_Name     varchar(30),


    Primary Key(Author_Name, Book_Id),
    Foreign Key(Book_Id) References BOOK(Book_Id)
);









