#include "finddialog.h"

#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>

FindDialog::FindDialog(QWidget *parent)
    : QDialog(parent),findText("")
{
    QLabel findLabel(tr("Enter the name of a contact:"));
    lineEdit = std::make_unique<QLineEdit>();
    findButton = std::make_unique<QPushButton>(tr("&Find"));
    
    
    auto layout = std::make_unique<QHBoxLayout>();

    layout->addWidget(&findLabel);
    layout->addWidget(lineEdit.get());
    layout->addWidget(findButton.get());
    setLayout(layout);
    setWindowTitle(tr("Find a Contact"));

    connect(findButton.get(), SIGNAL(clicked()), this, SLOT(findClicked()));
    connect(findButton.get(), SIGNAL(clicked()), this, SLOT(accept()));
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
        hide();
    }
}

QString FindDialog::getFindText() const
 {
     return findText;
 }
