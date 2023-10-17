import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from book import Book
from user import User
from library import Library

class LibraryApp:

    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.admin_functions = []

        self.build_gui()

    def build_gui(self):
        self.root.geometry("800x600")
        
        # Title
        tk.Label(self.root, text="Library Management System", font=("Arial", 16)).grid(row=0, column=1, pady=20)

        # Frame for Book List
        book_frame = tk.Frame(self.root)
        book_frame.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="ns")

        scrollbar = tk.Scrollbar(book_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.books_listbox = tk.Listbox(book_frame, yscrollcommand=scrollbar.set, height=20, width=50)
        self.books_listbox.bind('<<ListboxSelect>>', self.display_book_details)
        self.books_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.books_listbox.yview)

        self.update_books_listbox()

        # Frame for Book Details
        details_frame = tk.Frame(self.root)
        details_frame.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(details_frame, text="Book Details", font=("Arial", 14)).pack()
        self.book_details_var = tk.StringVar()
        self.book_details_label = tk.Label(details_frame, textvariable=self.book_details_var, font=("Arial", 12))
        self.book_details_label.pack(pady=10)

        # Dropdown for users
        self.user_var = tk.StringVar()
        self.users_dropdown = ttk.Combobox(self.root, textvariable=self.user_var, width=40)
        self.users_dropdown.grid(row=2, column=1, padx=20, pady=20)
        self.update_users_dropdown()

        # Login Frame
        login_frame = tk.Frame(self.root)
        login_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Button(login_frame, text="Register", command=self.show_registration_form).grid(row=3, column=0, columnspan=2)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(login_frame, text="Username:").grid(row=0, column=0)
        tk.Entry(login_frame, textvariable=self.username_var).grid(row=0, column=1)

        tk.Label(login_frame, text="Password:").grid(row=1, column=0)
        tk.Entry(login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)

        tk.Button(login_frame, text="Login", command=self.authenticate_user).grid(row=2, column=0, columnspan=2)


        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=3, column=1, padx=20, pady=20)

        self.add_book_button = tk.Button(button_frame, text="Add Book", command=self.add_book)
        self.add_book_button.grid(row=0, column=0, padx=10, pady=10)

        self.remove_book_button = tk.Button(button_frame, text="Remove Book", command=self.remove_book)
        self.remove_book_button.grid(row=4, column=0, padx=10, pady=10)

        self.remove_user_button = tk.Button(button_frame, text="Remove User", command=self.remove_user)
        self.remove_user_button.grid(row=4, column=1, padx=10, pady=10)

        self.save_data_button = tk.Button(button_frame, text="Save Data", command=self.save_data)
        self.save_data_button.grid(row=3, column=0, padx=10, pady=10)

        self.load_data_button = tk.Button(button_frame, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=3, column=1, padx=10, pady=10)

        # Add Book Button
        #tk.Button(button_frame, text="Add Book", command=self.add_book).grid(row=0, column=0, padx=10, pady=10)

        # Borrow Book Button
        tk.Button(button_frame, text="Borrow Book", command=self.borrow_book).grid(row=1, column=0, padx=10, pady=10)

        # Return Book Button
        tk.Button(button_frame, text="Return Book", command=self.return_book).grid(row=1, column=1, padx=10, pady=10)

        # Search by Title Button
        tk.Button(button_frame, text="Search by Title", command=self.search_by_title).grid(row=2, column=0, padx=10, pady=10)

        # Search by Author Button
        tk.Button(button_frame, text="Search by Author", command=self.search_by_author).grid(row=2, column=1, padx=10, pady=10)

        #tk.Button(button_frame, text="Remove Book", command=self.remove_book).grid(row=4, column=0, padx=10, pady=10)

        #tk.Button(button_frame, text="Remove User", command=self.remove_user).grid(row=4, column=1, padx=10, pady=10)

        # Save Data Button
        #tk.Button(button_frame, text="Save Data", command=self.save_data).grid(row=3, column=0, padx=10, pady=10)

        # Load Data Button
        #tk.Button(button_frame, text="Load Data", command=self.load_data).grid(row=3, column=1, padx=10, pady=10)

        # Exit Button
        tk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to the Library Management System!")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="we")

        self.toggle_admin_functions(show=False)


    def display_book_details(self, evt):
        selected_index = self.books_listbox.curselection()
        if selected_index:
            selected_book = self.library.books[selected_index[0]]
            details = f"Title: {selected_book.title}\nAuthor: {selected_book.author}\nISBN: {selected_book.ISBN}"
            self.book_details_var.set(details)

    def update_books_listbox(self):
        self.books_listbox.delete(0, tk.END)
        for book in self.library.books:
            self.books_listbox.insert(tk.END, book.title)

    def update_users_dropdown(self):
        self.users_dropdown['values'] = [user.name for user in self.library.users]

    def create_buttons(self):
        tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=10)
        tk.Button(self.root, text="Register User", command=self.register_user).pack(pady=10)
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self.root, text="Remove Book", command=self.remove_book).pack(pady=10)
        tk.Button(self.root, text="Remove User", command=self.remove_user).pack(pady=10)
        tk.Button(self.root, text="Search by Title", command=self.search_by_title).pack(pady=10)
        tk.Button(self.root, text="Search by Author", command=self.search_by_author).pack(pady=10)
        tk.Button(self.root, text="Save Data", command=self.save_data).pack(pady=10)
        tk.Button(self.root, text="Load Data", command=self.load_data).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def add_book(self):
        title = simpledialog.askstring("Input", "Enter book title:")
        author = simpledialog.askstring("Input", "Enter book author:")
        ISBN = simpledialog.askstring("Input", "Enter book ISBN:")

        if title and author and ISBN:
            book = Book(title, author, ISBN)
            self.library.add_book(book)
            self.update_books_listbox()
            self.status_var.set(f"Book '{title}' added successfully!")

    def borrow_book(self):
        user_name = simpledialog.askstring("Input", "Enter user name:")
        book_title = simpledialog.askstring("Input", "Enter book title:")

        user = self.library.find_user_by_name(user_name)
        book = self.library.find_book_by_title(book_title)

        if user and book:
            user.borrow_book(book)
        else:
            messagebox.showerror("Error", "User or Book not found.")

    def return_book(self):
        user_name = simpledialog.askstring("Input", "Enter user name:")
        book_title = simpledialog.askstring("Input", "Enter book title:")

        user = self.library.find_user_by_name(user_name)
        book = self.library.find_book_by_title(book_title)

        if user and book:
            user.return_book(book)
        else:
            messagebox.showerror("Error", "User or Book not found.")

    def remove_book(self):
        selected_index = self.books_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select a book to remove.")
            return
        
        selected_book = self.library.books[selected_index[0]]
        if messagebox.askyesno("Confirmation", f"Do you want to remove the book '{selected_book.title}'?"):
            self.library.books.remove(selected_book)
            self.update_books_listbox()
            self.status_var.set(f"Book '{selected_book.title}' removed successfully!")
        else:
            self.status_var.set("Book removal cancelled.")

    def remove_user(self):
        selected_user_name = self.user_var.get()
        if not selected_user_name:
            messagebox.showinfo("Info", "Please select a user to remove.")
            return
        
        selected_user = next((user for user in self.library.users if user.name == selected_user_name), None)
        if not selected_user:
            messagebox.showinfo("Info", "Selected user not found.")
            return
        
        if messagebox.askyesno("Confirmation", f"Do you want to remove the user '{selected_user.name}'?"):
            self.library.users.remove(selected_user)
            self.update_users_dropdown()
            self.status_var.set(f"User '{selected_user.name}' removed successfully!")
        else:
            self.status_var.set("User removal cancelled.")

    def search_by_title(self):
        title = simpledialog.askstring("Input", "Enter title keyword:")
        books = self.library.search_books_by_title(title)

        if books:
            book_titles = "\n".join([book.title for book in books])
            messagebox.showinfo("Books Found", book_titles)
        else:
            messagebox.showinfo("Info", "No books found.")

    def search_by_author(self):
        author = simpledialog.askstring("Input", "Enter author keyword:")
        books = self.library.search_books_by_author(author)

        if books:
            book_titles = "\n".join([book.title for book in books])
            messagebox.showinfo("Books Found", book_titles)
        else:
            messagebox.showinfo("Info", "No books found.")

    def save_data(self):
        self.library.save_data()
        messagebox.showinfo("Info", "Data saved successfully!")

    def load_data(self):
        self.library.load_data()
        messagebox.showinfo("Info", "Data loaded successfully!")

    def authenticate_user(self):
        username = self.username_var.get()
        password = self.password_var.get()

        user = next((user for user in self.library.users if user.name == username), None)
        if not user:
            messagebox.showinfo("Info", "User not found.")
            return

        if user.check_password(password):
            self.current_user = user
            if user.role == "admin":
                self.toggle_admin_functions(show=True)
            else:
                self.toggle_admin_functions(show=False)
        else:
            messagebox.showinfo("Info", "Incorrect password.")

    def show_registration_form(self):
        # Create a new top-level window for registration
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register New User")

        tk.Label(self.register_window, text="Username:").grid(row=0, column=0)
        self.register_username_var = tk.StringVar()
        tk.Entry(self.register_window, textvariable=self.register_username_var).grid(row=0, column=1)

        tk.Label(self.register_window, text="Password:").grid(row=1, column=0)
        self.register_password_var = tk.StringVar()
        tk.Entry(self.register_window, textvariable=self.register_password_var, show="*").grid(row=1, column=1)

        tk.Label(self.register_window, text="Role:").grid(row=2, column=0)
        self.register_role_var = tk.StringVar(value="regular")  # default to 'regular'
        tk.OptionMenu(self.register_window, self.register_role_var, "regular", "admin").grid(row=2, column=1)

        tk.Button(self.register_window, text="Submit", command=self.register_user).grid(row=3, column=0, columnspan=2)

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
        self.update_users_dropdown()

        # Provide feedback and close the registration window
        messagebox.showinfo("Info", "Registration successful!")
        self.register_window.destroy()

    def toggle_admin_functions(self, show=True):
        if show:
            self.add_book_button.config(state=tk.NORMAL)
            self.remove_book_button.config(state=tk.NORMAL)
            self.remove_user_button.config(state=tk.NORMAL)
            self.save_data_button.config(state=tk.NORMAL)
            self.load_data_button.config(state=tk.NORMAL)
        else:
            self.add_book_button.config(state=tk.DISABLED)
            self.remove_book_button.config(state=tk.DISABLED)
            self.remove_user_button.config(state=tk.DISABLED)
            self.save_data_button.config(state=tk.DISABLED)
            self.load_data_button.config(state=tk.DISABLED)