from PyQt6.QtWidgets import QPushButton, QFileDialog, QListWidget, QApplication, QMainWindow, QLabel, QLineEdit, \
    QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import sys


class MainAppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.entries = []
        self.setWindowTitle("Entries")
        self.setWindowIcon(QIcon("icon.ico"))

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Title:"))
        self.input_title = QLineEdit()
        input_layout.addWidget(self.input_title)

        input_layout.addWidget(QLabel("Content:"))
        self.input_content = QLineEdit()
        input_layout.addWidget(self.input_content)

        button_layout = QHBoxLayout()
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_entry)
        button_layout.addWidget(self.button_add)

        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.edit_entry)
        button_layout.addWidget(self.button_edit)

        self.button_remove = QPushButton("Remove")
        self.button_remove.clicked.connect(self.remove_entry)
        button_layout.addWidget(self.button_remove)

        self.button_find = QPushButton("Find")
        self.button_find.clicked.connect(self.find_entry)
        button_layout.addWidget(self.button_find)

        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_entries)
        button_layout.addWidget(self.button_save)

        self.button_load = QPushButton("Load")
        self.button_load.clicked.connect(self.load_entries)
        button_layout.addWidget(self.button_load)

        self.button_export = QPushButton("Export")
        self.button_export.clicked.connect(self.export_entries)
        button_layout.addWidget(self.button_export)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)

        self.list = QListWidget()
        main_layout.addWidget(self.list)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def find_entry(self):
        title = self.input_title.text()
        content = self.input_content.text()
        self.list.clear()
        for entry in self.entries:
            if title.lower() in entry["title"].lower() and content.lower() in entry["content"].lower():
                self.list.addItem(f"{entry['title']} - {entry['content']}")

    def add_entry(self):
        title = self.input_title.text()
        content = self.input_content.text()
        if title and content:
            entry = {"title": title, "content": content}
            self.entries.append(entry)
            self.list.addItem(f"{title} - {content}")
            self.clear_fields()

    def edit_entry(self):
        selected_row = self.list.currentRow()
        if selected_row != -1:
            title = self.input_title.text()
            content = self.input_content.text()
            if title and content:
                entry = {"title": title, "content": content}
                self.entries[selected_row] = entry
                self.list.currentItem().setText(f"{title} - {content}")
                self.clear_fields()

    def remove_entry(self):
        selected_row = self.list.currentRow()
        if selected_row != -1:
            del self.entries[selected_row]
            self.list.takeItem(selected_row)
            self.clear_fields()

    def clear_fields(self):
        self.input_title.clear()
        self.input_content.clear()

    def save_entries(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save to", "entries.ent", "(*.ent)"
        )
        if filename:
            try:
                with open(filename, "w") as file:
                    import json
                    json.dump(self.entries, file, indent=4)
                print("Entries are saved perfectly!")
            except Exception as e:
                print(f"Error while saving: {e}")

    def load_entries(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load from", "", "(*.ent)"
        )
        if filename:
            try:
                with open(filename, "r") as file:
                    import json
                    self.entries = json.load(file)
                    self.list.clear()
                    for entry in self.entries:
                        self.list.addItem(f"{entry['title']} - {entry['content']}")
                print("Entries are loaded perfectly!")
            except FileNotFoundError:
                print("Entry file wasn't found.")
            except Exception as e:
                print(f"Error while loading: {e}")

    def export_entries(self):
        selected_row = self.list.currentRow()
        if selected_row != -1:
            entry = self.entries[selected_row]
            title = entry["title"]
            content = entry["content"]
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Export Text", f"{title}.txt", "Text files (*.txt)"
            )
            if file_name:
                with open(file_name, "w") as file:
                    file.write(f"Title: {title}\n")
                    file.write(f"Content: {content}\n")
                print("Text file created!")


app = QApplication(sys.argv)

window = MainAppWindow()
window.show()

sys.exit(app.exec())
