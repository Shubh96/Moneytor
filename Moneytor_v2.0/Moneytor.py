''''** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***
    ** Project title: Moneytor                                                                                              **
    ** Project description: An expense tracking desktop application                                                         **
    **                                                                                                                      **
    ** Author: Subham Sarda                                                                                                 **
    ** Created: 25th July 2017                                                                                              **
    ** Version: 2.0                                                                                                         **
    **                                                                                                                      **
    ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***
    **                        @@@@@@@@@@ MAJOR METHODS IMPLEMENTED IN THE PROJECT @@@@@@@@@@                                **
    **                                                                                                                      **
    ** MainMenuGUI(): The first menu that is displayed upon executing Moneytor.exe                                          **
    ** ServerConnection(): Method to establish connection with the localhost server                                         **
    ** Main(): This method creates the window for the main menu                                                             **
    ** Register(): The registration form where the user registers himself into the app                                      **
    ** LogIn():    The login form where the user registers himself into the app                                             **
    ** UserMenu(): The menu to be presented to the user after he logs in successfully                                       **
    ** AddExpense(): The method through which user can add his expenses into balance sheet                                  **
    ** AddDeposit(): The method through which user can add his deposits into balance sheet                                  **
    ** BalanceSheetGUI(): The method through which user can generate the balance sheet                                      **
    ** StaticUI(): The method to generate the header row of the Balance Sheet through GUI                                   **
    ** DynamicUI(): The method to generate the database rows of the Balance Sheet through GUI                               **
    ** LogOutGUI(): The Method to LogOut the user                                                                           **
    ** Quit(): The Method to Quit the program                                                                               **
    **                                                                                                                      **
    ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***'''

from tkinter import *                   #To use the graphics in GenerateBalanceSheet() method
import mysql.connector                  #To connect and perform database operations
from mysql.connector import errorcode   #To handle certain exceptions
import time                             #To use sleep() function
import datetime                         #To use strptime() function used in date validation
import re                               #To validate email id using regular expression
from tkinter import messagebox

#This is the main class in the project which contains all the code and functions
class Moneytor:

    # Creating the constructor for the Moneytor class
    def __init__(self, master):

        self.ServerConnection()
        self.master = master
        self.Main(self.master)

    #Establishing connection with the local server
    def ServerConnection(self):
        #This try except block checks the existence of database
        try:
            # Establishing connection to Moneytor database with username: 'root', password: '' in localhost server
            self.conn = mysql.connector.connect(user="root", password="", host="localhost", database="Moneytor")
            self.mycursor = self.conn.cursor()                                                                      #setting the cursor.
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:                                                       #Exception if username and password are incorrect
                print("Access to database denied. Incorrect database username or password\n")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:                                                            #Exception if database is not found
                self.conn= mysql.connector.connect(user="root", password="", host="localhost")                           #Establishing connection
                self.mycursor= self.conn.cursor()                                                                        #settin up cursor
                cursor= self.conn.cursor()

                cursor.execute('''CREATE DATABASE Moneytor''')                                                      #creating database
                self.mycursor= self.conn.cursor()

    #Displays the main menu window frame
    def Main(self, master):

        self.master.title("Moneytor:Home")

        self.master.minsize(height=300, width=400)
        self.master.maxsize(height=300, width=400)
        self.master.configure(background="#e6f2ff")
        self.MainMenuGUI()

        # The main menu that will be displayed to the user upon running the app

    #The entire main menu graphical user interface
    def MainMenuGUI(self):

        register_label1 = Label(self.master, text="Welcome to Moneytor!!", width="18", relief="flat", font=("Cambria", 14, "bold"), fg="Blue", bg="#e6f2ff")
        register_label1.place(x=95, y=10)
        register_label1 = Label(self.master, text="Don't have an account?", width="18", relief="flat", font=("Cambria", 12), fg="#cc7a00", bg="#e6f2ff")
        register_label1.place(x=115, y=36)
        register_label1 = Label(self.master, text="Register now & track your expenses OTG", width="32", relief="flat", font=("Cambria", 12), fg="#b30000", bg="#e6f2ff")
        register_label1.place(x=58, y=58)

        self.register_btn= Button(self.master, text="Register Now", width=15, font=("Cambria", 12), activebackground= "#88ff4d", relief="ridge", command=self.RegisterGUI)
        self.register_btn.place(x=125,y=95)

        login_label1 = Label(self.master, text="Already a Moneytor user?", width="20", relief="flat",font=("Cambria", 12), fg="#cc7a00", bg="#e6f2ff")
        login_label1.place(x=105, y=155)
        login_label1 = Label(self.master, text="Welcome back!! Login Here", width="21", relief="flat",font=("Cambria", 12), fg="#006600", bg="#e6f2ff")
        login_label1.place(x=97, y=180)

        self.login_btn = Button(self.master, text="Login Now", width=15, font=("Cambria", 12), activebackground="#88ff4d", relief="ridge", command= self.LoginGUI)
        self.login_btn.place(x=125, y=217)

    # The entire registration form graphical user interface
    def RegisterGUI(self):

        self.menuchoice=1

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)

        self.Register_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')

        self.Register_GUI.title("Moneytor: Register")
        self.Register_GUI.minsize(height=300, width=400)
        self.Register_GUI.maxsize(height=300, width=400)
        self.Register_GUI.configure(background="#d9b3ff")

        register_label = Label(self.Register_GUI, text="REGISTRATION FORM", width="18", relief="flat", font=("Cambria", 14, "bold"), fg="#331a00", bg="#d9b3ff")
        register_label.place(x=105, y=10)

        register_name= Label(self.Register_GUI, text="Name:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        register_name.place(x=47, y=65)

        reg_entry_name=  Entry(self.Register_GUI, width="25", relief="ridge", font=("Century", 11))
        reg_entry_name.place(x=150, y=68)

        register_email = Label(self.Register_GUI, text="E-mail:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        register_email.place(x=44, y=110)

        reg_entry_email = Entry(self.Register_GUI, width="25", relief="ridge", font=("Century", 11))
        reg_entry_email.place(x=150, y=113)

        register_pwd= Label(self.Register_GUI, text="Password:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        register_pwd.place(x=36, y=155)

        reg_entry_pwd = Entry(self.Register_GUI, width="25", relief="ridge", font=("Century", 11), show="*")
        reg_entry_pwd.place(x=150, y=158)

        register_dob= Label(self.Register_GUI, text="Date of Birth:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        register_dob.place(x=25, y=200)

        reg_entry_dob = Entry(self.Register_GUI, width="25", relief="ridge", font=("Century", 11))
        reg_entry_dob.place(x=150, y=203)

        self.register_now= Button(self.Register_GUI, text="Register Now", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", background= "#80ff80",
                                            relief="raised", command= lambda: self.Register(reg_entry_name.get(), reg_entry_email.get(), reg_entry_pwd.get(), reg_entry_dob.get()))
        self.register_now.place(x=150,y=250)

        self.Register_GUI.protocol("WM_DELETE_WINDOW", self.CloseAction)
        self.master.state(newstate='normal')

    # Registration coding
    def Register(self, name, email, password, dob):

        name_not_valid= self.ValidateName(name)
        email_not_valid= self.ValidateEmail(email)
        pwd_not_valid= self.ValidatePwd(password)
        dob_not_valid= self.ValidateDOB(dob)

        if name_not_valid== FALSE and email_not_valid== FALSE and pwd_not_valid== FALSE and dob_not_valid== FALSE:
            try:
                self.mycursor.execute('''INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `user_dob`)
                                        VALUES (NULL, '%s', '%s', '%s', '%s')''' %(name, email, password, dob))
                self.conn.commit()
                self.Register_GUI.destroy()
                #self.Login_GUI.lift()
                self.LoginGUI()
            except mysql.connector.ProgrammingError as err:
                self.mycursor.execute('''CREATE TABLE `moneytor`.`users` ( `user_id` INT NOT NULL AUTO_INCREMENT , `user_name` VARCHAR(255) NOT NULL ,
                                                                                `user_email` VARCHAR(255) NOT NULL , `user_password` VARCHAR(255) NOT NULL ,
                                                                                `user_dob` DATE NOT NULL , PRIMARY KEY (`user_id`), UNIQUE (`user_email`))
                                                                                ENGINE = MyISAM''')
                self.conn.commit()

                self.mycursor.execute('''INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `user_dob`)
                                        VALUES (NULL, '%s', '%s', '%s', '%s')''' % (name, email, password, dob))
                self.conn.commit()
                self.Register_GUI.destroy()
                # self.Login_GUI.lift()
                self.LoginGUI()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Duplicate entry", "This e-mail id already exists.")
        else:
            self.Register_GUI.lift()

    # The entire login form graphical user interface
    def LoginGUI(self):

        self.menuchoice=2

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)

        self.Login_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')

        self.Login_GUI.title("Moneytor: Login")
        self.Login_GUI.minsize(height=300, width=400)
        self.Login_GUI.maxsize(height=300, width=400)
        self.Login_GUI.configure(background="#d9b3ff")

        login_label = Label(self.Login_GUI, text="LOGIN FORM", width="18", relief="flat", font=("Cambria", 14, "bold"), fg="#660033", bg="#d9b3ff")
        login_label.place(x=100, y=10)

        login_email = Label(self.Login_GUI, text="E-mail:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        login_email.place(x=47, y=65)
        login_entry_email = Entry(self.Login_GUI, width="25", relief="ridge", font=("Century", 11))
        login_entry_email.place(x=150, y=68)

        login_pwd= Label(self.Login_GUI, text="Password:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        login_pwd.place(x=37, y=110)
        login_entry_pwd = Entry(self.Login_GUI, width="25", relief="ridge", font=("Century", 11), show="*")
        login_entry_pwd.place(x=150, y=115)

        self.login_now= Button(self.Login_GUI, text="Login Now", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", background= "#80ff80",
                                            relief="raised", command= lambda: self.LogIn(login_entry_email.get(), login_entry_pwd.get()))
        self.login_now.place(x=150,y=162)

        self.Login_GUI.protocol("WM_DELETE_WINDOW", self.CloseAction)
        self.master.state(newstate='normal')

    # Login coding
    def LogIn(self, email, password):

        email_not_valid=self.ValidateEmail(email)
        pwd_not_valid= self.ValidatePwd(password)

        flag = 0

        if email_not_valid== FALSE and pwd_not_valid== FALSE:
            self.mycursor.execute('''SELECT * FROM `users` WHERE `user_email` LIKE '%s' and `user_password` LIKE '%s' ''' %(email, password))
            user_list = self.mycursor.fetchall()
            for i in user_list:
                user_logged_in = i
                flag += 1
        else:
            #messagebox.showerror("Login Error", "Invalid e-mail ID or password.")
            time.sleep(1)
            self.Login_GUI.lift()

        if flag==1:
            self.user_is_logged_in=TRUE
            self.logged_in_user_id= user_logged_in[0]
            self.logged_in_user_name = user_logged_in[1]
            time.sleep(1)
            messagebox.showinfo("Login Success", "Logged in successfully")
            self.UserMenuGUI()
            self.Login_GUI.destroy()
        else:
            self.Login_GUI.lift()

    #The entire user menu graphical user interface
    def UserMenuGUI(self):

        self.menuchoice=3

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)

        self.User_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')

        self.User_GUI.title("Moneytor: User Menu")
        self.User_GUI.minsize(height=400, width=400)
        self.User_GUI.maxsize(height=400, width=400)
        self.User_GUI.configure(background="#d9b3ff")

        text= "Welcome %s" %(self.logged_in_user_name)
        user_label = Label(self.User_GUI, text=text, width="18", relief="flat", font=("Cambria", 14, "bold"), fg="Blue", bg="#d9b3ff")
        user_label.place(x=95, y=10)

        user_label1 = Label(self.User_GUI, text="Want to add your expenses?", width="22", relief="flat", font=("Cambria", 12), fg="#cc7a00", bg="#d9b3ff")
        user_label1.place(x=100, y=40)
        self.add_expense_btn= Button(self.User_GUI, text="Add Expense", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", activebackground= "#88ff4d",
                                                                                                                                    relief="ridge", command=self.AddExpenseGUI)
        self.add_expense_btn.place(x=125,y=75)

        user_label2 = Label(self.User_GUI, text="Want to add your deposits?", width="22", relief="flat", font=("Cambria", 12), fg="#b30000", bg="#d9b3ff")
        user_label2.place(x=100, y=125)
        self.add_deposit_btn= Button(self.User_GUI, text="Add Deposit", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", activebackground= "#88ff4d",
                                                                                                                                    relief="ridge", command=self.AddDepositGUI)
        self.add_deposit_btn.place(x=125,y=160)

        user_label3 = Label(self.User_GUI, text="Generate Balance Sheet", width="20", relief="flat",font=("Cambria", 12), fg="#cc7a00", bg="#d9b3ff")
        user_label3.place(x=107, y=210)
        self.view_bsheet_btn= Button(self.User_GUI, text="Balance Sheet", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", activebackground= "#88ff4d",
                                                                                                                                    relief="ridge", command=self.BalanceSheetGUI)
        self.view_bsheet_btn.place(x=125,y=250)

        user_label4 = Label(self.User_GUI, text="Looking to Log Out?", width="19", relief="flat",font=("Cambria", 12), fg="#006600", bg="#d9b3ff")
        user_label4.place(x=110, y=300)
        self.logout_btn = Button(self.User_GUI, text="Log Out", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", activebackground="#88ff4d",
                                                                                                                                    relief="ridge", command= self.LogOutGUI)

        self.User_GUI.protocol("WM_DELETE_WINDOW", self.CloseAction)

        self.logout_btn.place(x=125, y=340)

    #The entire expense form graphical user interface
    def AddExpenseGUI(self):

        self.menuchoice=4

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)
        self.add_expense_btn.config(state=DISABLED)
        self.add_deposit_btn.config(state=DISABLED)
        self.view_bsheet_btn.config(state=DISABLED)
        self.logout_btn.config(state=DISABLED)

        self.Expense_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')
        self.User_GUI.state(newstate='withdrawn')

        self.Expense_GUI.title("Moneytor: Add Expense")
        self.Expense_GUI.minsize(height=300, width=400)
        self.Expense_GUI.maxsize(height=300, width=400)
        self.Expense_GUI.configure(background="#d9b3ff")

        expense_label = Label(self.Expense_GUI, text="ADD EXPENSE", width="18", relief="flat", font=("Cambria", 14, "bold"), fg="#331a00", bg="#d9b3ff")
        expense_label.place(x=105, y=10)

        expense_amt= Label(self.Expense_GUI, text="Amount:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        expense_amt.place(x=47, y=65)

        expense_entry_amt=  Entry(self.Expense_GUI, width="25", relief="ridge", font=("Century", 11))
        expense_entry_amt.place(x=150, y=68)

        expense_desc = Label(self.Expense_GUI, text="Description:", width="15", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        expense_desc.place(x=38, y=110)

        expense_entry_desc = Entry(self.Expense_GUI, width="25", relief="ridge", font=("Century", 11))
        expense_entry_desc.place(x=150, y=113)

        expense_date= Label(self.Expense_GUI, text="Expense Date:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        expense_date.place(x=25, y=155)

        expense_entry_date = Entry(self.Expense_GUI, width="25", relief="ridge", font=("Century", 11))
        expense_entry_date.place(x=150, y=158)

        self.add_expense= Button(self.Expense_GUI, text="Add", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", background= "#80ff80",
                                            relief="raised", command= lambda: self.AddExpense(expense_entry_amt.get(), expense_entry_desc.get(), expense_entry_date.get()))
        self.add_expense.place(x=150,y=200)

        self.Expense_GUI.protocol("WM_DELETE_WINDOW", self.UserCloseAction)

    #Adding expense and inserting to database
    def AddExpense(self, amount, desc, date):

        amt_not_valid = self.ValidateAmount(amount)
        desc_not_valid = self.ValidateDesc(desc)
        dob_not_valid= self.ValidateDOB(date)

        balance=0

        # Fetching the latest updated balance from the database
        self.mycursor.execute('''SELECT `balance` FROM `balancesheet` WHERE `user_id`=%s ORDER BY `transaction_id` DESC LIMIT 1 '''%(self.logged_in_user_id))
        balance_list =self.mycursor.fetchall()

        for i in balance_list:
            balance= i[0]

        balance= balance- float(amount)

        if amt_not_valid == FALSE and desc_not_valid== FALSE and dob_not_valid==FALSE:
            # Try except block to create a new table and then insert expenditure data if table doesn't exist
            try:
                self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                            `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', NULL, '%s', '%s')'''
                                            %(self.logged_in_user_id, date, desc, amount, balance))
                self.conn.commit()
                messagebox.showinfo("Successful", "Expense added successfully")
                self.Expense_GUI.destroy()
                self.UserMenuGUI()

            except mysql.connector.ProgrammingError as err:
                # creating a table if one doesn't exist
                self.mycursor.execute('''CREATE TABLE `moneytor`.`balancesheet` ( `user_id` INT NOT NULL , `transaction_id` INT NOT NULL AUTO_INCREMENT , 
                                        `transaction_date` DATE NOT NULL , `transaction_desc` VARCHAR(255) NOT NULL , `transaction_credit` INT NULL DEFAULT NULL ,
                                        `transaction_debit` INT NULL DEFAULT NULL , `balance` INT NOT NULL , PRIMARY KEY (`transaction_id`)) ENGINE = MyISAM''')
                self.conn.commit()

                # inserting into the table the expense amount data
                self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                        `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', NULL, '%s', '%s')'''
                                      % (self.logged_in_user_id, date, desc, amount, balance))
                self.conn.commit()
                messagebox.showinfo("Successful", "Expense added successfully")
                self.Expense_GUI.destroy()
                self.UserMenuGUI()
        else:
            self.Expense_GUI.lift()

    # The entire deposit form graphical user interface
    def AddDepositGUI(self):

        self.menuchoice=5

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)
        self.add_expense_btn.config(state=DISABLED)
        self.add_deposit_btn.config(state=DISABLED)
        self.view_bsheet_btn.config(state=DISABLED)
        self.logout_btn.config(state=DISABLED)

        self.Deposit_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')
        self.User_GUI.state(newstate='withdrawn')

        self.Deposit_GUI.title("Moneytor: Add Deposit")
        self.Deposit_GUI.minsize(height=300, width=400)
        self.Deposit_GUI.maxsize(height=300, width=400)
        self.Deposit_GUI.configure(background="#d9b3ff")

        deposit_label = Label(self.Deposit_GUI, text="ADD DEPOSIT", width="18", relief="flat", font=("Cambria", 14, "bold"), fg="#331a00", bg="#d9b3ff")
        deposit_label.place(x=105, y=10)

        deposit_amt= Label(self.Deposit_GUI, text="Amount:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        deposit_amt.place(x=47, y=65)

        deposit_entry_amt=  Entry(self.Deposit_GUI, width="25", relief="ridge", font=("Century", 11))
        deposit_entry_amt.place(x=150, y=68)

        deposit_desc = Label(self.Deposit_GUI, text="Description:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        deposit_desc.place(x=44, y=110)

        deposit_entry_desc = Entry(self.Deposit_GUI, width="25", relief="ridge", font=("Century", 11))
        deposit_entry_desc.place(x=150, y=113)

        deposit_date= Label(self.Deposit_GUI, text="Deposit Date:", width="14", relief="flat", font=("Cambria", 13), fg="#990000", bg="#d9b3ff")
        deposit_date.place(x=25, y=155)

        deposit_entry_date = Entry(self.Deposit_GUI, width="25", relief="ridge", font=("Century", 11))
        deposit_entry_date.place(x=150, y=158)

        self.add_deposit= Button(self.Deposit_GUI, text="Add", width=15, bd= 3, font=("Cambria", 12), highlightbackground="#000000", background= "#80ff80",
                                            relief="raised", command= lambda: self.AddDeposit(deposit_entry_amt.get(), deposit_entry_desc.get(), deposit_entry_date.get()))
        self.add_deposit.place(x=150,y=200)

        self.Deposit_GUI.protocol("WM_DELETE_WINDOW", self.UserCloseAction)

    # Adding deposit and inserting to database
    def AddDeposit(self, amount, desc, date):

        amt_not_valid= self.ValidateAmount(amount)
        desc_not_valid= self.ValidateDesc(desc)
        dob_not_valid= self.ValidateDOB(date)

        balance=0

        # Fetching the latest updated balance from the database
        self.mycursor.execute('''SELECT `balance` FROM `balancesheet` WHERE `user_id`=%s ORDER BY `transaction_id` DESC LIMIT 1 '''%(self.logged_in_user_id))
        balance_list =self.mycursor.fetchall()

        for i in balance_list:
            balance= i[0]

        balance= balance+ float(amount)

        if amt_not_valid == FALSE and desc_not_valid== FALSE and dob_not_valid==FALSE:
            # Try except block to create a new table and then insert expenditure data if table doesn't exist
            try:
                self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                            `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', '%s', NULL, '%s')'''
                                            %(self.logged_in_user_id, date, desc, amount, balance))
                self.conn.commit()
                messagebox.showinfo("Successful", "Deposit added successfully")
                self.Deposit_GUI.destroy()
                self.UserMenuGUI()

            except mysql.connector.ProgrammingError as err:
                # creating a table if one doesn't exist
                self.mycursor.execute('''CREATE TABLE `moneytor`.`balancesheet` ( `user_id` INT NOT NULL , `transaction_id` INT NOT NULL AUTO_INCREMENT , 
                                        `transaction_date` DATE NOT NULL , `transaction_desc` VARCHAR(255) NOT NULL , `transaction_credit` INT NULL DEFAULT NULL ,
                                        `transaction_debit` INT NULL DEFAULT NULL , `balance` INT NOT NULL , PRIMARY KEY (`transaction_id`)) ENGINE = MyISAM''')
                self.conn.commit()

                # inserting into the table the expense amount data
                self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                        `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', NULL, '%s', '%s')'''
                                      % (self.logged_in_user_id, date, desc, amount, balance))
                self.conn.commit()
                messagebox.showinfo("Successful", "Deposit added successfully")
                self.Deposit_GUI.destroy()
                self.UserMenuGUI()
        else:
            self.Deposit_GUI.lift()

    # Displays the balance sheet
    def BalanceSheetGUI(self):

        self.row_count = 0
        self.menuchoice=6

        self.register_btn.config(state=DISABLED)
        self.login_btn.config(state=DISABLED)
        self.add_expense_btn.config(state=DISABLED)
        self.add_deposit_btn.config(state=DISABLED)
        self.view_bsheet_btn.config(state=DISABLED)
        self.logout_btn.config(state=DISABLED)

        self.BalanceSheet_GUI= Toplevel(root)
        self.master.state(newstate='withdrawn')
        self.User_GUI.state(newstate='withdrawn')

        self.BalanceSheet_GUI.title("Moneytor: Generate Balancesheet")
        self.BalanceSheet_GUI.configure(background="#d9b3ff")

        self.mycursor.execute('''SELECT * FROM `balancesheet` WHERE `user_id`=%s'''%(self.logged_in_user_id))
        transaction_list = self.mycursor.fetchall()

        #Creating the header row of the balance sheet
        self.StaticUI()

        #Getting all transaction data of the logged in user from the database
        for row_data in transaction_list:
            self.row_count += 1
            self.DynamicUI(row_data)

        self.BalanceSheet_GUI.protocol("WM_DELETE_WINDOW", self.UserCloseAction)

    # The method to generate the header row of the Balance Sheet through GUI
    def StaticUI(self):

        user_id = Label(self.BalanceSheet_GUI, text="User ID", width="10", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        user_id.grid(row=self.row_count, column=0)

        tran_id = Label(self.BalanceSheet_GUI, text="Transaction ID", width="14", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_id.grid(row=self.row_count, column=1)

        tran_date = Label(self.BalanceSheet_GUI, text="Transaction Date", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_date.grid(row=self.row_count, column=2)

        tran_desc = Label(self.BalanceSheet_GUI, text="Transaction Description", width="40", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_desc.grid(row=self.row_count, column=3)

        tran_credit = Label(self.BalanceSheet_GUI, text="Transaction Credit", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_credit.grid(row=self.row_count, column=4)

        tran_debit = Label(self.BalanceSheet_GUI, text="Transaction Debit", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_debit.grid(row=self.row_count, column=5)

        tran_balance = Label(self.BalanceSheet_GUI, text="Balance", width="14", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_balance.grid(row=self.row_count, column=6)

    # The method to generate the database rows of the Balance Sheet through GUI
    def DynamicUI(self, row_data):

        for i in row_data:
            uid= row_data[0]
            tid= row_data[1]
            tdate = row_data[2]
            tdesc = row_data[3]
            tcredit = row_data[4]
            tdebit = row_data[5]
            tbalance = row_data[6]

        user_id = Label(self.BalanceSheet_GUI, text=uid, width="10", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        user_id.grid(row=self.row_count, column=0)

        tran_id = Label(self.BalanceSheet_GUI, text=tid, width="14", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_id.grid(row=self.row_count, column=1)

        tran_date = Label(self.BalanceSheet_GUI, text=tdate, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_date.grid(row=self.row_count, column=2)

        tran_desc = Label(self.BalanceSheet_GUI, text=tdesc, width="40", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_desc.grid(row=self.row_count, column=3)

        tran_credit = Label(self.BalanceSheet_GUI, text=tcredit, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_credit.grid(row=self.row_count, column=4)

        tran_debit = Label(self.BalanceSheet_GUI, text=tdebit, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_debit.grid(row=self.row_count, column=5)

        tran_balance = Label(self.BalanceSheet_GUI, text=tbalance, width="14", relief="solid", font=("Cambria", 12), fg="Blue", bg="#70db70")
        tran_balance.grid(row=self.row_count, column=6)

    # Function to log out the user
    def LogOutGUI(self):

        self.user_is_logged_in = FALSE
        self.User_GUI.destroy()
        self.master = Tk()
        self.Main(self.master)

    #Validating entered name
    def ValidateName(self, name):

        if len(name)== 0:
            messagebox.showerror("Name Field Empty", "Name field can't be blank")
            self.not_valid= TRUE
        elif not re.match("^[a-zA-Z\s]*$", name):
            messagebox.showerror("Invalid entry", "Name must contain only letters")
            self.not_valid = TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    # Validating entered description
    def ValidateDesc(self, desc):

        if len(desc)== 0:
            messagebox.showerror("Field Empty", "Description field can't be blank")
            self.not_valid= TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    # Validating entered amount
    def ValidateAmount(self, amt):
        if amt == "":
            messagebox.showerror("Amount Field Empty", "Amount field can't be blank")
            self.not_valid= TRUE
        elif not re.match("^[0-9]{1,45}$", amt):
            messagebox.showerror("Invalid entry", "Amount must contain only digits")
            self.not_valid = TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    # Validating entered email
    def ValidateEmail(self, email):

        if email=="":
            messagebox.showerror("E-mail Field Empty", "E-mail field can't be blank")
            self.not_valid = TRUE
        elif '@' and '.' not in email:
            messagebox.showerror("Invalid entry", "E-mail must contain '@' and '.'")
            self.not_valid = TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    # Validating entered password
    def ValidatePwd(self, pwd):

        if pwd=="":
            messagebox.showerror("Password Field Empty", "Password field can't be blank")
            self.not_valid = TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    # Validating entered date of birth
    def ValidateDOB(self,dob):

        if dob=="":
            messagebox.showerror("Date Field Empty", "Date field can't be blank")
            self.not_valid = TRUE
        elif not datetime.datetime.strptime(dob, '%Y/%m/%d'):
            messagebox.showerror("Invalid entry", "Enter date in (YYYY/MM/DD) format")
            self.not_valid = TRUE
        else:
            self.not_valid= FALSE

        return self.not_valid

    #Action to be performed when close button is clicked by the user before logging in
    def CloseAction(self):

        if self.menuchoice==1:
            self.Register_GUI.destroy()
        elif self.menuchoice==2:
            self.Login_GUI.destroy()
        elif self.menuchoice==3:
            self.User_GUI.destroy()
            self.user_is_logged_in=FALSE
            self.master = Tk()
            self.Main(self.master)

        root.lift()
        self.register_btn.config(state=NORMAL)
        self.login_btn.config(state=NORMAL)

    # Action to be performed when close button is clicked by the user after logging in
    def UserCloseAction(self):

        if self.menuchoice==4:
            self.Expense_GUI.destroy()
        elif self.menuchoice==5:
            self.Deposit_GUI.destroy()
        elif self.menuchoice == 6:
            self.BalanceSheet_GUI.destroy()

        self.User_GUI.state(newstate='normal')
        self.User_GUI.lift()

        self.add_expense_btn.config(state=NORMAL)
        self.add_deposit_btn.config(state=NORMAL)
        self.view_bsheet_btn.config(state=NORMAL)
        self.logout_btn.config(state=NORMAL)

root= Tk()
GUI= Moneytor(root)
root.mainloop()