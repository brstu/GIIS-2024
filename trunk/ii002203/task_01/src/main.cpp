#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.setWindowTitle("Filter");
    w.setWindowIcon(QIcon("S:/Univercity/GIIS_Labs/GIIS_Lab_1/icon.png"));
    w.show();
    return a.exec();
}
