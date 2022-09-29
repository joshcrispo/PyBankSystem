# Joshua AL Rasbi - C20356061 - Project Python Bank

# Importing modules to python file
# importing date was used to attempt to tackle monthly transactions
# random allows me to set an ID to users with random.randint method
# import os helps with file management using os.replace to be able to replace original files
from datetime import date, timedelta
import random
import os


# Customer class
class Customer (object):

    # default constructor for customer class
    def __init__(self, name="", age=0, gender=""):
        """Takes 3 parameters: name, age, gender to initialise """
        self.name = name
        self.age = age
        self.gender = gender
        self.cust_id = random.randint(0, 999999)

    # default method for printing data members
    def __str__(self):
        """This method doesn't require a parameter, simply returns a formatted version of the initialsed attributes"""
        return "{}|{}|{}|{}".format(self.cust_id, self.name, self.age, self.gender)

    # method for printing to customer.txt file
    def print_cust_to_file(self):
        """Method for printing to file associated with customers"""
        with open("customers.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.__str__())


# BankAccount Super Class
class BankAccount (object):

    # constructor for BankAccount class
    def __init__(self, name="", age=0, gender="", username="", password="", acc_no=0, balance=0):
        """Takes 7 parameters when called and initialises, but has 13 attributes linked to the class"""
        self.name = name
        self.age = age
        self.gender = gender
        self.username = username
        self.password = password
        self.acc_no = acc_no
        self.balance = balance
        self.client_details_list = []
        self.transfer_list = []
        self.convert_str = ""
        self.transaction_id = 0
        self.loggedin = False

    # method for formatting instance's data, used to organise for file
    def format_for_file(self):
        """This method doesn't require a parameter, simply returns a formatted version of the initialsed attributes"""
        return "{}|{}|{}|{}|{}|{}|{}".format(self.acc_no, self.username, self.password, self.balance, self.name, self.age, self.gender)

    # method for printing to accounts.txt
    def print_bank_acc_to_file(self):
        """Method for printing to file associated with accounts"""
        with open("accounts.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # method for displaying all transactions of associated BankAccount -> prints savings/checking
    def display_transactions(self):
        """Method that prints all transactions to user that holds the respective account number"""
        # Read file that holds all transactions
        with open("accountTransactions.txt", "r") as file_object:
            # Iterate through each line
            for line in file_object:
                # if the account no occurs in the line
                if str(self.acc_no) in line:
                    # print line where it occurs
                    print(line)
        print()

    # method for logging into bank account
    def login(self, name="", password=""):
        """Method that requires 2 parameters, 1st - name, 2nd - pass, Reads a file, then references and
        provide login details to bankAccount instance"""
        # Reads file
        with open("accounts.txt", "r") as file_object:
            # Iterates lines through file
            for lines in file_object:
                # If the name that has been passed is in a line in the file
                if str(name) in lines:
                    # split the lines with '|' and place into list
                    self.client_details_list = lines.split("|")
                    # check if name is the same as whats in the list with appropriate index position
                    if str(name) == str(self.client_details_list[1]):
                        # check for password in the list
                        if str(password) == str(self.client_details_list[2]):
                            # change attribute value from false to True
                            self.loggedin = True

            # if all conditions are true and loggedin becomes True set all login details to the class
            if self.loggedin is True:
                self.acc_no = int(self.client_details_list[0])
                self.username = self.client_details_list[1]
                self.password = self.client_details_list[2]
                self.balance = int(self.client_details_list[3])
                self.name = self.client_details_list[4]
                self.age = self .client_details_list[5]
                self.gender = self.client_details_list[6]

                # return true for conditions in main
                return True

            else:
                # error checking
                print("Wrong details")

    # method check balance
    def view_balance(self):
        """Method that checks balance of associated instance"""
        print("Your general account balance is €{}".format(self.balance))

    # method deposit
    def deposit_cash(self, amount):
        """Method that deposits cash of BankAccount instance, passes 1 parameter: AMOUNT TO BE DEPOSITED"""
        self.balance += amount
        # Sets random number between 0 and a million to be the identifier
        self.transaction_id = random.randint(0, 999999)
        # format to be used for printing to file
        caller = "{}|Deposit {} to Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

        # open file associated with transactions with intention to write at the end of it
        with open("accountTransactions.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(caller)

        # deleting lines of file
        # open file one for read and one to write
        with open("accounts.txt", "r") as file_input:
            with open("temp.txt", "w") as file_output:
                # iterate all lines from file
                for line in file_input:
                    # if the account number contained in a line then don't write it
                    if str(self.acc_no) not in line.strip("\n"):
                        file_output.write(line)

        # replace file with original name
        os.replace('temp.txt', 'accounts.txt')

        # take the original file replaced, here is accounts.txt and append to it
        with open("accounts.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # method transfer
    def transfer_cash(self, amount, acc_no):
        """Method for transferring cash from logged in Bank Account instance to another, passing 2 parameters:
        1 - amount to transfer, 2 - account no of receiver"""
        # checks if you have enough balance
        if self.balance < amount:
            print("Sorry, insufficient funds")
        elif self.balance > amount:
            # subtract from balance of the instance object
            self.balance -= amount
            # sets a random number as identifier
            self.transaction_id = random.randint(0, 999999)
            # format to be used to print to file
            caller = "{}|Transferred {} from Account No. {} to Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, acc_no, self.balance)

            # Printing into file
            with open("accountTransactions.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(caller)

            # Updating File
            # Deleting line
            with open("accounts.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(self.acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accounts.txt')

            # Adding Line
            with open("accounts.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(self.format_for_file())

            # Reading file to find associated receiver account
            with open("accounts.txt", "r") as file_object:
                for lines in file_object:
                    if str(acc_no) in lines:
                        self.transfer_list = lines.split("|")
                        self.transfer_list[3] = int(self.transfer_list[3]) + amount
                        self.transfer_list[3] = str(self.transfer_list[3])
                        self.convert_str = '|'.join(self.transfer_list)

            # Updating Receiver Account
            # Deleting line
            with open("accounts.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accounts.txt')

            # Adding
            with open("accounts.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(self.convert_str)

    def withdraw_cash(self, amount):
        """Method for withdrawing cash, 1 parameter needed: amount"""
        # Checks if enough balance
        if self.balance < amount:
            print("Sorry, insufficient funds")
        elif self.balance > amount:
            # Subtracting withdrawn amount from balance
            self.balance -= amount
            # generating random number as identifier
            self.transaction_id = random.randint(0, 999999)
            # format for printing to file
            caller = "{}| Withdrew {} from Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

            # Adding line to file
            with open("accountTransactions.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(caller)

            # Updating file by deleting line by replacing it with temp.txt
            with open("accounts.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(self.acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accounts.txt')

            # Adding updated line to file with new balance
            with open("accounts.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(self.format_for_file())

    # method delete Account
    def delete_account(self):
        """Method for deleting an account"""
        # Updating file by deleting line by replacing it with temp.txt
        with open("accounts.txt", "r") as file_input:
            with open("temp.txt", "w") as file_output:
                # iterate all lines from file
                for line in file_input:
                    # if substring contain in a line then don't write it
                    if str(self.acc_no) not in line.strip("\n"):
                        file_output.write(line)

        # replace file with original name
        os.replace('temp.txt', 'accounts.txt')


# SavingsAccount subclass of BankAccount
class SavingsAccount (BankAccount):

    # constructor for Savings Account class
    def __init__(self, name="", age=0, gender="", username="", password="", acc_no=0, balance=0, mode="Savings", withdrew_date=date.today().isoformat()):
        """"Method for initialising object instances passes 7 parameter"""
        # Inheriting and initialising attributes with superclass BankAccount
        BankAccount.__init__(self, name, age, gender, username, password, acc_no, balance)
        self.mode = mode
        self.withdrew_date = withdrew_date

    # default method for printing data members
    def __str__(self):
        """Method for formatting when called in main"""
        result_str = BankAccount.__str__(self) + "|{}|{}".format(self.mode, self.withdrew_date)
        return result_str

    # method for setting balance for account
    def set_balance_savings(self, amount=0):
        """Method for setting the balance for savings account, passes 1 parameter: amount"""
        # Checks if amount is negative
        if amount < 0:
            print("Can't have negative set up balance")
        else:
            self.balance = amount

            # Adds to file associated with Savings Accounts
            with open("accountsSaving.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(self.format_for_file())

    # method for viewing balance
    def view_balance(self):
        """Simply prints out the savings account object instance's balance"""
        print("Your savings account balance is €{}".format(self.balance))

    # method for formatting data of class instances
    def format_for_file(self):
        """Formats the attributes in a certain way to be printed into file"""
        return "{}|{}|{}|{}|{}|{}|{}|{}|{}".format(self.acc_no, self.username, self.password, self.balance, self.name, self.age, self.gender, self.mode, self.withdrew_date)

    # method for depositing money of savings account class instance
    def deposit_cash(self, amount):
        """Method for depositing cash, passes 1 parameter: amount"""
        # Adding amount to the balance
        self.balance += amount
        # Generating random number to be set as identifier
        self.transaction_id = random.randint(0, 999999)
        # Format of transaction to be added to file
        caller = "{}|Deposit {} to Savings Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

        # Adding transaction to file by line
        with open("accountTransactions.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(caller)

        # Updating file by deleting line by replacing it with temp.txt
        with open("accountsSaving.txt", "r") as file_input:
            with open("temp.txt", "w") as file_output:
                # iterate all lines from file
                for line in file_input:
                    # if substring contain in a line then don't write it
                    if str(self.acc_no) not in line.strip("\n"):
                        file_output.write(line)

        # replace file with original name
        os.replace('temp.txt', 'accountsSaving.txt')

        # Adding new line with updated balance to associated savings account file
        with open("accountsSaving.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # Method for withdrawing cash from savings account object instances
    def withdraw_cash(self, amount):
        """Method for withdrawing cash, 1 parameter needed: amount"""
        # Checks if enough balance
        if self.balance < amount:
            print("Sorry, insufficient funds")
        elif self.balance > amount:
            # Subtracting withdrawn amount from balance
            self.balance -= amount
            # generating random number as identifier
            self.transaction_id = random.randint(0, 999999)
            # format for printing to file
            caller = "{}| Withdrew {} from Savings Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

            # Adding line to file
            with open("accountTransactions.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(caller)

            # Updating file by deleting line by replacing it with temp.txt
            with open("accountsSaving.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(self.acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accountsSaving.txt')

            # Adding updated line to file with new balance
            with open("accountsSaving.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(self.format_for_file())

    # Method for logging in, getting values from file
    def login(self, acc_no=0, password=""):
        """Method that requires 2 parameters, 1st - account number, 2nd - password, Reads a file, then references and
        provide login details to bankAccount instance"""
        # Reads file and checks each line for corresponding account number and password with index position in list
        with open("accountsSaving.txt", "r") as file_object:
            for lines in file_object:
                if str(acc_no) in lines:
                    self.client_details_list = lines.split("|")
                    if str(acc_no) == str(self.client_details_list[0]):
                        if str(password) == str(self.client_details_list[2]):
                            self.loggedin = True

            # If all conditions are met and account no and password are in the same line
            # Set attribute values to appropriate attribute by index
            if self.loggedin is True:
                self.acc_no = int(self.client_details_list[0])
                self.username = self.client_details_list[1]
                self.password = self.client_details_list[2]
                self.balance = int(self.client_details_list[3])
                self.name = self.client_details_list[4]
                self.age = self .client_details_list[5]
                self.gender = self.client_details_list[6]
                self.mode = self.client_details_list[7]
                # In attempt to use date to get 30 days
                self.withdrew_date = self.client_details_list[8]

                # return true for conditions in main
                return True

            # else takes account for wrong inputs
            else:
                print("You have no account/You entered the wrong details")

    # Only general account can perform money transfer
    def transfer_cash(self, amount, acc_no):
        """Saving's account transfer instance does nothing"""
        return

    # Method for deleting an account
    def delete_account(self, mode="Savings"):
        """Delete account method, has preset parameter: mode=Savings"""
        # Checks to make sure balance is 0
        if self.balance == 0:
            # Generates a random ID to transaction
            self.transaction_id = random.randint(0, 999999)
            # Format so that it will be printed to file
            caller = "{}|Deleted Savings Account of {} ".format(self.transaction_id, self.acc_no)

            # Add formatted line to file
            with open("accountTransactions.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(caller)

            # Updating file by not included lines with Savings
            with open("accountsSaving.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(self.acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accountsSaving.txt')

            print("SUCCESSFUL DELETION")

        # checks to show user balance isn't 0
        elif self.balance > 0:
            print("Sorry, still have positive balance\nFAILED DELETION")
        elif self.balance < 0:
            print("Sorry, you have negative balance!\nFAILED DELETION")


class CheckingAccount (BankAccount):

    # default constructor for Checking Account class
    def __init__(self, name="", age=0, gender="", username="", password="", acc_no=0, balance=0, mode="Checking"):
        """Method for initialising values to CheckingAccount class instances, passes 8 parameters"""
        # Inherits 7 attributes from super class
        BankAccount.__init__(self, name, age, gender, username, password, acc_no, balance)
        self.mode = mode

    # default method for printing data members
    def __str__(self):
        """Method for formatting to be printed to file"""
        result_str = BankAccount.__str__(self) + "|{}".format(self.mode)
        return result_str

    # Method for setting balance of checking account during creation
    def set_balance_checking(self, amount=0):
        """Method for setting balance of checking account user, passes parameter : amount """
        self.balance = amount

        # Adds to file by end of line
        with open("accountsChecking.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # Method to check balance of checking account
    def view_balance(self):
        """Method to show balance, call in main/driver code"""
        print("Your checking account balance is €{}".format(self.balance))

    # Method to organise class attributes
    def format_for_file(self):
        """Method for formatting to be printed to file"""
        return "{}|{}|{}|{}|{}|{}|{}|{}".format(self.acc_no, self.username, self.password, self.balance, self.name, self.age, self.gender, self.mode)

    # Method to deposit cash
    def deposit_cash(self, amount):
        """Method for deposit to checking account, passes 1 parameter : amount -> money to be deposit"""
        self.balance += amount
        self.transaction_id = random.randint(0, 999999)
        caller = "{}|Deposit {} to Checking Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

        # Add transaction line to newline at end of file
        with open("accountTransactions.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(caller)

        # Updating File by deleting
        with open("accountsChecking.txt", "r") as file_input:
            with open("temp.txt", "w") as file_output:
                # iterate all lines from file
                for line in file_input:
                    # if substring contain in a line then don't write it
                    if str(self.acc_no) not in line.strip("\n"):
                        file_output.write(line)

        # replace file with original name
        os.replace('temp.txt', 'accountsChecking.txt')

        # Updating File after deletion add to it with new balance
        with open("accountsChecking.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # Method for withdrawing cash checking account
    def withdraw_cash(self, amount):
        """Method for withdrawing cash passed by 1 parameter: amount -> money to be withdrawn"""
        self.balance -= amount
        self.transaction_id = random.randint(0, 999999)
        caller = "{}| Withdrew {} from Checking Account No. {}, New balance is {}".format(self.transaction_id, amount, self.acc_no, self.balance)

        # Add transaction line to newline at end of file
        with open("accountTransactions.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(caller)

        # Update file by deletion (non-inclusion) of line with acc.no
        with open("accountsChecking.txt", "r") as file_input:
            with open("temp.txt", "w") as file_output:
                # iterate all lines from file
                for line in file_input:
                    # if substring contain in a line then don't write it
                    if str(self.acc_no) not in line.strip("\n"):
                        file_output.write(line)

        # replace file with original name
        os.replace('temp.txt', 'accountsChecking.txt')

        # Update file by adding new line to file with updated balance
        with open("accountsChecking.txt", "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(self.format_for_file())

    # Method for logging in, getting values from file
    def login(self, acc_no=0, password=""):
        """Method that requires 2 parameters, 1st - account number, 2nd - password, Reads a file, then references and
        provide login details to bankAccount instance"""

        # Reads file and checks each line for corresponding account number and password with index position in list
        with open("accountsChecking.txt", "r") as file_object:
            for lines in file_object:
                if str(acc_no) in lines:
                    self.client_details_list = lines.split("|")
                    if str(acc_no) == str(self.client_details_list[0]):
                        if str(password) == str(self.client_details_list[2]):
                            self.loggedin = True

            # If all conditions are met and account no and password are in the same line
            # Set attribute values to appropriate attribute by index
            if self.loggedin is True:
                self.acc_no = int(self.client_details_list[0])
                self.username = self.client_details_list[1]
                self.password = self.client_details_list[2]
                self.balance = int(self.client_details_list[3])
                self.name = self.client_details_list[4]
                self.age = self .client_details_list[5]
                self.gender = self.client_details_list[6]
                self.mode = self.client_details_list[7]

                return True

            # Lets user know that there is not account corresponding to input
            else:
                print("You have no account/You entered the wrong details")

    # Only general account can perform money transfer
    def transfer_cash(self, amount, acc_no):
        """No action"""
        return

    # Method for delete Checking Account instance
    def delete_account(self, mode="Checking"):
        """Method for deleting account, with the use account number, preset parameter : mode=Checking"""
        # if only allows deletion if balance of instance is 0
        if self.balance == 0:
            self.transaction_id = random.randint(0, 999999)
            caller = "{}|Deleted Checking Account of {} ".format(self.transaction_id, self.acc_no)

            # Add transaction line to newline at end of file
            with open("accountTransactions.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(caller)

            # Update file by deletion (non-inclusion) of line with acc.no
            with open("accountsChecking.txt", "r") as file_input:
                with open("temp.txt", "w") as file_output:
                    # iterate all lines from file
                    for line in file_input:
                        # if substring contain in a line then don't write it
                        if str(self.acc_no) not in line.strip("\n"):
                            file_output.write(line)

            # replace file with original name
            os.replace('temp.txt', 'accountsChecking.txt')

            print("SUCCESSFUL DELETION!")

        elif self.balance > 0:
            print("Sorry, still have positive balance\nFAILED DELETION")
        elif self.balance < 0:
            print("Sorry, you have negative balance!\nFAILED DELETION")


# Function that helps initialise Sub class CheckingAccount/SavingsAccount
def get_attributes(acc_no):
    """This function takes 1 parameter : account number, and returns a list from line of words in a file
    that account number was referenced"""
    new_lst = []
    with open("accounts.txt", "r") as file_object:
        for lines in file_object:
            if str(acc_no) in lines:
                lst = lines.split("|")

                for el in lst:
                    new_lst.append(el.strip())
                # Set balance at 0 at creation
                new_lst[3] = 0
    # returned list
    return new_lst


def main():
    """Method main is the Bank system provides menus for user to be able to interact with the system"""
    bank_object = BankAccount()
    print("Welcome to Josh's Very Swaggy Bank!")
    try:
        while True:
            # Menu with prompt
            option = int(input("Menu\n1) Login \n2) Register \n3) Quit\nSelect an option: "))
            # if 1: Ask to login
            if option == 1:
                print("Enter Login Details: ")
                username = input("Enter your username")
                pword = input("Enter your password")

                # login returns boolean if login is right set boolean to TRUE then it can continue
                result = bank_object.login(username, pword)
                if result is True:
                    try:
                        while True:
                            # After login has been successful
                            # 2nd Menu is shown
                            second_op = int(input("Select an option from Menu 1-4, 5 to Quit\n =====Menu=====\n1) Create a savings/checking account \n2) View transactions \n3) Account Services \n4) Delete account \n5) Exit:\n"))
                            if second_op == 1:
                                print("Choose type of account:\n1) Create Savings Account\n2) Create Checking Account")
                                try:
                                    third_op = int(input("Select an option: "))
                                    # if 1st choice create children accounts
                                    if third_op == 1:
                                        print("Creating Savings Account:\n")
                                        user_acc_no = int(input("Enter you account number"))
                                        # Function call returns list, list placed in list
                                        attributes = get_attributes(user_acc_no)
                                        # Checks if account holder age is 14 or over
                                        if int(attributes[5]) >= 14:
                                            # initialises attribute values to instance object bank_object_sav
                                            bank_object_sav = SavingsAccount(str(attributes[4]), int(attributes[5]), str(attributes[6]), str(attributes[1]), str(attributes[2]), int(attributes[0]), int(attributes[3]))
                                            amount = int(input("Enter amount to be placed in savings: "))
                                            # method calls
                                            bank_object_sav.set_balance_savings(amount)
                                            bank_object_sav.view_balance()
                                        else:
                                            print("SAVINGS ACCOUNT ERROR:\n NEED TO BE 14+")
                                    elif third_op == 2:
                                        print("Creating Checking Account:\n")
                                        user_acc_no = int(input("Enter you account number"))
                                        attributes = get_attributes(user_acc_no)
                                        # Checks if account holder age is 18 or over
                                        if int(attributes[5]) >= 18:
                                            # initialises attribute values to instance object bank_object_sav
                                            bank_object_checking = CheckingAccount(str(attributes[4]), int(attributes[5]), str(attributes[6]), str(attributes[1]), str(attributes[2]), int(attributes[0]), int(attributes[3]))
                                            amount = int(input("Enter amount to be placed in checking account: "))
                                            # method calls
                                            bank_object_checking.set_balance_checking(amount)
                                            bank_object_checking.view_balance()
                                        else:
                                            print("CHECKING ACCOUNT ERROR:\nNEED TO BE 18+")
                                except ValueError:
                                    print("Enter a valid option 1/2")
                            elif second_op == 2:
                                # Read from account transactions file search for word in line then print line
                                print("Your transactions: ")
                                bank_object.display_transactions()
                            elif second_op == 3:
                                # 3rd Menu for showing bank systems functionalities
                                print("Account Services :\n1) View Balance\n2) Deposit cash\n3) Transfer cash\n4) Withdraw cash")
                                try:
                                    forth_op = int(input("Select an option: "))
                                    # if 1 check balance of referenced account (general/savings/checking)
                                    if forth_op == 1:
                                        try:
                                            fifth_op = int(input("Which Account's balance:\n1)General\n2)Savings\n3)Checking\n:"))
                                            if fifth_op == 1:
                                                bank_object.view_balance()
                                            elif fifth_op == 2:
                                                try:
                                                    bank_object_sav = SavingsAccount()
                                                    acc_no = int(input("Enter your Account number: "))
                                                    pword = input("Password: ")
                                                    result = bank_object_sav.login(acc_no, pword)
                                                    if result is True:
                                                        bank_object_sav.view_balance()
                                                except NameError:
                                                    print("You don't have a savings account")
                                            elif fifth_op == 3:
                                                try:
                                                    bank_object_checking = CheckingAccount()
                                                    acc_no = int(input("Enter your Account number: "))
                                                    pword = input("Password: ")
                                                    result = bank_object_checking.login(acc_no, pword)
                                                    if result is True:
                                                        bank_object_checking.view_balance()
                                                except NameError:
                                                    print("You don't have a checking account")
                                        except ValueError:
                                            print("Enter valid option:\n1)General\n2)Savings\n3)Checking\n:")
                                    elif forth_op == 2:
                                        try:
                                            # if 2 deposit amount to referenced account (general/savings/checking)
                                            seven_op = int(input("Which account would you like to deposit to:\n1)General\n2)Savings\n3)Checking\n:"))
                                            if seven_op == 1:
                                                amount = int(input("Enter amount to deposit : €"))
                                                bank_object.deposit_cash(amount)
                                            elif seven_op == 2:
                                                bank_object_sav = SavingsAccount()
                                                acc_no = int(input("Enter your Account number: "))
                                                pword = input("Password: ")
                                                result = bank_object_sav.login(acc_no, pword)
                                                if result is True:
                                                    amount = int(input("Enter amount to deposit : €"))
                                                    bank_object_sav.deposit_cash(amount)
                                            elif seven_op == 3:
                                                bank_object_checking = CheckingAccount()
                                                acc_no = int(input("Enter your Account number: "))
                                                pword = input("Password: ")
                                                result = bank_object_checking.login(acc_no, pword)
                                                if result is True:
                                                    amount = int(input("Enter amount to deposit : €"))
                                                    bank_object_checking.deposit_cash(amount)
                                        except ValueError:
                                            print("Enter valid option:\n1)General\n2)Savings\n3)Checking\n:")
                                    elif forth_op == 3:
                                        # if 3 Transfer account option
                                        print("Transferring cash:")
                                        amount = int(input("Enter amount to transfer: €"))
                                        acc_no = int(input("Enter Account No. of receiver: "))
                                        bank_object.transfer_cash(amount, acc_no)
                                    elif forth_op == 4:
                                        try:
                                            # if 4 Withdraw amount from referenced account (general/savings/checking)
                                            six_op = int(input("Which account would you like to withdraw from:\n1)General\n2)Savings\n3)Checking\n:"))
                                            if six_op == 1:
                                                amount = int(input("Enter amount you'd like to withdraw : €"))
                                                bank_object.withdraw_cash(amount)
                                            elif six_op == 2:
                                                bank_object_sav = SavingsAccount()
                                                acc_no = int(input("Enter your Account number: "))
                                                pword = input("Password: ")
                                                result = bank_object_sav.login(acc_no, pword)
                                                if result is True:
                                                    amount = int(input("Enter amount you'd like to withdraw : €"))
                                                    bank_object_sav.withdraw_cash(amount)

                                                # Attempt to have a 30 day withdrawal limit
                                                # if getattr(bank_object_sav, bank_object_sav.withdrew_date).days - date.today().days >= 30:
                                                    # amount = int(input("Enter amount you'd like to withdraw : €"))
                                                    # bank_object_sav.withdraw_cash(amount)
                                            elif six_op == 3:
                                                bank_object_checking = CheckingAccount()
                                                acc_no = int(input("Enter your Account number: "))
                                                pword = input("Password: ")
                                                result = bank_object_checking.login(acc_no, pword)
                                                if result is True:
                                                    amount = int(input("Enter amount you'd like to withdraw : €"))
                                                    bank_object_checking.withdraw_cash(amount)
                                        except ValueError:
                                            print("Enter valid option:\n1)General\n2)Savings\n3)Checking")
                                except ValueError:
                                    print("Enter a valid option 1-4")
                            elif second_op == 4:
                                try:
                                    # if 4th gives user to delete sub classes (savings/checking)
                                    eight_op = int(input("Which account would you like to delete:\n1)Savings\n2)Checking\n:"))
                                    if eight_op == 1:
                                        print("Deleting Savings Account")
                                        bank_object_sav = SavingsAccount()
                                        acc_no = int(input("Enter your Account number: "))
                                        pword = input("Password: ")
                                        result = bank_object_sav.login(acc_no, pword)
                                        if result is True:
                                            prompt = input("Are you sure ? Y/N")
                                            if prompt == "Y":
                                                bank_object_sav.delete_account()
                                            else:
                                                print("Failed Account Deletion")
                                    elif eight_op == 2:
                                        print("Deleting Checking Account")
                                        bank_object_checking = CheckingAccount()
                                        acc_no = int(input("Enter your Account number: "))
                                        pword = input("Password: ")
                                        result = bank_object_checking.login(acc_no, pword)
                                        if result is True:
                                            prompt = input("Are you sure ? Y/N")
                                            if prompt == "Y":
                                                bank_object_checking.delete_account()
                                            else:
                                                print("Failed Account Deletion")
                                except ValueError:
                                    print("Enter valid option:\n1)Savings\n2)Checking")
                            elif second_op == 5:
                                print("Logging out!")
                                exit("Thank you!")
                    except ValueError:
                        print("Enter a valid option 1-5")

            # Registration
            elif option == 2:
                # registration
                name = input("Enter your fullname")
                for i in "123456789":
                    if i in name:
                        exit("Error: Exiting please enter characters for fullname")
                age = input("Enter your age")
                gender = input("Sex (Male/Female/Other): ")
                username = input("Enter a username")
                password = input("Enter a password")
                acc_no = random.randint(0, 99999)
                cust1 = Customer(name, int(age), gender)
                bank1 = BankAccount(name, int(age), gender, username, password, acc_no)
                cust1.print_cust_to_file()
                bank1.print_bank_acc_to_file()

            # Quit main
            elif option == 3:
                exit('Have a nice day')
            elif option != 1 or 2 or 3:
                print("Select between 1-3")
    except ValueError:
        print('Enter a valid option 1-3')


main()
