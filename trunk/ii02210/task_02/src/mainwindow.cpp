#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QMessageBox>
#include <QInputDialog>
#include <QFileDialog>
#include <QTextStream>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(std::make_unique<Ui::MainWindow>())
{
    ui->setupUi(this);
}

MainWindow::~MainWindow() = default;

void MainWindow::on_pushButton_clicked()
{
    QString name = ui->lineEdit->text();
    QString address = ui->lineEdit_2->text();

    if (name.isEmpty() || address.isEmpty()) {
        QMessageBox::warning(this, "Empty field ...", "Enter data in both fields !!");
        return;
    }

    QString entry = name + " - " + address;

    ui->listWidget->addItem(entry);

    ui->lineEdit->clear();
    ui->lineEdit_2->clear();
}


void MainWindow::on_pushButton_3_clicked()
{
    QListWidgetItem *selectedItem = ui->listWidget->currentItem();

    if (selectedItem) {
        QMessageBox::StandardButton reply = QMessageBox::question(
            this,
            "Confirm your action",
            "Are you sure you want to remove the item from the list ?",
            QMessageBox::Yes | QMessageBox::No
            );

        if (reply == QMessageBox::Yes) {
            int row = ui->listWidget->row(selectedItem);
            ui->listWidget->takeItem(row);
        }
    } else {
        QMessageBox::warning(this, "No item selected ...", "Select an item from the list to delete.");
    }
}

<<<<<<< HEAD


=======
>>>>>>> e5b97fac54470d53b97f6f0b9b30d0e87b2ac468
void MainWindow::on_pushButton_2_clicked()
{
    QListWidgetItem *selectedItem = ui->listWidget->currentItem();

    if (selectedItem) {
        QString currentText = selectedItem->text();
        QStringList currentData = currentText.split(" - ");

        bool ok;
        QString name = QInputDialog::getText(this, "Edit window", "Name:", QLineEdit::Normal, currentData.at(0), &ok);

        if (!ok) {
            return;
        }

        QString address = QInputDialog::getText(this, "Edit window", "Address:", QLineEdit::Normal, currentData.at(1), &ok);

        if (!ok) {
            return;
        }

        if (name.isEmpty() || address.isEmpty()) {
            QMessageBox::warning(this, "Empty field ...", "Enter data in both fields !!");
            return;
        }
        // Обновляем данные в списке
        QString updatedEntry = name + " - " + address;
        selectedItem->setText(updatedEntry);
    } else {
        QMessageBox::warning(this, "No item selected ...", "Select an item from the list to edit.");
    }
}


void MainWindow::on_pushButton_5_clicked()
{
    QString nameToSearch = ui->lineEdit->text();
    QString addressToSearch = ui->lineEdit_2->text();

    if (nameToSearch.isEmpty() || addressToSearch.isEmpty()) {
        QMessageBox::warning(this, "Empty field ...", "Enter data in both fields !!");
        return;
    }

    ui->listWidget->clearSelection();

    for (int i = 0; i < ui->listWidget->count(); ++i) {
        QListWidgetItem *item = ui->listWidget->item(i);
        QString currentItemText = item->text();
        QStringList currentData = currentItemText.split(" - ");

        if (currentData.at(0) == nameToSearch && currentData.at(1) == addressToSearch) {

            ui->listWidget->scrollToItem(item, QAbstractItemView::PositionAtCenter);

            item->setSelected(true);
        }
    }

    if (ui->listWidget->selectedItems().isEmpty()) {
        QMessageBox::information(this, "Item not found ...", "There is no such element in the list.");
    }
}

void MainWindow::on_actionOPEN_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(this, "Open file ...", QDir::homePath(), "Text Files (*.txt)");

    if (fileName.isEmpty()) {
        return;
    }

    QFile file(fileName);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {

        ui->listWidget->clear();

        QTextStream stream(&file);
        while (!stream.atEnd()) {
            QString line = stream.readLine();
            ui->listWidget->addItem(line);
        }

        file.close();

        QMessageBox::information(this, "Successfully ...", "The file was successfully opened and the data was loaded !!");
    } else {
        QMessageBox::warning(this, "Error ...", "Failed to open file !!");
    }
}


void MainWindow::on_actionEXPORT_triggered()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export in vCard", QDir::homePath(), "vCard Files (*.vcf)");

    if (fileName.isEmpty()) {
        return;
    }

    QFile file(fileName);
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream stream(&file);

        stream << "BEGIN:VCARD\nVERSION:3.0\n";

        for (int i = 0; i < ui->listWidget->count(); ++i) {
            QListWidgetItem *item = ui->listWidget->item(i);
            QStringList data = item->text().split(" - ");

            if (data.size() == 2) {
                QString name = data.at(0);
                QString address = data.at(1);

                stream << "FN:" << name << "\n";
                stream << "ADR:" << address << "\n";
            }
        }

        stream << "END:VCARD\n";

        file.close();

        QMessageBox::information(this, "Successfully ...", "The data is successfully exported to vCard !!");
    } else {

        QMessageBox::warning(this, "Error ...", "Failed to export to vCard !!");
    }
}


void MainWindow::on_actionSAVE_triggered()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Save list ...", QDir::homePath(), "Text Files (*.txt)");

    if (fileName.isEmpty()) {
        return;
    }

    QFile file(fileName);
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream stream(&file);

        for (int i = 0; i < ui->listWidget->count(); ++i) {
            QListWidgetItem *item = ui->listWidget->item(i);
            stream << item->text() << "\n";
        }

        file.close();

        QMessageBox::information(this, "Successfully ...", "The list was successfully save !!");
    } else {

        QMessageBox::warning(this, "Error ...", "Failed to save list !!");
    }
}

