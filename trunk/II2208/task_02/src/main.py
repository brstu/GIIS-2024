from PyQt6.QtWidgets import QPushButton, QFileDialog, QListWidget, QApplication, QMainWindow, QLabel, QLineEdit, QGridLayout, QWidget
from PyQt6.QtGui import QIcon

import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.contacts = []
        self.setWindowTitle("Contacts")
        self.setWindowIcon(QIcon("icon.ico"))
        self.layout = QGridLayout()
        self.label_name = QLabel("Name:")
        self.label_name.setFixedWidth(60)
        self.label_address = QLabel("Address:")
        self.label_address.setFixedWidth(60)
        self.input_name = QLineEdit()
        self.input_name.textChanged.connect(self.on_text_changed)
        self.input_address = QLineEdit()
        self.input_address.textChanged.connect(self.on_text_changed)
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_contact)
        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.edit_contact)
        self.button_remove = QPushButton("Remove")
        self.button_remove.clicked.connect(self.remove_contact)
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_contacts)
        self.button_load = QPushButton("Load")
        self.button_load.clicked.connect(self.load_contacts)
        self.button_export = QPushButton("Export")
        self.button_export.clicked.connect(self.export_contacts)
        self.list = QListWidget()
        self.list.itemClicked.connect(self.select_contact)
        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.input_name, 0, 1)
        self.layout.addWidget(self.label_address, 1, 0)
        self.layout.addWidget(self.input_address, 1, 1)
        self.layout.addWidget(self.button_add, 2, 0)
        self.layout.addWidget(self.button_edit, 3, 0)
        self.layout.addWidget(self.button_remove, 4, 0)
        self.layout.addWidget(self.button_save, 5, 0)
        self.layout.addWidget(self.button_load, 6, 0)
        self.layout.addWidget(self.button_export, 7, 0)
        self.layout.addWidget(self.list, 2, 1, 6, 1)
        self.setLayout(self.layout)
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def on_text_changed(self):
        name = self.input_name.text()
        address = self.input_address.text()
        self.list.clear()
        for i in self.contacts:
            if name == "" and address == "":
                self.list.addItem(f"{self.contacts[i]['name']} - {self.contacts[i]['address']}")
            elif name in self.contacts[i]["name"] and address in self.contacts[i]["address"]:
                self.list.addItem(f"{self.contacts[i]['name']} - {self.contacts[i]['address']}")

    def add_contact(self):
        name = self.input_name.text()
        address = self.input_address.text()

        if name and address:
            contact = {"name": name, "address": address}
            self.contacts.append(contact)
            self.list.addItem(f"{name} - {address}")
            self.clear_fields()

    def edit_contact(self):
        selected_item = self.list.currentItem()
        if selected_item:
            index = self.list.row(selected_item)
            self.contacts[index] = {"name": self.input_name.text(), "address": self.input_address.text()}
            self.list.currentItem().setText(f"{self.input_name.text()} - {self.input_address.text()}")
            self.clear_fields()

    def remove_contact(self):
        selected_item = self.list.currentItem()
        if selected_item:
            index = self.list.row(selected_item)
            del self.contacts[index]
            self.list.takeItem(index)
            self.clear_fields()

    def clear_fields(self):
        self.input_name.clear()
        self.input_address.clear()

    def save_contacts(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save to", "contacts.cntcts", "(*.cntcts)"
        )
        if filename:
            try:
                with open(filename, "w") as file:
                    import json

                    json.dump(self.contacts, file, indent=4)
                print("Contacts are saved perfectly!")
            except Exception as e:
                print(f"Error while saving: {e}")

    def load_contacts(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load from", "", "(*.cntcts)"
        )
        if filename:
            try:
                with open(filename, "r") as file:
                    import json

                    self.contacts = json.load(file)
                    self.list.clear()
                    for contact in self.contacts:
                        self.list.addItem(f"{contact['name']} - {contact['address']}")
                print("Contacts are loaded perfectly!")
            except FileNotFoundError:
                print("Contact's file wasn't found.")
            except Exception as e:
                print(f"Error while loading: {e}")

    def export_contacts(self):
        selected_item = self.list.currentItem()
        if selected_item:
            index = self.list.row(selected_item)
            name = self.contacts[index]["name"]
            address = self.contacts[index]["address"]

            fileName, _ = QFileDialog.getSaveFileName(
                self, "Export vCard", str(name) + ".vcf", "vCard (*.vcf)"
            )

            if fileName:
                with open(fileName, "w") as file:
                    file.write("BEGIN:VCARD\n")
                    file.write("VERSION:3.0\n")
                    file.write("N:;;;;\n")
                    file.write(f"FN:{name}\n")
                    file.write(f"ADR:{address}\n")
                    file.write("END:VCARD\n")
                print("vCard created!")

    def select_contact(self):
        selected_item = self.list.currentItem()
        if selected_item:
            index = self.list.row(selected_item)
            name, address = self.contacts[index]["name"], self.contacts[index]["address"]
            self.input_name.setText(name)
            self.input_address.setText(address)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()