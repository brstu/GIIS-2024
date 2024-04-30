#ifndef ADDRESSBOOK_H
#define ADDRESSBOOK_H

#include <QMainWindow>
#include "ui_addressbook.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class AddressBook;
}
QT_END_NAMESPACE

class AddressBook : public QMainWindow
{
    Q_OBJECT

public:
    explicit AddressBook(QWidget *parent = nullptr);

private slots:
    void on_buttonAdd_clicked();
    void on_buttonRemove_clicked();
    void on_buttonSearch_clicked();
    void on_buttonCancel_clicked();
    void on_buttonOK_clicked();
    void saveToFile();
    void loadFromFile();

private:
    std::unique_ptr<Ui::AddressBook> ui;
};

#endif // ADDRESSBOOK_H
