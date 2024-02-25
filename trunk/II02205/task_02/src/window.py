from PySide6 import QtWidgets
from adress_book import AdressBook


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # windows settings
        self.setWindowTitle("Адресная книга")
        self.resize(600, 300)

        self.grid_layout = QtWidgets.QGridLayout()

        # inputs
        self.name_input = QtWidgets.QLineEdit()
        self.adress_input = QtWidgets.QTextEdit()
        self.name_input.setEnabled(False)
        self.adress_input.setEnabled(False)

        # buttons
        self.prev_button = QtWidgets.QPushButton("Предыдущий")
        self.next_button = QtWidgets.QPushButton("Следуюший")

        self.add_button = QtWidgets.QPushButton("Создать")
        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.delete_button = QtWidgets.QPushButton("Удалить")
        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.open_button = QtWidgets.QPushButton("Открыть")

        # button's bars
        self.bottom_button_bar = QtWidgets.QHBoxLayout()
        self.right_button_bar = QtWidgets.QVBoxLayout()
        self.bottom_button_bar_widget = QtWidgets.QWidget()
        self.right_button_bar_widget = QtWidgets.QWidget()

        self.bottom_button_bar_widget.setLayout(self.bottom_button_bar)
        self.right_button_bar_widget.setLayout(self.right_button_bar)

        # button's bars add buttons
        self.bottom_button_bar.addWidget(self.prev_button)
        self.bottom_button_bar.addWidget(self.next_button)

        self.right_button_bar.addWidget(self.add_button)
        self.right_button_bar.addWidget(self.edit_button)
        self.right_button_bar.addWidget(self.delete_button)
        self.right_button_bar.addWidget(self.save_button)
        self.right_button_bar.addWidget(self.open_button)

        self.grid_layout.addWidget(QtWidgets.QLabel("Имя"), 0, 0)
        self.grid_layout.addWidget(self.name_input, 0, 1)
        self.grid_layout.addWidget(QtWidgets.QLabel("Адрес"), 1, 0)
        self.grid_layout.addWidget(self.adress_input, 1, 1)
        self.grid_layout.addWidget(self.right_button_bar_widget, 1, 2)
        self.grid_layout.addWidget(self.bottom_button_bar_widget, 2, 1)

        # button's handler
        self.add_button.clicked.connect(self.add_button_click)
        self.save_button.clicked.connect(self.save_button_click)
        self.open_button.clicked.connect(self.open_button_click)
        self.edit_button.clicked.connect(self.edit_button_click)
        self.next_button.clicked.connect(self.next_button_click)
        self.prev_button.clicked.connect(self.prev_button_click)
        self.delete_button.clicked.connect(self.delete_button_click)

        # add grid to a layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)

        self.adress_book = AdressBook()

    def next_button_click(self) -> None:
        self.adress_book.next()
        self.set_current_data_to_inputs()

    def prev_button_click(self) -> None:
        self.adress_book.prev()
        self.set_current_data_to_inputs()

    is_editing_mode_enabled: bool = False
    data_before_edit: tuple = ()

    def edit_button_click(self) -> None:
        if not self.is_editing_mode_enabled:
            self.is_editing_mode_enabled = True
            self.button_enabled("edit")
            self.name_input.setEnabled(True)
            self.adress_input.setEnabled(True)
            self.name_input.setFocus()
            data = self.adress_book.get_current()
            if data is None:
                data = ("", "")
            self.data_before_edit = (data[0], data[1])
        else:
            self.is_editing_mode_enabled = False
            self.adress_book.edit(self.data_before_edit, (self.name_input.text(),
                                                          self.adress_input.toPlainText()))
            self.name_input.setEnabled(False)
            self.adress_input.setEnabled(False)
            self.button_enabled("default")

    def delete_button_click(self) -> None:
        self.adress_book.delete()
        self.set_current_data_to_inputs()

    def save_button_click(self) -> None:
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(caption="Save File", filter="ABK files (*.abk)")
        self.adress_book.save(file_path)

    def open_button_click(self) -> None:
        file_dialog = QtWidgets.QFileDialog()

        file_dialog.setNameFilter("ABK files (*.abk)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.adress_book.read(filenames[0])
            self.set_current_data_to_inputs()

    is_inputs_cleaned: bool = False

    def add_button_click(self) -> None:
        if not self.is_inputs_cleaned:
            self.is_inputs_cleaned = True
            self.name_input.setText("")
            self.adress_input.setText("")
            self.name_input.setEnabled(True)
            self.adress_input.setEnabled(True)
            self.name_input.setFocus()
            self.button_enabled("add")

        if self.is_inputs_cleaned and self.name_input.text() != "" and self.adress_input.toPlainText() != "":
            self.adress_book.add(self.name_input.text(), self.adress_input.toPlainText())
            self.is_inputs_cleaned = False
            self.name_input.setEnabled(False)
            self.adress_input.setEnabled(False)
            self.button_enabled("default")

    def set_current_data_to_inputs(self) -> None:
        data = self.adress_book.get_current()
        if data is not None:
            self.name_input.setText(data[0])
            self.adress_input.setText(data[1])
        else:
            self.name_input.setText("")
            self.adress_input.setText("")

    def button_enabled(self, mode: str) -> None:
        self.add_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.open_button.setEnabled(False)
        if mode == "add":
            self.add_button.setEnabled(True)
        elif mode == "edit":
            self.edit_button.setEnabled(True)
        elif mode == "default":
            self.add_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            self.edit_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
            self.open_button.setEnabled(True)
