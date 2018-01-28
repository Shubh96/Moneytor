''''** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***
    ** Project title: Moneytor                                                                                              **
    ** Project description: An expense tracking desktop application                                                         **
    **                                                                                                                      **
    ** Author: Subham Sarda                                                                                                 **
    ** Created: 22nd July 2017                                                                                              **
    ** Version: 1.0                                                                                                         **
    **                                                                                                                      **
    ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***
    **                           @@@@@@@@@@ METHODS IMPLEMENTED IN THE PROJECT @@@@@@@@@@                                   **
    **                                                                                                                      **
    ** MainMenu(): The first menu that is displayed upon executing Moneytor.exe                                             **
    ** Register(): The registration form where the user registers himself into the app                                      **
    ** LogIn():    The login form where the user registers himself into the app                                             **
    ** UserMenu(): The menu to be presented to the user after he logs in successfully                                       **
    ** AddExpense(): The method through which user can add his expenses into balance sheet                                  **
    ** AddDeposit(): The method through which user can add his deposits into balance sheet                                  **
    ** GenerateBalanceSheet(): The method through which user can generate the balance sheet                                 **
    ** StaticUI(): The method to generate the header row of the Balance Sheet through GUI                                   **
    ** DynamicUI(): The method to generate the database rows of the Balance Sheet through GUI                               **
    ** LogOut(): The Method to LogOut the user                                                                              **
    ** Quit(): The Method to Quit the program                                                                               **
    **                                                                                                                      **
    ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ***'''



from tkinter import *                   #To use the graphics in GenerateBalanceSheet() method
import mysql.connector                  #To connect and perform database operations
from mysql.connector import errorcode   #To handle certain exceptions
import time                             #To use sleep() function
import datetime                         #To use strptime() function used in date validation
import re                               #To validate email id using regular expression

#This is the main class in the project which conatins all the code and functions

class Moneytor:

    # Creating the constructor for the Moneytor class
    def __init__(self):

        #self.root = Tk()

        #This try except block checks the existence of database
        try:
            # Establishing connection to Moneytor database with username: 'root', password: '' in localhost server
            self.conn = mysql.connector.connect(user="root", password="", host="localhost", database="Moneytor")
            self.mycursor = self.conn.cursor()                                                                      #setting the cursor.
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:                                                       #Exception if username and password are incorrect
                print("Access to database denied. Incorrect database username or password\n")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:                                                            #Exception if database is not found
                conn= mysql.connector.connect(user="root", password="", host="localhost")                           #Establishing connection
                self.mycursor= conn.cursor()                                                                        #settin up cursor
                cursor= conn.cursor()

                cursor.execute('''CREATE DATABASE Moneytor''')                                                      #creating database
                self.mycursor= conn.cursor()

        #self.master=self.root
        self.row_count=0
        #self.root.title("Moneytor: BalanceSheet")
        self.MainMenu()                                                                                             #Mainmenu invoked

    # The main menu that will be displayed to the user upon running the app
    def MainMenu(self):

        print("\t\t\t@@@@@  Welcome to Moneytor  @@@@@")

        #Try except block to validate the user choice from the main menu
        try:
            userChoiceInMainMenu = int(input("\n1.Register\n2.Login\n3.Quit\n\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid input")
            self.MainMenu()
        except Exception:
            print("Some unexpected exception has occurred")

        if userChoiceInMainMenu == 1:
            self.Register()
        elif userChoiceInMainMenu == 2:
            self.LogIn()
        elif userChoiceInMainMenu == 3:
            self.Quit()
        else:
            print("Invalid Choice, Try again")
            self.MainMenu()

    # The registration form where the user registers himself into the app
    def Register(self):

        print("\n\t\t\t********** REGISTRATION FORM **********")

        #Try except block for name validation
        while TRUE:
            try:
                name = input("Name: ")
                if name=="":
                    raise ValueError
                elif not re.match("^[a-zA-Z]*$", name):
                    raise SyntaxError
                else:
                    break
            except ValueError:
                print("Name cannot be blank.")
            except SyntaxError:
                print("Name must contain only letters")
            except Exception:
                print("Some unexpected exception has occurred")

        # Try except block for email validation
        while TRUE:
            try:
                email = input("E-mail ID: ")
                if email=="":
                    raise ValueError
                elif '@' and '.' not in email:
                    raise SyntaxError
                else:
                    break
            except ValueError:
                print("E-mail cannot be blank.")
            except SyntaxError:
                print("E-mail must contain '@' and '.' ")
            except Exception:
                print("Some unexpected exception has occurred")

        # Try except block for password validation
        while TRUE:
            try:
                password = input("Password: ")
                if password=="":
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Password cannot be blank.")
            except Exception:
                print("Some unexpected exception has occurred")

        # Try except block for date validation
        while TRUE:
            try:
                dob = input("Date of Birth(YYYY/MM/DD): ")

                if datetime.datetime.strptime(dob, '%Y/%m/%d'):
                    break
                elif dob=="":
                    raise SyntaxError
            except ValueError:
                print("Enter valid date in specified format")
            except SyntaxError:
                print("Can't leave this field empty")
            except Exception:
                print("Some unexpected exception has occurred")

        #Try except block to create a new table and then insert registration data if table doesn't exist
        try:
            self.mycursor.execute('''INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `user_dob`) 
                                    VALUES (NULL, '%s', '%s', '%s', '%s')''' %(name, email, password, dob))
            self.conn.commit()
        except mysql.connector.ProgrammingError as err:
                self.mycursor.execute('''CREATE TABLE `moneytor`.`users` ( `user_id` INT NOT NULL AUTO_INCREMENT , `user_name` VARCHAR(255) NOT NULL , 
                                                                            `user_email` VARCHAR(255) NOT NULL , `user_password` VARCHAR(255) NOT NULL , 
                                                                            `user_dob` DATE NOT NULL , PRIMARY KEY (`user_id`), UNIQUE (`user_email`)) 
                                                                            ENGINE = MyISAM''')
                self.conn.commit()

                self.mycursor.execute('''INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `user_dob`) 
                                        VALUES (NULL, '%s', '%s', '%s', '%s')''' % (name, email, password, dob))
                self.conn.commit()


        print("Thank You %s, for registering at Moneytor" %(name))
        self.LogIn()                                                    #invoking the login menu

    # The login form where the user registers himself into the app
    def LogIn(self):

        print("\n\t\t\t********** LOGIN FORM **********")

        while TRUE:
            try:
                login_email_input = input("E-mail ID: ")
                if login_email_input=="":
                    raise ValueError
                elif '@' and '.' not in login_email_input:
                    raise SyntaxError
                else:
                    break
            except ValueError:
                print("E-mail cannot be blank.")
            except SyntaxError:
                print("Invalid Email")
            except Exception:
                print("Some unexpected exception has occurred")

        login_password_input = input("Password: ")

        self.mycursor.execute('''SELECT * FROM `users` WHERE `user_email` LIKE '%s' and `user_password` LIKE '%s' '''
                            %(login_email_input, login_password_input))

        user_list= self.mycursor.fetchall()
        flag=0

        for i in user_list:
            user_logged_in= i
            flag+=1

        if flag==1:
            self.user_is_logged_in=1
            self.logged_in_user_id= user_logged_in[0]
            self.logged_in_user_name = user_logged_in[1]
            time.sleep(1)
            print("Welcome %s" %(self.logged_in_user_name))
            self.UserMenu()
        else:
            print("Incorrect email ID or password. Try again")
            time.sleep(1)
            self.LogIn()

    # The menu to be presented to the user after he logs in successfully
    def UserMenu(self):

        print("\n\t\t\t********** USER MENU **********")

        # Try except block for user input validation in the menu after login
        try:
            userChoiceInUserMenu = int(input("1. Add Expense\n2. Add Deposit\n3. Generate Balance Sheet\n4. Logout\n\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid input\n")
            time.sleep(1)
            self.UserMenu()

        if userChoiceInUserMenu == 1:
            self.AddExpense()
        elif userChoiceInUserMenu == 2:
            self.AddDeposit()
        elif userChoiceInUserMenu == 3:
            self.master = Tk()
            self.master.title("Moneytor: BalanceSheet")
            self.GenerateBalanceSheet()
        elif userChoiceInUserMenu == 4:
            self.LogOut()
        else:
            print("Invalid choice. Please try again..\n")
            time.sleep(1)
            self.UserMenu()

    # The method through which user can add his expenses into balance sheet
    def AddExpense(self):

        # Try except block for date validation
        while TRUE:
            try:
                expense_date = input("Expense Date(YYYY/MM/DD): ")

                if expense_date=="":
                    raise SyntaxError
                elif datetime.datetime.strptime(expense_date, '%Y/%m/%d'):
                    break
            except ValueError:
                print("Enter valid date in specified format\n")
            except SyntaxError:
                print("Can't leave this field empty\n")
            except Exception:
                print("Some unexpected exception has occurred\n")

        # Try except block for description validation
        while TRUE:
            try:
                expense_desc = input("Expense description: ")
                if expense_desc=="":
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Description cannot be blank\n")
            except Exception:
                print("Some unexpected exception has occurred\n")

        # Try except block for amount validation
        while TRUE:
            try:
                debit_amount = input("Expense amount: ")
                if debit_amount == "":
                    raise ValueError
                elif not re.match("^[0-9]{1,45}$", debit_amount):
                    raise SyntaxError
                else:
                    break
            except ValueError:
                print("Amount cannot be blank.\n")
            except SyntaxError:
                print("Enter a valid amount\n")
            except Exception:
                print("Some unexpected exception has occurred\n")

        balance=0

        # Fetching the latest updated balance from the database
        self.mycursor.execute('''SELECT `balance` FROM `balancesheet` WHERE `user_id`=%s ORDER BY `transaction_id` DESC LIMIT 1 '''
                                                                                                                    %(self.logged_in_user_id))
        balance_list =self.mycursor.fetchall()

        for i in balance_list:
            balance= i[0]

        balance= balance- int(debit_amount)

        # Try except block to create a new table and then insert expenditure data if table doesn't exist
        try:
            self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                        `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', NULL, '%s', '%s')'''
                                        %(self.logged_in_user_id, expense_date, expense_desc, debit_amount, balance))
            self.conn.commit()
        except mysql.connector.ProgrammingError as err:
            # creating a table if one doesn't exist
            self.mycursor.execute('''CREATE TABLE `moneytor`.`balancesheet` ( `user_id` INT NOT NULL , `transaction_id` INT NOT NULL AUTO_INCREMENT , 
                                    `transaction_date` DATE NOT NULL , `transaction_desc` VARCHAR(255) NOT NULL , `transaction_credit` INT NULL DEFAULT NULL ,
                                    `transaction_debit` INT NULL DEFAULT NULL , `balance` INT NOT NULL , PRIMARY KEY (`transaction_id`)) ENGINE = MyISAM''')
            self.conn.commit()

            # inserting into the table the expense amount data
            self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                    `transaction_debit`, `balance`)VALUES ('%s', NULL, '%s', '%s', NULL, '%s', '%s')'''
                                  % (self.logged_in_user_id, expense_date, expense_desc, debit_amount, balance))
            self.conn.commit()

        self.UserMenu()

    # The method through which user can add his deposits into balance sheet
    def AddDeposit(self):

        # Try except block for date validation
        while TRUE:
            try:
                deposit_date = input("Deposit Date(YYYY/MM/DD): ")

                if datetime.datetime.strptime(deposit_date, '%Y/%m/%d'):
                    break
                elif deposit_date=="":
                    raise SyntaxError
            except ValueError:
                print("Enter valid date in specified format")
            except SyntaxError:
                print("Can't leave this field empty")
            except Exception:
                print("Some unexpected exception has occurred")

        # Try except block for description validation
        while TRUE:
            try:
                deposit_desc = input("Deposit description: ")
                if deposit_desc=="":
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Deposit description cannot be blank.")
            except Exception:
                print("Some unexpected exception has occurred")

        # Try except block for amount validation
        while TRUE:
            try:
                credit_amount = input("Deposit amount: ")
                if credit_amount == "":
                    raise ValueError
                elif not re.match("^[0-9]{1,45}$", credit_amount):
                    raise SyntaxError
                else:
                    break
            except ValueError:
                print("Amount cannot be blank.")
            except SyntaxError:
                print("Enter a valid amount")
            except Exception:
                print("Some unexpected exception has occurred")

        balance = 0

        #Fetching the latest updated balance from the database
        self.mycursor.execute('''SELECT `balance` FROM `balancesheet` WHERE `user_id`=%s ORDER BY `transaction_id` DESC LIMIT 1 ''' % (self.logged_in_user_id))
        balance_list = self.mycursor.fetchall()

        for i in balance_list:
            balance = i[0]

        balance = balance + int(credit_amount)

        # Try except block to create a new table and then insert amount deposit data if table doesn't exist
        try:
            self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                    `transaction_debit`, `balance`) VALUES ('%s', NULL, '%s', '%s', '%s', NULL, '%s')'''
                                    % (self.logged_in_user_id, deposit_date, deposit_desc,credit_amount, balance))
            self.conn.commit()
        except mysql.connector.ProgrammingError as err:
            #creating a table if one doesn't exist
            self.mycursor.execute('''CREATE TABLE `moneytor`.`balancesheet` ( `user_id` INT NOT NULL , `transaction_id` INT NOT NULL AUTO_INCREMENT , 
                                  `transaction_date` DATE NOT NULL , `transaction_desc` VARCHAR(255) NOT NULL , `transaction_credit` INT NULL DEFAULT NULL,
                                  `transaction_debit` INT NULL DEFAULT NULL , `balance` INT NOT NULL , PRIMARY KEY (`transaction_id`)) ENGINE = MyISAM''')
            self.conn.commit()

            #inserting into the table the deposit amount data
            self.mycursor.execute('''INSERT INTO `balancesheet` (`user_id`, `transaction_id`, `transaction_date`, `transaction_desc`, `transaction_credit`,
                                    `transaction_debit`, `balance`) VALUES ('%s', NULL, '%s', '%s', '%s', NULL, '%s')'''
                                    % (self.logged_in_user_id, deposit_date, deposit_desc, credit_amount, balance))
            self.conn.commit()

        self.UserMenu()

    # The method through which user can generate the balance sheet
    def GenerateBalanceSheet(self):
        self.mycursor.execute('''SELECT * FROM `balancesheet` WHERE `user_id`=%s'''%(self.logged_in_user_id))
        transaction_list = self.mycursor.fetchall()

        #Creating the header row of the balance sheet
        self.StaticUI()

        #Getting all transaction data of the logged in user from the database
        for row_data in transaction_list:
            self.row_count += 1
            self.DynamicUI(row_data)

        self.master.mainloop()

        self.UserMenu()

    # The method to generate the header row of the Balance Sheet through GUI
    def StaticUI(self):

        user_id = Label(self.master, text="User ID", width="10", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        user_id.grid(row=self.row_count, column=0)

        tran_id = Label(self.master, text="Transaction ID", width="14", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_id.grid(row=self.row_count, column=1)

        tran_date = Label(self.master, text="Transaction Date", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_date.grid(row=self.row_count, column=2)

        tran_desc = Label(self.master, text="Transaction Description", width="40", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_desc.grid(row=self.row_count, column=3)

        tran_credit = Label(self.master, text="Transaction Credit", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_credit.grid(row=self.row_count, column=4)

        tran_debit = Label(self.master, text="Transaction Debit", width="20", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
        tran_debit.grid(row=self.row_count, column=5)

        tran_balance = Label(self.master, text="Balance", width="14", relief="solid", font=("Cambria", 12), fg="Black", bg="#ff9900")
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

        user_id = Label(self.master, text=uid, width="10", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        user_id.grid(row=self.row_count, column=0)

        tran_id = Label(self.master, text=tid, width="14", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_id.grid(row=self.row_count, column=1)

        tran_date = Label(self.master, text=tdate, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_date.grid(row=self.row_count, column=2)

        tran_desc = Label(self.master, text=tdesc, width="40", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_desc.grid(row=self.row_count, column=3)

        tran_credit = Label(self.master, text=tcredit, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_credit.grid(row=self.row_count, column=4)

        tran_debit = Label(self.master, text=tdebit, width="20", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_debit.grid(row=self.row_count, column=5)

        tran_balance = Label(self.master, text=tbalance, width="14", relief="solid", font=("Cambria", 12), fg="Blue", bg="#99ffff")
        tran_balance.grid(row=self.row_count, column=6)

    # The Method to LogOut the user
    def LogOut(self):

        self.user_is_logged_in = 0                  #setting the login session variable back to 0 after logout
        self.row_count=0

        time.sleep(1)
        print("You have successfully logged out")

        time.sleep(1.5)
        self.MainMenu()

    # The Method to Quit the program
    def Quit(self):
        print("\nThanks for using Moneytor")
        print("\t\tExiting now...")
        time.sleep(2)                                   #sets the system on a 2 second delay
        exit()

object= Moneytor()