#ifndef FINDDIALOG_H
#define FINDDIALOG_H

#include <QWidget>
#include <QDialog>
#include <QLineEdit>
#include <QPushButton>
#include <QMessageBox>
#include <QLabel>
#include <QHBoxLayout>

class FindDialog : public QDialog
{
    Q_OBJECT

public:
    explicit FindDialog(QWidget *parent = nullptr);
    QString getFindText() const;

public slots:
    void findClicked();

private:
    std::unique_ptr<QLineEdit> lineEdit { std::make_unique<QLineEdit>() };
    std::unique_ptr<QPushButton> findButton { std::make_unique<QPushButton>("&Find") };
    std::unique_ptr<QLabel> findLabel { std::make_unique<QLabel>("Enter the name of a contact:") };
    QString findText = "";
    FindDialog *dialog;
};

#endif // FINDDIALOG_H
