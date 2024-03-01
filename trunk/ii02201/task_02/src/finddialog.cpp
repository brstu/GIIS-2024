#include "finddialog.h"

FindDialog::FindDialog(QWidget *parent)
    : QDialog(parent)
{
    QLabel *findLabel = new QLabel("Enter the name of a contact:");
    lineEdit = new QLineEdit;

    findButton = new QPushButton("&Find");
    findText = "";

    QHBoxLayout *layout = new QHBoxLayout;
    layout->addWidget(findLabel);
    layout->addWidget(lineEdit);
    layout->addWidget(findButton);

    this->setLayout(layout);
    setWindowTitle(tr("Find a Contact"));
    connect(findButton, SIGNAL(clicked()), this, SLOT(findClicked()));
}

void FindDialog::findClicked()
{
    QString text = lineEdit->text();

    if (text.isEmpty()) {
        QMessageBox::information(this, tr("Empty Field"),
                                 tr("Please enter a name."));
        return;
    } else {
        findText = text;
        lineEdit->clear();
        this->accept();
        hide();
    }
}


QString FindDialog::getFindText()
{
    return findText;
}



