import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog


class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.addresses = []  # Список для хранения адресов
        self.current_index = -1  # Индекс текущего адреса
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Адресная книга')

        # Создание меток и полей ввода для имени и адреса
        self.name_label = QLabel('Имя:')
        self.name_edit = QLineEdit()
        self.address_label = QLabel('Адрес:')
        self.address_edit = QLineEdit()

        # Создание кнопок для добавления адреса, редактирования, удаления адреса, поиска, предыдущего и следующего адресов
        self.add_button = QPushButton('Добавить адрес')
        self.add_button.clicked.connect(self.addAddress)

        self.edit_button = QPushButton('Редактировать')
        self.edit_button.clicked.connect(self.editAddress)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.deleteAddress)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.saveData)

        self.load_button = QPushButton('Загрузить')
        self.load_button.clicked.connect(self.loadData)

        self.clear_button = QPushButton('Очистить')
        self.clear_button.clicked.connect(self.clearFields)

        self.prev_button = QPushButton('Предыдущий')
        self.prev_button.clicked.connect(self.showPreviousAddress)

        self.next_button = QPushButton('Следующий')
        self.next_button.clicked.connect(self.showNextAddress)

        # Создание макета сетки и добавление в него виджетов
        layout = QGridLayout()
        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(self.address_label, 1, 0)
        layout.addWidget(self.address_edit, 1, 1)
        layout.addWidget(self.add_button, 0, 2)
        layout.addWidget(self.edit_button, 1, 2)
        layout.addWidget(self.delete_button, 2, 2)
        layout.addWidget(self.save_button, 3, 2)
        layout.addWidget(self.load_button, 4, 2)
        layout.addWidget(self.clear_button, 5, 2)
        layout.addWidget(self.prev_button, 6, 0)
        layout.addWidget(self.next_button, 6, 1)

        layout.setHorizontalSpacing(10)  # Устанавливаем горизонтальное расстояние между столбцами

        self.setLayout(layout)

    def addAddress(self):
        name = self.name_edit.text()
        address = self.address_edit.text()
        if name and address:
            self.addresses.append((name, address))  # Добавляем новый адрес в список
            self.current_index = len(self.addresses) - 1  # Устанавливаем текущий индекс на новый адрес
            print(f'Добавлен адрес: {name}: {address}')
        else:
            QMessageBox.warning(self, 'Пустые поля', 'Введите имя и адрес!')

    def editAddress(self):
        name = self.name_edit.text()
        address = self.address_edit.text()
        if name and address and self.current_index >= 0 and self.current_index < len(self.addresses):
            self.addresses[self.current_index] = (name, address)
            print(f'Адрес отредактирован: {name}: {address}')
        else:
            QMessageBox.warning(self, 'Некорректные данные', 'Некорректные данные для редактирования адреса')

    def deleteAddress(self):
        if self.current_index >= 0 and self.current_index < len(self.addresses):
            confirm = QMessageBox.question(self, 'Подтверждение удаления', 'Вы уверены, что хотите удалить адрес?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                del self.addresses[self.current_index]
                if self.current_index > 0:
                    self.current_index -= 1  # Переходим к предыдущему адресу после удаления текущего
                print('Адрес удален')
        else:
            QMessageBox.warning(self, 'Нет адреса', 'Нет адреса для удаления')

    def saveData(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Text files (*.txt)')  # Изменение фильтра на .txt
        if file_name:
            with open(file_name, 'w') as file:
                for name, address in self.addresses:
                    file.write(f'{name}:{address}\n')
            print('Данные сохранены')

    def loadData(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'Text files (*.txt)')  # Изменение фильтра на .txt
        if file_name:
            with open(file_name, 'r') as file:
                self.addresses = []
                for line in file:
                    name, address = line.strip().split(':')
                    self.addresses.append((name, address))
        print('Данные загружены')
        self.current_index = -1  # Сброс текущего индекса после загрузки новых данных
        self.showNextAddress()  # Показать первый адрес после загрузки данных

    def clearFields(self):
        self.name_edit.clear()
        self.address_edit.clear()

    def showPreviousAddress(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.showAddress()

    def showNextAddress(self):
        if self.current_index < len(self.addresses) - 1:
            self.current_index += 1
            self.showAddress()

    def showAddress(self):
        if self.current_index >= 0 and self.current_index < len(self.addresses):
            name, address = self.addresses[self.current_index]
            self.name_edit.setText(name)
            self.address_edit.setText(address)
        else:
            print('Нет адресов для отображения')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    address_book = AddressBook()
    address_book.show()
    sys.exit(app.exec_())
