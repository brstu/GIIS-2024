#ifndef ADDRESSBOOK_H
#define ADDRESSBOOK_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class AddressBook;
}
QT_END_NAMESPACE

class AddressBook : public QMainWindow
{
    Q_OBJECT

public:
    AddressBook(QWidget *parent = nullptr);
    ~AddressBook();

private slots:


    void on_buttonAdd_clicked();

    void on_buttonRemove_clicked();

private:
    Ui::AddressBook *ui;
};
#endif // ADDRESSBOOK_H
