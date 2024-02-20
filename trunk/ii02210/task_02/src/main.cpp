#include "mainwindow.h"
#include <QApplication>
#include <QIcon>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    w.setWindowIcon(QIcon("D:/gloom/lab/c sharp/GIIS/giis_2LAB/giis_lab2/yyyy1.ico"));
    return a.exec();
}
