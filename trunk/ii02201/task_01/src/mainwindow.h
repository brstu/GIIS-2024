#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QMessageBox>
#include <QImage>
#include <QRandomGenerator>

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
    ~MainWindow();

private slots:
    void onAddButtonClicked();

    void onSaveButtonClicked();

    void onAddNoiseButtonClicked();

    void onClearChangesButtonClicked();

    void onApplyFilterButtonClicked();

    void onThresholdSliderValueChanged(int value);

private:
    Ui::MainWindow *ui;
    QImage originalImage;
    QImage copiedImage;
    QImage noisyImage;
    void addImpulseNoise(QImage &image, float noiseLevel);
    void applyThresholdFilter(QImage &image, int threshold);

};
#endif // MAINWINDOW_H
