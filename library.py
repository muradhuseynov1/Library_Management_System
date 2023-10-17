import json
from tkinter import messagebox
from book import Book
from user import User
from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)
        print(f"'{book.title}' added to the library.")

    def add_user(self, user):
        self.users.append(user)
        print(f"User {user.name} added to the library system.")

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None
    
    def find_user_by_name(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None
    
    def search_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def search_books_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def save_data(self):
        with open("library_data.json", "w") as file:
            data = {
                "books": [{"title": book.title, "author": book.author, "ISBN": book.ISBN, "status": book.status, "due_date": book.due_date.strftime('%Y-%m-%d') if book.due_date else None} for book in self.books],
                "users": [{"name": user.name, "role": user.role, "borrowed_books": [book.title for book in user.borrowed_books]} for user in self.users]
            }
            json.dump(data, file)

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                self.books = [Book(b["title"], b["author"], b["ISBN"]) for b in data["books"]]
                self.users = [User(u["name"], u["user_id"]) for u in data["users"]]
                for b_data, book in zip(data["books"], self.books):
                    if b_data["status"] == "borrowed":
                        book.borrow()
                        if b_data["due_date"]:
                            book.due_date = datetime.strptime(b_data["due_date"], '%Y-%m-%d')
                for u_data, user in zip(data["users"], self.users):
                    user.borrowed_books = [self.find_book_by_title(title) for title in u_data["borrowed_books"]]
        except FileNotFoundError:
            print("No data file found. Starting with a fresh library system.")

    def register_user(self):
        # Get values from the registration form
        username = self.register_username_var.get()
        password = self.register_password_var.get()
        role = self.register_role_var.get()

        # Check if user already exists
        if any(user.name == username for user in self.library.users):
            messagebox.showinfo("Info", "User already exists!")
            return

        # Create a new user and add it to the library
        new_user = User(username, role)
        new_user.set_password(password)
        self.library.users.append(new_user)

        # Persist the new user to JSON
        self.library.save_data()  # <-- This is the corrected line

        # Provide feedback and close the registration window
        messagebox.showinfo("Info", "Registration successful!")
        self.register_window.destroy()

