import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog


class ContactManager(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts_list = []
        self.current_index = -1
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Менеджер контактов')

        self.name_label = QLabel('Имя:')
        self.name_input = QLineEdit()
        self.address_label = QLabel('Адрес:')
        self.address_input = QLineEdit()

        self.add_button = QPushButton('Добавить контакт')
        self.add_button.clicked.connect(self.addContact)

        self.edit_button = QPushButton('Редактировать')
        self.edit_button.clicked.connect(self.editContact)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.deleteContact)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.saveData)

        self.load_button = QPushButton('Загрузить')
        self.load_button.clicked.connect(self.loadData)

        self.clear_button = QPushButton('Очистить')
        self.clear_button.clicked.connect(self.clearFields)

        self.prev_button = QPushButton('Предыдущий')
        self.prev_button.clicked.connect(self.showPreviousContact)

        self.next_button = QPushButton('Следующий')
        self.next_button.clicked.connect(self.showNextContact)

        layout = QGridLayout()
        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_input, 0, 1)
        layout.addWidget(self.address_label, 1, 0)
        layout.addWidget(self.address_input, 1, 1)
        layout.addWidget(self.add_button, 0, 2)
        layout.addWidget(self.edit_button, 1, 2)
        layout.addWidget(self.delete_button, 2, 2)
        layout.addWidget(self.save_button, 3, 2)
        layout.addWidget(self.load_button, 4, 2)
        layout.addWidget(self.clear_button, 5, 2)
        layout.addWidget(self.prev_button, 6, 0)
        layout.addWidget(self.next_button, 6, 1)

        layout.setHorizontalSpacing(10)

        self.setLayout(layout)

    def addContact(self):
        name = self.name_input.text()
        address = self.address_input.text()
        if name and address:
            self.contacts_list.append((name, address))
            self.current_index = len(self.contacts_list) - 1
            print(f'Добавлен контакт: {name}: {address}')
        else:
            QMessageBox.warning(self, 'Пустые поля', 'Введите имя и адрес!')

    def editContact(self):
        name = self.name_input.text()
        address = self.address_input.text()
        if name and address and self.current_index >= 0 and self.current_index < len(self.contacts_list):
            self.contacts_list[self.current_index] = (name, address)
            print(f'Контакт отредактирован: {name}: {address}')
        else:
            QMessageBox.warning(self, 'Некорректные данные', 'Некорректные данные для редактирования контакта')

    def deleteContact(self):
        if self.current_index >= 0 and self.current_index < len(self.contacts_list):
            confirm = QMessageBox.question(self, 'Подтверждение удаления', 'Вы уверены, что хотите удалить контакт?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                del self.contacts_list[self.current_index]
                if self.current_index > 0:
                    self.current_index -= 1
                print('Контакт удален')
        else:
            QMessageBox.warning(self, 'Нет контакта', 'Нет контакта для удаления')

    def saveData(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Text files (*.txt)')
        if file_name:
            with open(file_name, 'w') as file:
                for name, address in self.contacts_list:
                    file.write(f'{name}:{address}\n')
            print('Данные сохранены')

    def loadData(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'Text files (*.txt)')
        if file_name:
            with open(file_name, 'r') as file:
                self.contacts_list = []
                for line in file:
                    name, address = line.strip().split(':')
                    self.contacts_list.append((name, address))
        print('Данные загружены')
        self.current_index = -1
        self.showNextContact()

    def clearFields(self):
        self.name_input.clear()
        self.address_input.clear()

    def showPreviousContact(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.showContact()

    def showNextContact(self):
        if self.current_index < len(self.contacts_list) - 1:
            self.current_index += 1
            self.showContact()

    def showContact(self):
        if self.current_index >= 0 and self.current_index < len(self.contacts_list):
            name, address = self.contacts_list[self.current_index]
            self.name_input.setText(name)
            self.address_input.setText(address)
        else:
            print('Нет контактов для отображения')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    contact_manager = ContactManager()
    contact_manager.show()
    sys.exit(app.exec_())
