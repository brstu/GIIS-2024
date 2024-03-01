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
    explicit FindDialog(QWidget *parent = 0);
    QString getFindText();

public slots:
    void findClicked();

private:
    QPushButton *findButton;
    QLineEdit *lineEdit;
    QString findText;
    FindDialog *dialog;
};

#endif // FINDDIALOG_H
