import json

class Settings:
    def __init__(self):
        self.max_books_borrowed = 5
        self.due_duration_days = 14

    def load_from_file(self, filename='settings.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.max_books_borrowed = data['max_books_borrowed']
            self.due_duration_days = data['due_duration_days']

    def save_to_file(self, filename='settings.json'):
        with open(filename, 'w') as file:
            data = {
                'max_books_borrowed': self.max_books_borrowed,
                'due_duration_days': self.due_duration_days
            }
            json.dump(data, file)