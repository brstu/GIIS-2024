#ifndef ADDRESSBOOK_H
#define ADDRESSBOOK_H

#include <QWidget>
#include <QMessageBox>
#include <QFile>
#include <QFileDialog>
#include "finddialog.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class AddressBook;
}
QT_END_NAMESPACE

class AddressBook : public QWidget
{
    Q_OBJECT

public:
    explicit AddressBook(QWidget *parent = nullptr);
    ~AddressBook();

private slots:
    void on_addButton_clicked();

    void on_submitButton_clicked();

    void on_cancelButton_clicked();

    void on_nextButton_clicked();

    void on_prevButton_clicked();

    void on_editButton_clicked();

    void on_removeButton_clicked();

    void on_findButton_clicked();

    void on_saveButton_clicked();

    void on_loadButton_clicked();

    void on_exportButton_clicked();

private:
    std::unique_ptr<Ui::AddressBook> ui;
    std::unique_ptr<FindDialog> dialog;
    QMap<QString, QString> contacts;
    QString oldName;
    QString oldAddress;
    enum Mode { NavigationMode, AddingMode, EditingMode };
    void updateInterface(Mode mode);
    Mode currentMode;
};
#endif // ADDRESSBOOK_H
