import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QFileDialog, QListWidget, QListWidgetItem, QScrollArea


class ContactDataManager:
    def __init__(self):
        self.contacts = []
        self.current_index = -1

    def add_contact(self, name, address):
        if name and address:
            self.contacts.append((name, address))
            self.current_index = len(self.contacts) - 1
            print(f'Added contact: {name}: {address}')
            return True
        else:
            QMessageBox.warning(None, 'Empty Fields', 'Please enter name and address!')
            return False

    def edit_contact(self, index, name, address):
        if name and address and 0 <= index < len(self.contacts):
            self.contacts[index] = (name, address)
            print(f'Contact edited: {name}: {address}')
            return True
        else:
            print('Error editing contact: invalid index or data')
            return False

    def delete_contact(self):
        if 0 <= self.current_index < len(self.contacts):
            confirm = QMessageBox.question(None, 'Delete Confirmation', 'Are you sure you want to delete the contact?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                del self.contacts[self.current_index]
                if self.current_index > 0:
                    self.current_index -= 1
                print('Contact deleted')
                return True
        else:
            QMessageBox.warning(None, 'No Contact', 'No contact to delete!')
            return False

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(None, 'Save File', '', 'Text files (*.txt)')
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    for index, (name, address) in enumerate(self.contacts, 1):
                        file.write(f'№{index}. {name}: {address}\n')  # Сохраняем контакты в новом формате
                print('Data saved')
                return True
            except Exception as e:
                print(f'Error saving data: {e}')
                QMessageBox.warning(None, 'Error', f'Error saving data: {e}')
        return False

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select File', '', 'Text files (*.txt)')
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.contacts = []
                    for line in file:
                        if line.startswith('№'):
                            parts = line.strip().split(':')
                            if len(parts) == 2:
                                name = parts[0].split('. ')[1].strip()  # Получаем имя контакта
                                address = parts[1].strip()  # Получаем адрес контакта
                                self.contacts.append((name, address))
                            else:
                                print(f'Ignoring malformed line: {line}')  # Если строка содержит не два значения, игнорируем её
                    print('Data loaded')
                    if self.contacts:
                        self.current_index = 0
                    return True
            except Exception as e:
                print(f'Error loading data: {e}')
                QMessageBox.warning(None, 'Error', f'Error loading data: {e}')
        return False

    def get_contact(self, index):
        return self.contacts[index] if 0 <= index < len(self.contacts) else None


class ContactManagerUI(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 300)
        main_layout = QHBoxLayout()

        # Left panel for adding/editing contacts
        left_layout = QVBoxLayout()

        self.name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        self.address_label = QLabel('Address:')
        self.address_input = QLineEdit()

        self.add_button = QPushButton('Add Contact')
        self.add_button.clicked.connect(self.add_contact)

        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_contact)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_contact)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_data)

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_data)

        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.name_input)
        left_layout.addWidget(self.address_label)
        left_layout.addWidget(self.address_input)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.edit_button)
        left_layout.addWidget(self.delete_button)
        left_layout.addWidget(self.save_button)
        left_layout.addWidget(self.load_button)

        # Right panel for displaying all contacts
        right_layout = QVBoxLayout()

        self.contacts_list_widget = QListWidget()
        self.contacts_list_widget.itemClicked.connect(self.select_contact)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.contacts_list_widget)

        right_layout.addWidget(QLabel('All Contacts:'))
        right_layout.addWidget(scroll_area)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.populate_contacts_list()

    def populate_contacts_list(self):
        self.contacts_list_widget.clear()
        for name, address in self.data_manager.contacts:
            item = QListWidgetItem(f'{name}: {address}')
            self.contacts_list_widget.addItem(item)

    def add_contact(self):
        name = self.name_input.text()
        address = self.address_input.text()
        if self.data_manager.add_contact(name, address):
            self.populate_contacts_list()
            self.clear_fields()

    def edit_contact(self):
        name = self.name_input.text()
        address = self.address_input.text()
        if self.data_manager.edit_contact(self.data_manager.current_index, name, address):
            self.populate_contacts_list()
            self.clear_fields()

    def delete_contact(self):
        if self.data_manager.delete_contact():
            self.populate_contacts_list()
            self.clear_fields()

    def save_data(self):
        self.data_manager.save_data()

    def load_data(self):
        if self.data_manager.load_data():
            self.populate_contacts_list()

    def clear_fields(self):
        self.name_input.clear()
        self.address_input.clear()

    def select_contact(self, item):
        index = self.contacts_list_widget.row(item)
        contact = self.data_manager.get_contact(index)
        if contact:
            self.data_manager.current_index = index  # Обновляем текущий индекс
            self.name_input.setText(contact[0])
            self.address_input.setText(contact[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_manager = ContactDataManager()
    contact_manager_ui = ContactManagerUI(data_manager)
    contact_manager_ui.show()
    sys.exit(app.exec_())
