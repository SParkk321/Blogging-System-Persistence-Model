from datetime import datetime

class Post:

    def __init__(self, code: int, title: str, text: str):
        self.code = code
        self.title = title
        self.text = text
        self.creation = datetime.now()
        self.update = datetime.now()

    def __repr__(self):
        return f"Post({self.code}, {self.title}, {self.text}, {self.creation}, {self.update})"

    def __str__(self):
        return f"Code: {self.code}\nTitle: {self.title}\nText: {self.text}\nPosted: {self.creation}\nLast Updated: {self.update}"

    def __eq__(self, other):
        return self.code == other.code and self.title == other.title and self.text == other.text

    def update_post(self, new_title, new_text):
        self.title = new_title
        self.text = new_text
        self.update = datetime.now()