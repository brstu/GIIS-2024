#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QStringListModel>
#include <QFileDialog>>




MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_2_clicked()
{
    QString name = ui->textEdit->toPlainText();
    QString adres = ui->textEdit_2->toPlainText();
    QStringList stringList;
    stringList.push_back(name + ": " + adres);
    QStringListModel *model = qobject_cast<QStringListModel*>(ui->listView->model());
    if (!model) {
        model = new QStringListModel(this);
        model->setStringList(stringList);
        ui->listView->setModel(model);
    }else{
        QStringList stringListModel = model->stringList();
        stringList += stringListModel;
        model->setStringList(stringList);
    }

}


void MainWindow::on_pushButton_clicked()
{
    QModelIndex selectedIndex = ui->listView->currentIndex();
    if(selectedIndex.isValid()){
        ui->listView->model()->removeRow(selectedIndex.row());
    }

}
QVector<int> find_name(QStringListModel *model,QString name){
    QStringList stringList = model->stringList();
    QVector<int> indexes;
    for(int i = 0; i< stringList.size(); i++){
        QStringList splitName = stringList[i].split(":");
        if(splitName[0] == name){
            indexes.push_back(i);
        }
    }
    return indexes;
}


void MainWindow::on_pushButton_4_clicked()
{
    QString name = ui->textEdit->toPlainText();
    QString adres = ui->textEdit_2->toPlainText();
    QStringListModel *model = qobject_cast<QStringListModel*>(ui->listView->model());
    if(model){
        QStringList stringList = model->stringList();
        QVector<int> indexes = find_name(model,name);
        stringList[indexes.first()] = name + ": " + adres;
        model->setStringList(stringList);
    }


}




void MainWindow::on_pushButton_3_clicked()
{
   QString name = ui->textEdit_3->toPlainText();
   QStringListModel *list_veiw_model = qobject_cast<QStringListModel*>(ui->listView->model());
   QStringList stringList;
   if(list_veiw_model){
       QStringList stringList1 = list_veiw_model->stringList();
       QStringList stringList2;
       QVector<int> indexes = find_name(list_veiw_model,name);
       for(int i : indexes){
           stringList2 = stringList1[i].split(":");
           stringList.push_back(stringList2[1]);
       }
       QStringListModel *model = new QStringListModel(stringList);
       ui->listView_2->setModel(model);
   }

}


void MainWindow::on_action_triggered()
{
    QString fileName = QFileDialog::getSaveFileName(this,tr("Save file"), "C://", tr("Text (*.txt)"));
    QStringListModel *list_veiw_model = qobject_cast<QStringListModel*>(ui->listView->model());
    QFile file(fileName);
    if(file.open(QIODevice::ReadWrite)){
        QTextStream stream(&file);
        for(QString string : list_veiw_model->stringList()){
            stream << string << Qt::endl;
        }

    }

}


void MainWindow::on_action_2_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open file"), "C://", tr("Text (*.txt)"));
    QStringListModel *list_veiw_model = qobject_cast<QStringListModel*>(ui->listView->model());
    QStringList stringList;
    QStringList stringList2;
    if(!list_veiw_model){
        list_veiw_model = new QStringListModel();
        ui->listView->setModel(list_veiw_model);

    }
    QFile file(fileName);
    if(file.open(QIODevice::ReadWrite)){
        QTextStream stream(&file);
        QString str = stream.readAll();
        stringList = str.split('\n');
        for(QString string : stringList ){
            stringList2.push_back(string);
        }
        list_veiw_model->setStringList(stringList2);


    }
}

