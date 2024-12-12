from tkinter import *
from tkinter import ttk

import sqlite3
root = Tk()


root.title('Library Management System')
root.geometry("800x800")
#conn = sqlite3.connect('libraryproject.db')

# Uniformity Variables
button_color = "steel blue"
button_width = 20

# Funcions for buttons

# Function for implementing trigger for Query #1
def maketrigger():

    maketrigger_conn = sqlite3.connect('libraryproject.db')
    maketrigger_cur = maketrigger_conn.cursor()

    triggersql = '''
                CREATE TRIGGER IF NOT EXISTS UpdateBookCopiesOnLoan
                AFTER INSERT ON BOOK_LOANS
                FOR EACH ROW
                BEGIN
                    UPDATE BOOK_COPIES
                    SET No_Of_Copies = No_Of_Copies - 1
                WHERE Book_id = NEW.Book_id AND Branch_id = NEW.Branch_id;
                END;
                 '''
    try:
        maketrigger_cur.execute(triggersql)
        #print("Trigger Build")
    except sqlite3.Error as E:
        print("Trigger Build failed")
    finally:
        maketrigger_conn.close()

# Query 1
def checkout_book_window():

    window = Toplevel(root)
    window.geometry("800x800")
    window.title("Checkout Book")

    # Connecting to database
    checkout_conn = sqlite3.connect('libraryproject.db')
    checkout_cur = checkout_conn.cursor()
    maketrigger()
    #addbook_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide Book ID, BranchID, Card_no, Date_out, and Due_date to checkout ", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    b_id_label = Label(window, text="Book ID:")
    b_id_label.grid(row=1, column=0, padx=10, pady=10)

    br_id_label = Label(window, text="Branch ID:")
    br_id_label.grid(row=3, column=0, padx=10, pady=10)

    card_no_label = Label(window, text="Card_no")
    card_no_label.grid(row=5, column=0, padx=10, pady=10)

    dateout_label = Label(window, text="Date_out")
    dateout_label.grid(row=7, column=0, padx=10, pady=10)

    duedate_label = Label(window, text="Due_date")
    duedate_label.grid(row=9, column=0, padx=10, pady=10)


    # Adding the text fields
    b_id = Entry(window, width = 30)
    b_id.grid(row = 2, column = 0, padx = 20)

    br_id = Entry(window, width = 30)
    br_id.grid(row = 4, column =0)

    card_no = Entry(window, width = 30)
    card_no.grid(row = 6, column =0)
    
    date_out = Entry(window, width = 30)
    date_out.grid(row = 8, column =0)

    due_date = Entry(window, width = 30)
    due_date.grid(row = 10, column =0)

    # Function for executing the SQL query
    def add_new_borrower():
        
        bookid = b_id.get() or None
        branchid = br_id.get() or None
        cardno = card_no.get() or None
        dateout = date_out.get() or None
        duedate = due_date.get() or None
        idx = 13
        try:
            # Adding record to BORROWER
            checkout_cur.execute('''INSERT INTO BOOK_LOANS VALUES (?, ?, ?, ?, ?, ?, ?)''', (bookid, branchid, cardno, dateout, duedate, 'NULL', None)) # Think about adding INSERT OR IGNORE INTO
            checkout_cur.execute(''' SELECT * FROM BOOK_COPIES WHERE Book_id = ? AND Branch_id = ?''', (bookid, branchid,))

            rows = checkout_cur.fetchall()

            header = f"{'Branch ID':<10} {'Branch Name':<30} {'No Of Copies':<5}\n"
            header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
            header.grid(row=12, column=0, columnspan=2, pady=10)

            for row in rows:
                
                result_text = f"{row[0]:<5} {row[1]:<30} {row[2]:<5}"
                result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                idx += 1
            

            checkout_conn.commit()
            success_message = Label(window, text="Loan Added!", fg="green")
            success_message.grid(row=idx, column=0, pady=10)


        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = 12, column = 0, pady = 10)
        finally:
            checkout_conn.close()

    # Button for executing sql query
    submit_btn = Button(window, text="Add New Loan", command= add_new_borrower, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=11, column=0, pady=10)


# Query 2
def add_new_borrower_window():
    window = Toplevel(root)
    window.geometry("800x800")
    window.title("Add New Borrower")

    # Connecting to database
    addborrower_conn = sqlite3.connect('libraryproject.db')
    addborrower_cur = addborrower_conn.cursor()
    #addbook_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide Name, Address, Phone(Not necessary) to register", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    b_name_label = Label(window, text="Borrower Name:")
    b_name_label.grid(row=1, column=0, padx=10, pady=10)

    b_addr_label = Label(window, text="Borrower Address:")
    b_addr_label.grid(row=3, column=0, padx=10, pady=10)

    b_phone_label = Label(window, text="Borrower Phone")
    b_phone_label.grid(row=5, column=0, padx=10, pady=10)


    # Adding the text fields
    b_name = Entry(window, width = 30)
    b_name.grid(row = 2, column = 0, padx = 20)

    b_addr = Entry(window, width = 30)
    b_addr.grid(row = 4, column =0)

    b_phone = Entry(window, width = 30)
    b_phone.grid(row = 6, column =0)

    # Function for executing the SQL query
    def add_new_borrower():
        
        borrower_name = b_name.get() or None
        borrower_addr = b_addr.get() or None
        borrower_phone = b_phone.get() or None
        try:
            # Adding record to BORROWER
            addborrower_cur.execute("INSERT INTO BORROWER VALUES (?, ?, ?, ?)", (None, borrower_name, borrower_addr, borrower_phone)) # Think about adding INSERT OR IGNORE INTO
            Borrower_id = addborrower_cur.lastrowid

            header = "Your Library Card\n"
            header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
            header.grid(row=9, column=0, columnspan=2, pady=10)

            header = f"{'Borrower ID':<15} {'Name':<25} {'Address':<30} {'Phone':<15}\n"
            header_label = Label(window, text=header, font=("Courier", 10, "bold"), fg="black", anchor="w")
            header_label.grid(row=10, column=0, columnspan=2, pady=10)

            result_text = f"{Borrower_id:<15} {borrower_name:<25} {borrower_addr:<30} {borrower_phone:<15}"
            result_label = Label(window, text=result_text, font=("Courier", 10), anchor="w")
            result_label.grid(row=11, column=0, columnspan=2, pady=2, padx=10)

            addborrower_conn.commit()
            success_message = Label(window, text="Borrower Added Successfully!", fg="green")
            success_message.grid(row=12, column=0, pady=10)


        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = 8, column = 0, pady = 10)
        finally:
            addborrower_conn.close()

    # Button for executing sql query
    submit_btn = Button(window, text="Add New Borrower", command= add_new_borrower, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=7, column=0, pady=10)


# Query 3
def add_new_book_window():
    window = Toplevel(root)
    window.geometry("800x800")
    window.title("Add New Book")

    # Connecting to database
    addbook_conn = sqlite3.connect('libraryproject.db')
    addbook_cur = addbook_conn.cursor()
    #addbook_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide Publisher (already exists) and Author to add new book", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    p_name_label = Label(window, text="Publisher Name:")
    p_name_label.grid(row=1, column=0, padx=10, pady=10)

    a_name_label = Label(window, text="Author Name:")
    a_name_label.grid(row=3, column=0, padx=10, pady=10)

    b_name_label = Label(window, text="Book Title:")
    b_name_label.grid(row=5, column=0, padx=10, pady=10)


    # Adding the text fields
    p_name = Entry(window, width = 30)
    p_name.grid(row = 2, column = 0, padx = 20)

    a_name = Entry(window, width = 30)
    a_name.grid(row = 4, column =0)

    b_name = Entry(window, width = 30)
    b_name.grid(row = 6, column =0)

    # Function for executing the SQL query
    def add_new_book():
        
        publisher_name = p_name.get() or None
        author_name = a_name.get() or None
        book_title = b_name.get() or None
        try:
            # Adding record to BOOK
            addbook_cur.execute("INSERT INTO BOOK(Title, Publisher_name) VALUES (?, ?)", (book_title, publisher_name)) # Think about adding INSERT OR IGNORE INTO
            Book_id = addbook_cur.lastrowid
            # Updating BOOK_AUTHORS with the author
            addbook_cur.execute("INSERT INTO BOOK_AUTHORS(Book_id, Author_name) VALUES (?, ?)", (Book_id, author_name))
            # Storing the list of branch_id's in a list
            addbook_cur.execute("SELECT Branch_id FROM LIBRARY_BRANCH")
            rows = addbook_cur.fetchall()
            branch_ids = []
            for row in rows:
                branch_ids.append(row[0])
            for branch_id in branch_ids:
                addbook_cur.execute("INSERT INTO BOOK_COPIES VALUES (?, ?, ?)", (Book_id, branch_id, 5))
        
            addbook_conn.commit()
            success_message = Label(window, text="Book Added Successfully!", fg="green")
            success_message.grid(row=8, column=0, pady=10)
        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = 8, column = 0, pady = 10)
        finally:
            addbook_conn.close()

    # Button for executing sql query
    submit_btn = Button(window, text="Add New Book", command= add_new_book, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=7, column=0, pady=10)

# Query 4

def list_loaned_window():
    window = Toplevel(root)
    window.geometry("800x800")
    window.title("List Loaned Copies Per Branch")
    # Connecting to database
    listloaned_conn = sqlite3.connect('libraryproject.db')
    listloaned_cur = listloaned_conn.cursor()
    #listloaned_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide Book Title to get listed all loaned copies per branch", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    b_name_label = Label(window, text="Book Title:")
    b_name_label.grid(row=1, column=0, padx=10, pady=10)

    # Adding the text fields
    b_name = Entry(window, width = 30)
    b_name.grid(row = 2, column = 0, padx = 20)

    def list_loaned():

        book_title = b_name.get() or None
        idx = 5
        try:
            # Adding record to BOOK
            listloaned_cur.execute('''
                                           SELECT LB.Branch_id, LB.Branch_name, COUNT(*) AS Copies_loaned
                                           FROM BOOK_LOANS BL JOIN LIBRARY_BRANCH LB ON BL.Branch_id = LB.Branch_id 
                                           JOIN BOOK B ON BL.Book_id = B.Book_id
                                           WHERE B.Title = ?
                                           GROUP BY LB.Branch_id, LB.Branch_name''', (book_title,)) 
            
            rows = listloaned_cur.fetchall()

            header = f"{'Branch ID':<10} {'Branch Name':<30} {'Copies Loaned':<5}\n"
            header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
            header.grid(row=4, column=0, columnspan=2, pady=10)

            for row in rows:
                
                result_text = f"{row[0]:<5} {row[1]:<30} {row[2]:<5}"
                result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                idx += 1
      
            #listloaned_conn.commit()
            success_message = Label(window, text="List Retrieved Successfully!", fg="green")
            success_message.grid(row=idx, column=0, pady=10)
        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = idx, column = 0, pady = 10)
        finally:
            listloaned_conn.close()

    # Button for executing sql query
    submit_btn = Button(window, text="View List", command= list_loaned, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=3, column=0, pady=10)

#query 5
def OpenNewWindowLateBooks():
    newWindow = Toplevel(root)
    newWindow.title("Late Books")
    newWindow.geometry("800x800")




    late_conn = sqlite3.connect('libraryproject.db')
    late_cur = late_conn.cursor()




    start_date_label = Label(newWindow, text="Start Date (YYYY-MM-DD):")
    start_date_label.grid(row=0, column=0, padx=10, pady=10)
    start_date_Entry = Entry(newWindow)
    start_date_Entry.grid(row=0, column=1, padx=10, pady=10)




    end_date_label = Label(newWindow, text="End Date (YYYY-MM-DD):")
    end_date_label.grid(row=1, column=0, padx=10, pady=10)
    end_date_Entry = Entry(newWindow)
    end_date_Entry.grid(row=1, column=1, padx=10, pady=10)




    columns = ("Book_id", "Branch_id", "Card_no", "Date_out", "Due_date", "Returned_date", "Days_Late")
    tree = ttk.Treeview(newWindow, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Adjust width as needed
    tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")




    scrollbar = Scrollbar(newWindow, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=3, column=2, sticky="ns")




    def find_late():
        for row in tree.get_children():
            tree.delete(row)




        start_date = start_date_Entry.get()
        end_date = end_date_Entry.get()




        late_cur.execute(
            """
            SELECT Book_id, Branch_id, Card_no, Date_out, Due_date, Returned_date,
                   (julianday(Returned_date) - julianday(Due_date)) AS Days_Late
            FROM BOOK_LOANS
            WHERE Due_date BETWEEN ? AND ? AND Returned_date > Due_date
            ORDER BY Days_Late DESC
            """,
            (start_date, end_date),
        )




        records = late_cur.fetchall()
        for record in records:
            tree.insert("", "end", values=record)




    find_late_btn = Button(newWindow, text="Find Late Returns", command=find_late, bg=button_color, fg="white", width=button_width)
    find_late_btn.grid(row=2, column=0, pady=10)


    newWindow.grid_rowconfigure(3, weight=1)
    newWindow.grid_columnconfigure(1, weight=1)

# Query 6a
def list_latefee_window():

    window = Toplevel(root)
    window.geometry("1000x1000")
    window.title("List Late Fee for Borrower(s)")
    # Connecting to database
    listlatefee_conn = sqlite3.connect('libraryproject.db')
    listlatefee_cur = listlatefee_conn.cursor()
    #listloaned_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide borrower id, name, or part-name to get late fee for borrower or leave it blank to see latefee for all borrowers ", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    b_id_label = Label(window, text="Borrower ID [Card_on] (Blank Allowed)")
    b_id_label.grid(row=1, column=0, padx=10, pady=10)

    b_name_label = Label(window, text="Borrower Name or Part-name (Blank Allowed)")
    b_name_label.grid(row=3, column=0, padx=10, pady=10)

    # Adding the text fields
    b_id = Entry(window, width = 30)
    b_id.grid(row = 2, column = 0, padx = 20)

    b_name = Entry(window, width = 30)
    b_name.grid(row = 4, column = 0, padx = 20)

    def list_latefee():

        borrower_id = b_id.get() or None
        borrower_name = b_name.get() or None
        
        idx = 7
        try:
            
            if borrower_id == None and borrower_name == None:
                listlatefee_cur.execute('''
                                        SELECT Card_no as Borrower_ID, Borrower_name, SUM(LateFeeBalance) as LateFeeBalance
                                        FROM BookLoanInfo
                                        GROUP BY  Card_no, Borrower_name
                                        ORDER BY LateFeeBalance DESC''')

                rows = listlatefee_cur.fetchall()

                header = f"{'Borrower ID':<10} {'Borrower Name':<30} {'LateFeeBalance':<10}\n"
                header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                header.grid(row=6, column=0, columnspan=2, pady=10)

                for row in rows:
                    
                    formatted_balance = f"${float(row[2]):,.2f}"
                    result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                    result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                    result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                    idx += 1

            elif borrower_id != None and borrower_name != None:
                idx = 7
                borrower_name_like = f"%{borrower_name}%"
                listlatefee_cur.execute('''
                                        SELECT Card_no as Borrower_ID, Borrower_name, SUM(LateFeeBalance) as LateFeeBalance
                                        FROM BookLoanInfo
                                        WHERE Card_no = ? AND Borrower_name LIKE ?
                                        GROUP BY  Card_no, Borrower_name
                                        ORDER BY LateFeeBalance DESC
                                        ''', (borrower_id, borrower_name_like))
                
                rows = listlatefee_cur.fetchall()

                header = f"{'Borrower ID':<10} {'Borrower Name':<30} {'LateFeeBalance':<10}\n"
                header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                header.grid(row=6, column=0, columnspan=2, pady=10)

                for row in rows:
                    
                    formatted_balance = f"${float(row[2]):,.2f}"
                    result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                    result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                    result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                    idx += 1
            
            elif borrower_id != None and borrower_name == None:
                idx = 7
                listlatefee_cur.execute('''
                                        SELECT Card_no as Borrower_ID, Borrower_name, SUM(LateFeeBalance) as LateFeeBalance
                                        FROM BookLoanInfo
                                        WHERE Card_no = ?
                                        GROUP BY  Card_no, Borrower_name
                                        ORDER BY LateFeeBalance DESC;
                                        ''', (borrower_id,))
                
                rows = listlatefee_cur.fetchall()

                header = f"{'Borrower ID':<10} {'Borrower Name':<30} {'LateFeeBalance':<10}\n"
                header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                header.grid(row=6, column=0, columnspan=2, pady=10)

                for row in rows:
                    
                    formatted_balance = f"${float(row[2]):,.2f}"
                    result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                    result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                    result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                    idx += 1
                
            elif borrower_id == None and borrower_name != None:

                idx = 7
                borrower_name_like = f"%{borrower_name}%"
                listlatefee_cur.execute('''
                                        SELECT Card_no as Borrower_ID, Borrower_name, SUM(LateFeeBalance) as LateFeeBalance
                                        FROM BookLoanInfo
                                        WHERE Borrower_name LIKE ?
                                        GROUP BY  Card_no, Borrower_name
                                        ORDER BY LateFeeBalance DESC;
                                        ''', (borrower_name_like,))
                
                rows = listlatefee_cur.fetchall()

                header = f"{'Borrower ID':<10} {'Borrower Name':<30} {'LateFeeBalance':<10}\n"
                header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                header.grid(row=6, column=0, columnspan=2, pady=10)

                for row in rows:
                    
                    formatted_balance = f"${float(row[2]):,.2f}"
                    result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                    result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                    result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                    idx += 1
            
            

      
            #listloaned_conn.commit()
            success_message = Label(window, text="List Retrieved Successfully!", fg="green")
            success_message.grid(row=idx, column=0, pady=10)

                
        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = idx, column = 0, pady = 10)
        finally:
            listlatefee_conn.close()
    
    # Button for executing sql query
    submit_btn = Button(window, text="View List", command= list_latefee, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=5, column=0, pady=10)

# Query 6b
def list_bookinfo_window():

    window = Toplevel(root)
    window.geometry("1000x1000")
    window.title("List Book Info for Borrower(s)")
    # Connecting to database
    listbookinfo_conn = sqlite3.connect('libraryproject.db')
    listbookinfo_cur = listbookinfo_conn.cursor()
    #listloaned_conn.execute("PRAGMA foreign_keys = ON")
    # Message of the query's purpose
    label = Label(window, text="Provide Borrower ID (necessary) and any of book id, book title or part-title", justify="left")
    label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Adding labels
    b_id_label = Label(window, text="Borrower ID [Card_on] (Necessary)")
    b_id_label.grid(row=1, column=0, padx=10, pady=10)

    bok_id_label = Label(window, text="Book ID (Blank Allowed)")
    bok_id_label.grid(row=3, column=0, padx=10, pady=10)

    b_title_label = Label(window, text="Book Title (Blank Allowed)")
    b_title_label.grid(row=5, column=0, padx=10, pady=10)

    # Adding the text fields
    b_id = Entry(window, width = 30)
    b_id.grid(row = 2, column = 0, padx = 20)

    bok_id = Entry(window, width = 30)
    bok_id.grid(row = 4, column = 0, padx = 20)

    b_title = Entry(window, width = 30)
    b_title.grid(row = 6, column = 0, padx = 20)

    def list_bookinfo():

        borrower_id = b_id.get() or None
        book_id = bok_id.get() or None
        book_title = b_title.get() or None
        idx = 9
        try:
            
            if borrower_id != None:
                

                if book_id == None and book_title == None:
                    listbookinfo_cur.execute('''
                                            SELECT B.Book_id, BLI.Book_title, BLI.LateFeeBalance 
                                            FROM BookLoanInfo BLI 
                                            JOIN Book_Loans BL ON BLI.Card_No = BL.Card_no 
                                            JOIN Book B ON BL.Book_id = B.Book_id
                                            WHERE BLI.Card_no = ?
                                            ORDER BY BLI.LateFeeBalance DESC''', (borrower_id,))

                    rows = listbookinfo_cur.fetchall()

                    header = f"{'Book ID':<10} {'Book Title':<30} {'LateFeeBalance':<10}\n"
                    header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                    header.grid(row=8, column=0, columnspan=2, pady=10)

                    for row in rows:
                    
                        formatted_balance = f"${float(row[2]):,.2f}"
                        result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                        result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                        result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                        idx += 1

                elif book_id != None and book_title != None:
                    idx = 9
                    book_title_like = f"%{book_title}%"
                    listbookinfo_cur.execute('''
                                            SELECT B.Book_id, BLI.Book_title, BLI.LateFeeBalance 
                                            FROM BookLoanInfo BLI 
                                            JOIN Book_Loans BL ON BLI.Card_No = BL.Card_no 
                                            JOIN Book B ON BL.Book_id = B.Book_id
                                            WHERE BLI.Card_no = ? AND B.Book_id = ? AND BLI.Book_title LIKE ?
                                            ORDER BY BLI.LateFeeBalance DESC
                                            ''', (borrower_id, book_id, book_title_like))
                
                    rows = listbookinfo_cur.fetchall()

                    header = f"{'Book ID':<10} {'Book Title':<30} {'LateFeeBalance':<10}\n"
                    header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                    header.grid(row=6, column=0, columnspan=2, pady=10)

                    for row in rows:
                    
                        formatted_balance = f"${float(row[2]):,.2f}"
                        result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                        result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                        result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                        idx += 1
            
                elif book_id != None and book_title == None:
                    idx = 9
                    listbookinfo_cur.execute('''
                                            SELECT B.Book_id, BLI.Book_title, BLI.LateFeeBalance 
                                            FROM BookLoanInfo BLI 
                                            JOIN Book_Loans BL ON BLI.Card_No = BL.Card_no 
                                            JOIN Book B ON BL.Book_id = B.Book_id
                                            WHERE BLI.Card_no = ? AND B.Book_id = ?
                                            ORDER BY BLI.LateFeeBalance DESC
                                            ''', (borrower_id, book_id,))
                
                    rows = listbookinfo_cur.fetchall()

                    header = f"{'Book ID':<10} {'Bok Title':<30} {'LateFeeBalance':<10}\n"
                    header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                    header.grid(row=6, column=0, columnspan=2, pady=10)

                    for row in rows:
                    
                        formatted_balance = f"${float(row[2]):,.2f}"
                        result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                        result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                        result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                        idx += 1
                
                elif book_id == None and book_title != None:

                    idx = 9
                    book_title_like = f"%{book_title}%"
                    listbookinfo_cur.execute('''
                                            SELECT B.Book_id, BLI.Book_title, BLI.LateFeeBalance 
                                            FROM BookLoanInfo BLI 
                                            JOIN Book_Loans BL ON BLI.Card_No = BL.Card_no 
                                            JOIN Book B ON BL.Book_id = B.Book_id
                                            WHERE BLI.Card_no = ? AND BLI.Book_title LIKE ?
                                            ORDER BY BLI.LateFeeBalance DESC
                                            ''', (borrower_id, book_title_like,))
                
                    rows = listbookinfo_cur.fetchall()

                    header = f"{'Book ID':<10} {'Book Title':<30} {'LateFeeBalance':<10}\n"
                    header = Label(window, text = header, font=("Courier", 10, "bold"), fg = "black")
                    header.grid(row=6, column=0, columnspan=2, pady=10)

                    for row in rows:
                    
                        formatted_balance = f"${float(row[2]):,.2f}"
                        result_text = f"{row[0]:<10} {row[1]:<30} {formatted_balance:<10}"
                        result = Label(window, text = result_text, font=("Courier", 10), anchor="w")
                        result.grid(row=idx, column=0, columnspan=2, pady=2, padx=10)
                        idx += 1
                
                #listloaned_conn.commit()
                success_message = Label(window, text="List Retrieved Successfully!", fg="green")
                success_message.grid(row=idx, column=0, pady=10)

            else:
                fail_message = Label(window, text="Borrower ID is required", fg="red")
                fail_message.grid(row=8, column=0, pady=10)
            

                
        except sqlite3.Error as e:
            message = Label(window, text = f"Error: {e}", fg = "red")
            message.grid(row = idx, column = 0, pady = 10)
        finally:
            listbookinfo_conn.close()
    
    # Button for executing sql query
    submit_btn = Button(window, text="View List", command= list_bookinfo, bg=button_color, fg="white", width=button_width)
    submit_btn.grid(row=7, column=0, pady=10)










def submit():
    print("Button clicked")

#create buttons to access db

Label(root).grid(row=0, column=0, pady=50) 

check_out_btn = Button(root, text="Check Out Book", command = checkout_book_window, bg=button_color, fg="white", width=button_width)
check_out_btn.grid(row=1, column=0, padx = 300, pady=10)

add_borrower_btn = Button(root, text="Add New Borrower", command=add_new_borrower_window, bg=button_color, fg="white", width=button_width)
add_borrower_btn.grid(row=2, column=0, pady=10)

add_book_btn = Button(root, text="Add New Book", command=add_new_book_window, bg=button_color, fg="white", width=button_width)
add_book_btn.grid(row=3, column=0, pady=10)

list_copies_btn = Button(root, text="List Loaned Copies", command=list_loaned_window, bg=button_color, fg="white", width=button_width)
list_copies_btn.grid(row=4, column=0, pady=10)

list_late_btn = Button(root, text="List Late Returns", command = OpenNewWindowLateBooks, bg=button_color, fg="white", width=button_width)
list_late_btn.grid(row=5, column=0, pady=10)

view_part_a_btn = Button(root, text="List Late fee for Borrower(s)", command = list_latefee_window, bg=button_color, fg="white", width=button_width)
view_part_a_btn.grid(row=6, column=0, pady=10)

view_part_b_btn = Button(root, text="List Loaned Book Info", command = list_bookinfo_window, bg=button_color, fg="white", width=button_width)
view_part_b_btn.grid(row=7, column=0, pady=10)

root.mainloop()