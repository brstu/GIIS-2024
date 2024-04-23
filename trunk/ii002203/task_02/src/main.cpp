#include "addressbook.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    AddressBook addressBook;
    addressBook.setWindowTitle("Адресная книга");
    addressBook.show();
    return a.exec();
}
