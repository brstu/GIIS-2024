#include "addressbook.h"
#include "./ui_addressbook.h"

#include <QInputDialog>

AddressBook::AddressBook(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::AddressBook)
{
    ui->setupUi(this);
}

AddressBook::~AddressBook()
{
    delete ui;
}

void AddressBook::on_buttonAdd_clicked()
{
    ui->tableAddress->insertRow(ui->tableAddress->rowCount());
}



void AddressBook::on_buttonRemove_clicked()
{
    QList<QTableWidgetSelectionRange> selectedRanges = ui->tableAddress->selectedRanges();

    if (!selectedRanges.isEmpty()) {
        foreach (const QTableWidgetSelectionRange &range, selectedRanges) {
            int topRow = range.topRow();
            int bottomRow = range.bottomRow();
            for (int row = bottomRow; row >= topRow; --row) {
                ui->tableAddress->removeRow(row);
            }
        }
    }
}

