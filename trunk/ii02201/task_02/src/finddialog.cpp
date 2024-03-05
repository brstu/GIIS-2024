#include "finddialog.h"

FindDialog::FindDialog(QWidget *parent)
    : QDialog(parent)
{
    std::unique_ptr<QHBoxLayout> layout { std::make_unique<QHBoxLayout>() };
    layout->addWidget(findLabel.release());
    layout->addWidget(lineEdit.release());
    layout->addWidget(findButton.release());

    this->setLayout(layout.release());
    setWindowTitle(tr("Find a Contact"));
    connect(findButton.release(), SIGNAL(clicked()), this, SLOT(findClicked()));
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


QString FindDialog::getFindText() const
{
    return findText;
}



