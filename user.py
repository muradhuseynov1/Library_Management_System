import hashlib

MAX_BORROWED_BOOKS = 3

class User:
    def __init__(self, name, role='regular'):
        self.name = name
        #self.user_id = user_id
        self.borrowed_books = []
        self.role = role # 'admin' or 'regular'
        self.password_hash = None

    def borrow_book(self, book):
        if len(self.borrowed_books) < MAX_BORROWED_BOOKS:
            if book.status == "available":
                book.borrow()
                self.borrowed_books.append(book)
                print(f"{self.name} has borrowed '{book.title}'. Due date: {book.due_date.strftime('%Y-%m-%d')}")
            else:
                print(f"{book.title} is not available for borrowing.")
        else:
            print(f"{self.name} has reached the maximum limit of borrowed books.")
        

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            print(f"{self.name} has returned '{book.title}'.")
        else:
            print(f"{self.name} did not borrow '{book.title}'.")

    def set_password(self, password):
        salted_pw = password + "somesalt"
        self.password_hash = hashlib.sha256(salted_pw.encode()).hexdigest()

    def check_password(self, password):
        salted_pw = password + "somesalt"
        return self.password_hash == hashlib.sha256(salted_pw.encode()).hexdigest()