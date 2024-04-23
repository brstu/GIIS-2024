#include "addressbook.h"
#include "./ui_addressbook.h"

#include <QMessageBox>
#include <QFileDialog>

AddressBook::AddressBook(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::AddressBook)
{
    ui->setupUi(this);
    ui->labelName->setVisible(false);
    ui->lineName->setVisible(false);
    ui->buttonOK->setVisible(false);
    ui->buttonCancel->setVisible(false);

    connect(ui->actionSave, &QAction::triggered, this, &AddressBook::saveToFile);
    connect(ui->actionLoad, &QAction::triggered, this, &AddressBook::loadFromFile);
}

void AddressBook::on_buttonAdd_clicked()
{
    ui->tableAddress->insertRow(ui->tableAddress->rowCount());
}

void AddressBook::on_buttonRemove_clicked()
{
    QList<QTableWidgetSelectionRange> selectedRanges = ui->tableAddress->selectedRanges();

    if (!selectedRanges.isEmpty()) {
        for (const QTableWidgetSelectionRange &range : selectedRanges) {
            int topRow = range.topRow();
            int bottomRow = range.bottomRow();
            for (int row = bottomRow; row >= topRow; --row) {
                ui->tableAddress->removeRow(row);
            }
        }
    }
}

void AddressBook::on_buttonSearch_clicked()
{
    ui->buttonSearch->setVisible(false);
    ui->labelName->setVisible(true);
    ui->lineName->setVisible(true);
    ui->buttonOK->setVisible(true);
    ui->buttonCancel->setVisible(true);
}

void AddressBook::on_buttonCancel_clicked()
{
    ui->lineName->clear();
    ui->labelName->setVisible(false);
    ui->lineName->setVisible(false);
    ui->buttonOK->setVisible(false);
    ui->buttonCancel->setVisible(false);
    ui->buttonSearch->setVisible(true);
}

void AddressBook::on_buttonOK_clicked()
{
    QString name = ui->lineName->text();
    ui->lineName->clear();
    for (int row = 0; row < ui->tableAddress->rowCount(); ++row) {
        QTableWidgetItem *item = ui->tableAddress->item(row, 0);
        if (item && item->text() == name) {
            ui->tableAddress->selectRow(row);
            return;
        }
    }
}

void AddressBook::saveToFile()
{
    QString fileName = QFileDialog::getSaveFileName(this,
                                                    tr("Сохранение"), "",
                                                    tr("Таблица (*.csv);;All Files (*)"));
    if (fileName.isEmpty())
        return;

    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() << "Не удалось открыть файл для записи";
        return;
    }

    QTextStream out(&file);
    out.setLocale(QLocale::c());
    out.setGenerateByteOrderMark(true);

    QStringList headers;
    for (int col = 0; col < ui->tableAddress->columnCount(); ++col) {
        headers << ui->tableAddress->horizontalHeaderItem(col)->text();
    }
    out << headers.join(";") << "\n";

    for (int row = 0; row < ui->tableAddress->rowCount(); ++row) {
        QStringList rowData;
        for (int col = 0; col < ui->tableAddress->columnCount(); ++col) {
            QTableWidgetItem *item = ui->tableAddress->item(row, col);
            if (item) {
                rowData << item->text().replace(",", ";");
            } else {
                rowData << "";
            }
        }
        out << rowData.join(";") << "\n";
    }

    file.close();
    }
}

void AddressBook::loadFromFile()
{
    QString fileName = QFileDialog::getOpenFileName(this, tr("Загрузка данных"), QDir::currentPath(), tr("CSV файлы (*.csv);;Все файлы (*.*)"));
    if (fileName.isEmpty()) return;
    else {
        QFile file(fileName);
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
            qDebug() << "Не удалось открыть файл для чтения";
            return;
        }

        QTextStream in(&file);

        ui->tableAddress->clearContents();
        ui->tableAddress->setRowCount(0);

        in.readLine();

        while (!in.atEnd()) {
            QString line = in.readLine();
            QStringList parts = line.split(";");
            int row = ui->tableAddress->rowCount();
            ui->tableAddress->insertRow(row);
            for (int col = 0; col < parts.size(); ++col) {
                QTableWidgetItem *item = new QTableWidgetItem(parts[col]);
                ui->tableAddress->setItem(row, col, item);
            }
        }

        file.close();
    }
}

