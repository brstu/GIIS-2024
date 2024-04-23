#ifndef ADDRESSBOOK_H
#define ADDRESSBOOK_H

#include <QMainWindow>
#include "ui_addressbook.h"
#include <memory>

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

private:
    std::unique_ptr<Ui::AddressBook> ui;
};
#endif // ADDRESSBOOK_H
