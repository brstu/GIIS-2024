## Лабораторная работа №2 <br/> ##

## Тема ##

Разработка приложения «Адресная книга» средствами Qt

## Цель работы ##

Изучить базовые компоненты средства разработки графического интерфейса среды Qt.

## Задание ##

Выполнить последовательно разработку приложения «Адресная книга», согласно учебному пособию расположенному по адресу (K:\LOOK\4-kurs\ГИИС\Lab3\crossplatform\tutorials-addressbook.html).

## Результат работы ##

![основные функции](./1.jpg)
![сохранение файла](./2.jpg)
![открытие файла](./3.jpg)
![экспорт файла](./4.jpg)


## Код программы ##

### Конструктор и деструктор ###
```cpp
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}
```

### Использование указателей ###

```cpp
void MainWindow::on_pushButton_2_clicked()
{
    QListWidgetItem *selectedItem = ui->listWidget->currentItem();

    if (selectedItem) {
        // ... (прочие действия)

        // Обновляем данные в списке
        QString updatedEntry = name + " - " + address;
        selectedItem->setText(updatedEntry);
    } else {
        QMessageBox::warning(this, "No item selected ...", "Select an item from the list to edit.");
    }
}
```
В данном фрагменте кода используется указатель selectedItem для работы с выбранным элементом в списке. Это позволяет динамически изменять данные элемента.