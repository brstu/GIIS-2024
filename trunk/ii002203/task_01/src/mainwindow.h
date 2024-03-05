#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    QPixmap originalPixmap;
    QPixmap outputPixmap;
    ~MainWindow();

private slots:
    void on_buttonAddImage_clicked();

    void on_clearField_clicked();

    void on_buttonAddNoise_clicked();

    void on_buttonClearNoise_clicked();

    void on_buttonFilter_clicked();

    void on_sliderThreshold_sliderMoved(int position);

    void on_buttonSaveImage_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
