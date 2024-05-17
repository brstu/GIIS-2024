#include "addressbook.h"

#include <QFileDialog>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QtGui>

AddressBook::AddressBook(QWidget *parent)
    : QWidget(parent)
{
    QLabel nameLabel(tr("Name:"));
    nameLine = std::make_unique<QLineEdit>();
    nameLine->setReadOnly(true);

    QLabel addressLabel(tr("Address:"));
    addressText = std::make_unique<QTextEdit>();
    addressText->setReadOnly(true);

    addButton = std::make_unique<QPushButton>(tr("&Add"));
    addButton->show();

    submitButton = std::make_unique<QPushButton>(tr("&Submit"));
    submitButton->hide();

    cancelButton = std::make_unique<QPushButton>(tr("&Cancel"));
    cancelButton->hide();

    nextButton = std::make_unique<QPushButton>(tr("&Next"));
    nextButton->setEnabled(false);

    previousButton = std::make_unique<QPushButton>(tr("&Previous"));
    previousButton->setEnabled(false);

    editButton = std::make_unique<QPushButton>(tr("&Edit"));
    editButton->setEnabled(false);

    removeButton = std::make_unique<QPushButton>(tr("&Remove"));
    removeButton->setEnabled(false);

    findButton = std::make_unique<QPushButton>(tr("&Find"));
    findButton->setEnabled(false);

    loadButton = std::make_unique<QPushButton>(tr("&Load..."));
    loadButton->setToolTip(tr("Load contacts from a file"));

    saveButton = std::make_unique<QPushButton>(tr("&Save..."));
    saveButton->setToolTip(tr("Save contacts to a file"));

    exportButton = std::make_unique<QPushButton>(tr("E&xport"));
    exportButton->setToolTip(tr("Export as vCard"));

    dialog = std::make_unique<FindDialog>();

    connect(addButton.get(), SIGNAL(clicked()), this, SLOT(addContact()));
    connect(submitButton.get(), SIGNAL(clicked()), this, SLOT(submitContact()));
    connect(cancelButton.get(), SIGNAL(clicked()), this, SLOT(cancel()));
    connect(nextButton.get(), SIGNAL(clicked()), this, SLOT(next()));
    connect(previousButton.get(), SIGNAL(clicked()), this, SLOT(previous()));
    connect(editButton.get(), SIGNAL(clicked()), this, SLOT(editContact()));
    connect(removeButton.get(), SIGNAL(clicked()), this, SLOT(removeContact()));
    connect(findButton.get(), SIGNAL(clicked()), this, SLOT(findContact()));
    connect(loadButton.get(), SIGNAL(clicked()), this, SLOT(loadFromFile()));
    connect(saveButton.get(), SIGNAL(clicked()), this, SLOT(saveToFile()));
    connect(exportButton.get(), SIGNAL(clicked()), this, SLOT(exportAsVCard()));

    auto buttonLayout1 = std::make_unique<QVBoxLayout>();
    buttonLayout1->addWidget(addButton.get(), Qt::AlignTop);
    buttonLayout1->addWidget(submitButton.get());
    buttonLayout1->addWidget(cancelButton.get());
    buttonLayout1->addWidget(findButton.get());
    buttonLayout1->addWidget(editButton.get());
    buttonLayout1->addWidget(removeButton.get());
    buttonLayout1->addWidget(loadButton.get());
    buttonLayout1->addWidget(saveButton.get());
    buttonLayout1->addWidget(exportButton.get());
    buttonLayout1->addStretch();

    auto buttonLayout2 = std::make_unique<QHBoxLayout>();
    buttonLayout2->addWidget(previousButton.get());
    buttonLayout2->addWidget(nextButton.get());

    auto mainLayout = std::make_unique<QGridLayout>();
    mainLayout->addWidget(&nameLabel, 0, 0);
    mainLayout->addWidget(nameLine.get(), 0, 1);
    mainLayout->addWidget(&addressLabel, 1, 0, Qt::AlignTop);
    mainLayout->addWidget(addressText.get(), 1, 1);
    mainLayout->addLayout(buttonLayout1, 1, 2);
    mainLayout->addLayout(buttonLayout2, 2, 1);

    setLayout(mainLayout);
    setWindowTitle(tr("Simple Address Book"));
}


void AddressBook::addContact()
{
    oldName = nameLine->text();
    oldAddress = addressText->toPlainText();

    nameLine->clear();
    addressText->clear();

    updateInterface(AddingMode);
}

void AddressBook::submitContact()
{
    QString name = nameLine->text();
         QString address = addressText->toPlainText();

         if (name.isEmpty() || address.isEmpty()) {
             QMessageBox::information(this, tr("Empty Field"),
                 tr("Please enter a name and address."));
             return;
         }

         if (currentMode == AddingMode) {

             if (!contacts.contains(name)) {
                 contacts.insert(name, address);
                 QMessageBox::information(this, tr("Add Successful"),
                     tr("\"%1\" has been added to your address book.").arg(name));
             } else {
                 QMessageBox::information(this, tr("Add Unsuccessful"),
                     tr("Sorry, \"%1\" is already in your address book.").arg(name));
             }
         } else if (currentMode == EditingMode) {

             if (oldName != name) {
                 if (!contacts.contains(name)) {
                     QMessageBox::information(this, tr("Edit Successful"),
                         tr("\"%1\" has been edited in your address book.").arg(oldName));
                     contacts.remove(oldName);
                     contacts.insert(name, address);
                 } else {
                     QMessageBox::information(this, tr("Edit Unsuccessful"),
                         tr("Sorry, \"%1\" is already in your address book.").arg(name));
                 }
             } else if (oldAddress != address) {
                 QMessageBox::information(this, tr("Edit Successful"),
                     tr("\"%1\" has been edited in your address book.").arg(name));
                 contacts[name] = address;
             }
         }

         updateInterface(NavigationMode);
}

void AddressBook::cancel()
{
    int number = contacts.size();
    nextButton->setEnabled(number > 1);
    previousButton->setEnabled(number > 1);

    nameLine->setText(oldName);
    nameLine->setReadOnly(true);

    addressText->setText(oldAddress);
    addressText->setReadOnly(true);

    addButton->setEnabled(true);
    submitButton->hide();
    cancelButton->hide();
}

void AddressBook::next()
{
    QString name = nameLine->text();
    QMap<QString, QString>::iterator i = contacts.find(name);

    if (i != contacts.end())
        i++;

    if (i == contacts.end())
        i = contacts.begin();

    nameLine->setText(i.key());
    addressText->setText(i.value());
}

void AddressBook::previous()
{
    QString name = nameLine->text();
    QMap<QString, QString>::iterator i = contacts.find(name);

    if (i == contacts.end()){
        nameLine->clear();
        addressText->clear();
        return;
    }

    if (i == contacts.begin())
        i = contacts.end();

    i--;
    nameLine->setText(i.key());
    addressText->setText(i.value());
}

void AddressBook::editContact()
{
    oldName = nameLine->text();
    oldAddress = addressText->toPlainText();

    updateInterface(EditingMode);
}

void AddressBook::removeContact()
{
    QString name = nameLine->text();
    QString address = addressText->toPlainText();

    if (contacts.contains(name)) {

        int button = QMessageBox::question(this,
                                           tr("Confirm Remove"),
                                           tr("Are you sure you want to remove \"%1\"?").arg(name),
                                           QMessageBox::Yes | QMessageBox::No);

        if (button == QMessageBox::Yes) {

            previous();
            contacts.remove(name);

            QMessageBox::information(this, tr("Remove Successful"),
                                     tr("\"%1\" has been removed from your address book.").arg(name));
        }
    }

    updateInterface(NavigationMode);
}

void AddressBook::updateInterface(Mode mode)
{
    currentMode = mode;

    switch (currentMode) {

    case AddingMode:
    case EditingMode:

        nameLine->setReadOnly(false);
        nameLine->setFocus(Qt::OtherFocusReason);
        addressText->setReadOnly(false);

        addButton->setEnabled(false);
        editButton->setEnabled(false);
        removeButton->setEnabled(false);

        nextButton->setEnabled(false);
        previousButton->setEnabled(false);

        submitButton->show();
        cancelButton->show();
        break;
    case NavigationMode:

        if (contacts.isEmpty()) {
            nameLine->clear();
            addressText->clear();
        }

        nameLine->setReadOnly(true);
        addressText->setReadOnly(true);
        addButton->setEnabled(true);

        int number = contacts.size();
        editButton->setEnabled(number >= 1);
        removeButton->setEnabled(number >= 1);
        findButton->setEnabled(number > 1);
        nextButton->setEnabled(number > 1);
        previousButton->setEnabled(number >1 );

        submitButton->hide();
        cancelButton->hide();
        break;
    }
}

void AddressBook::findContact()
{
    dialog->show();

    if (dialog->exec() == QDialog::Accepted) {
        QString contactName = dialog->getFindText();

        if (contacts.contains(contactName)) {
            nameLine->setText(contactName);
            addressText->setText(contacts.value(contactName));
        } else {
            QMessageBox::information(this, tr("Contact Not Found"),
                                     tr("Sorry, \"%1\" is not in your address book.").arg(contactName));
            return;
        }
    }

    updateInterface(NavigationMode);
}

void AddressBook::saveToFile()
{
    if (QString fileName = QFileDialog::getOpenFileName(this,
                                                    tr("Open Address Book"), "",
                                                    tr("Address Book (*.abk);;All Files (*)"));fileName.isEmpty())
{
    return;
}
    else {
        QFile file(fileName);
        if (!file.open(QIODevice::WriteOnly)) {
            QMessageBox::information(this, tr("Unable to open file"),
                                     file.errorString());
            return;
        }
        QDataStream out(&file);
        out.setVersion(QDataStream::Qt_4_5);
        out << contacts;
    }
}

void AddressBook::loadFromFile()
{
    QString fileName = QFileDialog::getOpenFileName(this,
                                                    tr("Open Address Book"), "",
                                                    tr("Address Book (*.abk);;All Files (*)"));
    if (fileName.isEmpty())
        return;
    else {

        QFile file(fileName);

        if (!file.open(QIODevice::ReadOnly)) {
            QMessageBox::information(this, tr("Unable to open file"),
                                     file.errorString());
            return;
        }

        QDataStream in(&file);
        in.setVersion(QDataStream::Qt_4_5);
        contacts.empty();   // очищаем существующие контакты
        in >> contacts;
        if (contacts.isEmpty()) {
            QMessageBox::information(this, tr("No contacts in file"),
                                     tr("The file you are attempting to open contains no contacts."));
        } else {
            auto i = contacts.begin();
            nameLine->setText(i.key());
            addressText->setText(i.value());
        }
    }

    updateInterface(NavigationMode);
}

void AddressBook::exportAsVCard()
{
    QString name = nameLine->text();
    QString address = addressText->toPlainText();
    QString firstName;
    QString lastName;
    QStringList nameList;

    int index = name.indexOf(" ");

    if (index != -1) {
        nameList = name.split(QRegExp("\\s+"), QString::SkipEmptyParts);
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
