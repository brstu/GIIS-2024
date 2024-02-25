class AdressBook:

    book: dict
    current_adress: str = ""

    def __init__(self):
        self.book = {}

    def add(self, name: str, adress: str) -> None:
        self.book[name] = adress
        self.current_adress = name

    def delete(self) -> None:
        if self.current_adress != "":
            deleted_name = self.current_adress
            self.prev()
            if deleted_name == self.current_adress:
                self.current_adress = ""
            del self.book[deleted_name]

    def get_current(self) -> tuple | None:
        if self.current_adress == "":
            return None
        return self.current_adress, self.book[self.current_adress]

    def prev(self) -> None:
        for index, key in enumerate(self.book.keys()):
            if key == self.current_adress:
                self.current_adress = list(self.book.keys())[(index-1) % len(self.book.keys())]
                break

    def next(self) -> None:
        for index, key in enumerate(self.book.keys()):
            if key == self.current_adress:
                self.current_adress = list(self.book.keys())[(index+1) % len(self.book.keys())]
                break

    def save(self, path: str) -> None:
        try:
            file = open(path, "w")
            counter = 0
            for key, value in self.book.items():
                counter += 1
                file.write(f"{key}:{value}{"\n" if counter != len(self.book.items()) else ""}")
            file.close()
        except Exception as e:
            print(e)

    def read(self, path: str) -> None:
        try:
            file = open(path, "r")
            data = file.read().split('\n')
            for record in data:
                line_data = record.split(':')
                self.book[line_data[0]] = line_data[1]
                if self.current_adress == "":
                    self.current_adress = line_data[0]
            file.close()
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(e)

    def edit(self, old_record: tuple, new_record: tuple) -> None:
        if old_record in self.book.items() and new_record not in self.book.items():
            self.book.pop(old_record[0])
            self.book[new_record[0]] = new_record[1]
            if self.current_adress == old_record[0]:
                self.current_adress = new_record[0]
