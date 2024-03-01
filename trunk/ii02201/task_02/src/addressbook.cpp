#include "addressbook.h"
#include "./ui_addressbook.h"
#include <QRegularExpression>

AddressBook::AddressBook(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::AddressBook)
{
    ui->setupUi(this);
    ui->nameLine->setReadOnly(true);
    ui->addressText->setReadOnly(true);

    ui->submitButton->setEnabled(false);
    ui->cancelButton->setEnabled(false);

    ui->submitButton->hide();
    ui->cancelButton->hide();

    ui->nextButton->setEnabled(false);
    ui->prevButton->setEnabled(false);
    ui->editButton->setEnabled(false);
    ui->removeButton->setEnabled(false);
    ui->findButton->setEnabled(false);

    dialog = new FindDialog;

    ui->loadButton->setToolTip(tr("Load contacts from a file"));
    ui->saveButton->setToolTip(tr("Save contacts to a file"));
}

AddressBook::~AddressBook()
{
    delete ui;
}

void AddressBook::on_addButton_clicked()
{
    this->oldName = ui->nameLine->text();
    this->oldAddress = ui->addressText->toPlainText();

    ui->nameLine->clear();
    ui->addressText->clear();

    ui->nameLine->setReadOnly(false);
    ui->nameLine->setFocus(Qt::OtherFocusReason);
    ui->addressText->setReadOnly(false);

    ui->addButton->setEnabled(false);

    ui->submitButton->show();
    ui->cancelButton->show();
    ui->submitButton->setEnabled(true);
    ui->cancelButton->setEnabled(true);

    ui->nextButton->setEnabled(false);
    ui->prevButton->setEnabled(false);

    this->updateInterface(AddingMode);
}


void AddressBook::on_submitButton_clicked()
{
    QString name = ui->nameLine->text();
    QString address = ui->addressText->toPlainText();

    if (currentMode == AddingMode) {

        if (name.isEmpty() || address.isEmpty()) {
            QMessageBox::information(this, "Empty Field", "Please enter a name and address.");
            return;
        }

        if (!contacts.contains(name)) {
            contacts.insert(name, address);
            QMessageBox::information(this, tr("Add Successful"),
                                     tr("\"%1\" has been added to your address book.").arg(name));
        } else {
            QMessageBox::information(this, tr("Add Unsuccessful"),
                                     tr("Sorry, \"%1\" is already in your address book.").arg(name));
            ui->addressText->setText(this->oldAddress);
        }
    } else if (currentMode == EditingMode) {

        if (name.isEmpty() || address.isEmpty()) {
            QMessageBox::information(this, "Empty Field", "Please enter a name and address.");
            return;
        }

        if (oldName != name) {
            if (!contacts.contains(name)) {
                QMessageBox::information(this, tr("Edit Successful"),
                                         tr("\"%1\" has been edited in your address book.").arg(oldName));
                contacts.remove(oldName);
                contacts.insert(name, address);
            } else {
                QMessageBox::information(this, tr("Edit Unsuccessful"),
                                         tr("Sorry, \"%1\" is already in your address book.").arg(name));
                ui->addressText->setText(this->oldAddress);
            }
        } else if (oldAddress != address) {
            QMessageBox::information(this, tr("Edit Successful"),
                                     tr("\"%1\" has been edited in your address book.").arg(name));
            contacts[name] = address;
        }
    }

    this->updateInterface(NavigationMode);

    if (contacts.isEmpty()) {
        ui->nameLine->clear();
        ui->addressText->clear();
    }

    ui->nameLine->setReadOnly(true);
    ui->addressText->setReadOnly(true);
    ui->addButton->setEnabled(true);
    ui->submitButton->hide();
    ui->cancelButton->hide();

    int number = contacts.size();
    ui->nextButton->setEnabled(number > 1);
    ui->prevButton->setEnabled(number > 1);
}


void AddressBook::on_cancelButton_clicked()
{
    ui->nameLine->setText(oldName);
    ui->nameLine->setReadOnly(true);

    ui->addressText->setText(oldAddress);
    ui->addressText->setReadOnly(true);

    ui->addButton->setEnabled(true);
    ui->submitButton->hide();
    ui->cancelButton->hide();

    int number = contacts.size();
    ui->nextButton->setEnabled(number > 1);
    ui->prevButton->setEnabled(number > 1);

    this->updateInterface(NavigationMode);
}


void AddressBook::on_nextButton_clicked()
{
    QString name = ui->nameLine->text();
    QMap<QString, QString>::iterator i = contacts.find(name);

    if (i != contacts.end())
        i++;

    if (i == contacts.end())
        i = contacts.begin();

    ui->nameLine->setText(i.key());
    ui->addressText->setText(i.value());
}


void AddressBook::on_prevButton_clicked()
{
    QString name = ui->nameLine->text();
    QMap<QString, QString>::iterator i = contacts.find(name);

    if (i == contacts.end()){
        ui->nameLine->clear();
        ui->addressText->clear();
        return;
    }

    if (i == contacts.begin())
        i = contacts.end();

    i--;
    ui->nameLine->setText(i.key());
    ui->addressText->setText(i.value());
}


void AddressBook::on_editButton_clicked()
{
    oldName = ui->nameLine->text();
    oldAddress = ui->addressText->toPlainText();

    this->updateInterface(EditingMode);
}


void AddressBook::on_removeButton_clicked()
{
    QString name = ui->nameLine->text();

    if (contacts.contains(name)) {

        int button = QMessageBox::question(this,
                                           tr("Confirm Remove"),
                                           tr("Are you sure you want to remove \"%1\"?").arg(name),
                                           QMessageBox::Yes | QMessageBox::No);

        if (button == QMessageBox::Yes) {

            on_prevButton_clicked();
            contacts.remove(name);

            QMessageBox::information(this, tr("Remove Successful"),
                                     tr("\"%1\" has been removed from your address book.").arg(name));
        }
    }

    this->updateInterface(NavigationMode);
}


void AddressBook::updateInterface(Mode mode)
{
    this->currentMode = mode;

    switch (currentMode) {

    case AddingMode:
    case EditingMode:

        ui->nameLine->setReadOnly(false);
        ui->nameLine->setFocus(Qt::OtherFocusReason);
        ui->addressText->setReadOnly(false);

        ui->addButton->setEnabled(false);
        ui->editButton->setEnabled(false);
        ui->removeButton->setEnabled(false);

        ui->nextButton->setEnabled(false);
        ui->prevButton->setEnabled(false);

        ui->submitButton->show();
        ui->cancelButton->show();
        break;

    case NavigationMode:

        if (contacts.isEmpty()) {
            ui->nameLine->clear();
            ui->addressText->clear();
        }

        ui->nameLine->setReadOnly(true);
        ui->addressText->setReadOnly(true);
        ui->addButton->setEnabled(true);

        int number = contacts.size();
        ui->editButton->setEnabled(number >= 1);
        ui->removeButton->setEnabled(number >= 1);
        ui->nextButton->setEnabled(number > 1);
        ui->prevButton->setEnabled(number >1 );
        ui->findButton->setEnabled(number >1 );

        ui->submitButton->hide();
        ui->cancelButton->hide();
        break;
    }
}


void AddressBook::on_findButton_clicked()
{
    this->dialog->show();

    if (this->dialog->exec() == QDialog::Accepted) {
        QString contactName = dialog->getFindText();

        if (contacts.contains(contactName)) {
            ui->nameLine->setText(contactName);
            ui->addressText->setText(contacts.value(contactName));
        } else {
            QMessageBox::information(this, tr("Contact Not Found"),
                                     tr("Sorry, \"%1\" is not in your address book.").arg(contactName));
            return;
        }
    }

    updateInterface(NavigationMode);
}


void AddressBook::on_saveButton_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Save Address Book", "", "Address Book (*.abk);;All Files (*)");

    if (fileName.isEmpty())
        return;
    else {
        QFile file(fileName);
        if (!file.open(QIODevice::WriteOnly)) {
            QMessageBox::information(this, "Unable to open file", file.errorString());
            return;
        }

        QDataStream out(&file);
        out.setVersion(QDataStream::Qt_5_6);
        out << contacts;
    }
}


void AddressBook::on_loadButton_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this, "Open Address Book", "", "Address Book (*.abk);;All Files (*)");

    if (fileName.isEmpty())
        return;
    else {

        QFile file(fileName);

        if (!file.open(QIODevice::ReadOnly)) {
            QMessageBox::information(this, "Unable to open file", file.errorString());
            return;
        }

        QDataStream in(&file);
        in.setVersion(QDataStream::Qt_5_6);
        contacts.empty();
        in >> contacts;

        if (contacts.isEmpty()) {
            QMessageBox::information(this, "No contacts in file", "The file you are attempting to open contains no contacts.");
        } else {
            QMap<QString, QString>::iterator i = contacts.begin();
            ui->nameLine->setText(i.key());
            ui->addressText->setText(i.value());
        }
    }

    updateInterface(NavigationMode);
}


void AddressBook::on_exportButton_clicked()
{
    QString name = ui->nameLine->text();
    QString address = ui->addressText->toPlainText();
    QString firstName;
    QString lastName;
    QStringList nameList;

    int index = name.indexOf(" ");

    if (index != -1) {
        nameList = name.split(QRegularExpression("\\s+"), Qt::SkipEmptyParts);
        firstName = nameList.first();
        lastName = nameList.last();
    } else {
        firstName = name;
        lastName = "";
    }

    QString fileName = QFileDialog::getSaveFileName(this,
                                                    tr("Export Contact"), "",
                                                    tr("vCard Files (*.vcf);;All Files (*)"));

    if (fileName.isEmpty())
        return;

    QFile file(fileName);

    if (!file.open(QIODevice::WriteOnly)) {
        QMessageBox::information(this, tr("Unable to open file"),
                                 file.errorString());
        return;
    }

    QTextStream out(&file);

    out << "BEGIN:VCARD" << "\n";
    out << "VERSION:2.1" << "\n";
    out << "N:" << lastName << ";" << firstName << "\n";

    if (!nameList.isEmpty())
        out << "FN:" << nameList.join(" ") << "\n";
    else
        out << "FN:" << firstName << "\n";

    address.replace(";", "\\;", Qt::CaseInsensitive);
    address.replace("\n", ";", Qt::CaseInsensitive);
    address.replace(",", " ", Qt::CaseInsensitive);

    out << "ADR;HOME:;" << address << "\n";
    out << "END:VCARD" << "\n";

    QMessageBox::information(this, tr("Export Successful"),
                             tr("\"%1\" has been exported as a vCard.").arg(name));
}

