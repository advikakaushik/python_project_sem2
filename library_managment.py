import os
import datetime

# File paths
login_cred = "user_login.txt"
admin_cred = "admin_login.txt"
borrow_book_file = "borrowed_books.txt"
file_path = "books.txt"

# Global variables
available_books = []

# Functions to manage user login
def load_data(file_path):
    """
    Function to load data from file.
    """
    global available_books
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                title, author = line.strip().split(',')
                available_books.append((title, author))

def save_data(file_path):
    """
    Function to save data to file.
    """
    with open(file_path, 'w') as file:
        for book in available_books:
            file.write(','.join(book) + '\n')

def write_login_credentials(username, password, file_path):
    """
    Function to write login credentials to file.
    """
    with open(file_path, "a") as file:
        file.write(f"{username},{password}\n")

def read_login_credentials(file_path):
    """
    Function to read login credentials from file.
    """
    login_credentials = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                login_credentials[username] = password
    return login_credentials

def login(login_credentials):
    """
    Function for user login.
    """
    i = 0
    username = input("USERNAME: ")
    while i < 3:
        password = input("PASSWORD: ")
        if username in login_credentials and login_credentials[username] == password:
            print("Login successful!")
            return username
        else:
            print("Invalid login ID or Password")
            i += 1
    if i == 3:
        print("Too many unsuccessful login attempts. Exiting...")
        exit()

def signup():
    """
    Function for user signup.
    """
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    write_login_credentials(username, password, login_cred)
    print("Signup successful!")

# Functions for admin operations...
# (The same as before)

def admin_login():
    """
    Function for admin login.
    """
    fixed_admin_username = "admin"
    fixed_admin_password = "admin@123"
    print("ADMIN LOGIN")
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    if username == fixed_admin_username and password == fixed_admin_password:
        print("Login successful!")
        return username
    else:
        print("Invalid admin username or password.")
        exit()

# Function to borrow a book
def borrow_book(username):
    """
    Function to borrow a book.
    """
    global available_books
    if available_books:
        print("===== Books Available =====")
        for idx, book in enumerate(available_books, start=1):
            print(f"{idx}. {book[0]} by {book[1]}")
        print("==========================")
        choice = int(input("Enter the number of the book you want to borrow: "))
        if 1 <= choice <= len(available_books):
            selected_book = available_books.pop(choice - 1)
            save_data(file_path)
            current_time = datetime.datetime.now()
            borrow_date = current_time.date()
            borrow_time = current_time.time()
            borrow_day = borrow_date.strftime("%A")
            with open(borrow_book_file, "a") as file:
                file.write(f"{username},{selected_book[0]},{selected_book[1]},{borrow_date},{borrow_time},{borrow_day}\n")
            print(f"{selected_book[0]} by {selected_book[1]} borrowed successfully!")
        else:
            print("Invalid choice!")
    else:
        print("No books available.")

# Function to return a book
def return_book(username):
    """
    Function to return a book.
    """
    with open(borrow_book_file, "r") as file:
        lines = file.readlines()

    if lines:
        print("===== Books Borrowed =====")
        for idx, line in enumerate(lines, start=1):
            data = line.strip().split(',')
            if data[0] == username:
                print(f"{idx}. {data[1]} by {data[2]}")
        print("==========================")
        choice = int(input("Enter the number of the book you want to return: "))
        if 1 <= choice <= len(lines):
            selected_book = lines[choice - 1].strip().split(',')[1:3]
            with open(borrow_book_file, "w") as file:
                for line in lines:
                    data = line.strip().split(',')
                    if data[0] != username or data[1:3] != selected_book:
                        file.write(line)
            print(f"{selected_book[0]} by {selected_book[1]} returned successfully!")
        else:
            print("Invalid choice!")
    else:
        print("No books borrowed.")

# Function to add a book
def add_book():
    """
    Function to add a book.
    """
    title = input("Enter title of the book: ")
    author = input("Enter author of the book: ")
    available_books.append((title, author))
    save_data(file_path)
    print("Book added successfully!")

# Function to remove a book
def remove_book():
    """
    Function to remove a book.
    """
    display_books()
    if available_books:
        choice = int(input("Enter the number of the book you want to remove: "))
        if 1 <= choice <= len(available_books):
            removed_book = available_books.pop(choice - 1)
            save_data(file_path)
            print(f"{removed_book[0]} by {removed_book[1]} removed successfully!")
        else:
            print("Invalid choice!")
    else:
        print("No books available to remove.")

# Function to display all available books
def display_books():
    """
    Function to display all available books.
    """
    global available_books
    if available_books:
        print("===== Books Available =====")
        for idx, book in enumerate(available_books, start=1):
            print(f"{idx}. {book[0]} by {book[1]}")
        print("==========================")
    else:
        print("No books available.")

# Function to display all borrowed books
def display_borrowed_books():
    """
    Function to display all borrowed books with usernames of borrowers.
    """
    with open(borrow_book_file, "r") as file:
        print("===== Borrowed Books =====")
        for line in file:
            data = line.strip().split(',')
            print(f"Book: {data[1]} by {data[2]} | Borrower: {data[0]}")
        print("==========================")

def admin_menu():
    """
    Function to display the admin menu.
    """
    print("Welcome, Admin!")
    while True:
        choice = display_menu_admin()
        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            display_books()
        elif choice == '4':
            display_borrowed_books()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

def display_menu_admin():
    """
    Function to display menu for admin.
    """
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Display Books")
    print("4. Display Borrowed Books")
    print("5. Exit")
    opt = input("Enter your choice: ")
    return opt 


def main():
    """
    Function to start the library management system.
    """
    load_data(file_path)
    print("Welcome to the Library Management System!")
    print("Are you a Student or an Admin?")
    role = input("Enter 'S' for Student or 'A' for Admin: ")
    if role.lower() == 's':
        print("Do you want to login or signup?")
        option = input("Enter 'L' for Login or 'S' for Signup: ")
        if option.lower() == 'l':
            username = login(read_login_credentials(login_cred))
        elif option.lower() == 's':
            signup()
            username = login(read_login_credentials(login_cred))
        else:
            print("Invalid option! Please enter 'L' or 'S'.")
            return
        borrow_book(username)
    elif role.lower() == 'a':
        username = admin_login()
        admin_menu()
    else:
        print("Invalid choice! Please enter 'S' or 'A'.")

if __name__ == "__main__":
    main()
