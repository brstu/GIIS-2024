#include <QLineEdit>
#include <QPushButton>
#include <QTextEdit>
#include <QWidget>
#include "finddialog.h"

class AddressBook : public QWidget
 {
     Q_OBJECT

 public:
     explicit AddressBook(QWidget *parent = nullptr);

     enum class Mode { NavigationMode, AddingMode, EditingMode };

 private:
     void updateInterface(Mode mode);

     QPushButton *addButton;
     QPushButton *submitButton;
     QPushButton *cancelButton;
     QPushButton *nextButton;
     QPushButton *previousButton;
     QLineEdit *nameLine;
     QTextEdit *addressText;
     QPushButton *editButton;
     QPushButton *removeButton;
     QPushButton *findButton;
     FindDialog *dialog;
     QPushButton *loadButton;
     QPushButton *saveButton;
     QPushButton *exportButton;



     QMap<QString, QString> contacts;
     QString oldName;
     QString oldAddress;
     Mode currentMode;

public slots:
     void addContact();
     void submitContact();
     void cancel();
     void next();
     void previous();
     void editContact();
     void removeContact();
     void findContact();
     void saveToFile();
     void loadFromFile();
     void exportAsVCard();

 };
