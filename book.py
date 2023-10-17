from datetime import datetime, timedelta

DUE_DAYS = 7

class Book: 
    def __init__(self, title, author, ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.status = "available"
        self.due_date = None

    def borrow(self):
        if self.status == "available":
            self.status = "borrowed"
            self.due_date = datetime.now() + timedelta(days=DUE_DAYS)
        else:
            print(f"The book '{self.title}' is already borrowed.")

    def return_book(self):
        if self.is_overdue():
            print(f"The book '{self.tite}' is overdue!")
        self.status = "available"
        self.due_date = None

    def is_overdue(self):
        return datetime.now() > self.due_date if self.due_date else False