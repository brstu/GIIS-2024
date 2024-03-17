#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QHBoxLayout>
#include <QFileDialog>
#include <QRandomGenerator>

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


void MainWindow::on_buttonAddImage_clicked()
{
    QString imageAddPath = QFileDialog::getOpenFileName(this, tr("Выберите изображение"), "", tr("Изображения (*.png *.jpg *.bmp)"));

    if (!imageAddPath.isEmpty()) {
        originalPixmap.load(imageAddPath);
        outputPixmap.load(imageAddPath);
        ui->originalImage->setPixmap(originalPixmap);
        ui->originalImage->setScaledContents(true);

        ui->outputImage->setPixmap(outputPixmap);
        ui->outputImage->setScaledContents(true);
    }
}

void MainWindow::on_clearField_clicked()
{
    ui->originalImage->clear();
    ui->outputImage->clear();
}


void MainWindow::on_buttonAddNoise_clicked()
{
    QImage image = outputPixmap.toImage();
    if (image.isNull()) {
        return;
    }

    int noisePercent = ui->fieldPercentNoise->text().toInt();
    if(noisePercent > 100)
        return;

    int totalPixels = image.width() * image.height();
    int pixelsToChange = (totalPixels * noisePercent) / 100;

    // Получаем координаты случайных пикселей и меняем их цвет на случайный шум
    for (int i = 0; i < pixelsToChange; ++i) {
        int x = QRandomGenerator::global()->bounded(0, image.width());
        int y = QRandomGenerator::global()->bounded(0, image.height());

        QRgb noiseColor = (QRandomGenerator::global()->bounded(2) == 0) ? qRgb(0, 0, 0) : qRgb(255, 255, 255);
        // Устанавливаем шум на случайный пиксель
        image.setPixel(x, y, noiseColor);
    }
    outputPixmap.convertFromImage(image);
    ui->outputImage->setPixmap(outputPixmap);
}


void MainWindow::on_buttonClearNoise_clicked()
{
    outputPixmap = originalPixmap;
    ui->outputImage->setPixmap(originalPixmap);
}

double checkAverageValue(QImage image, int x, int y) {
    int sum = 0;

    for (int i = -2; i <= 2; ++i) {
        for (int j = -2; j <= 2; ++j) {
            if(i == 0 && j == 0){
                continue;
            }
            QRgb color = image.pixel(x + j, y + i);
            sum += qGray(color);
        }
    }

    return sum / 24;
}


void MainWindow::on_buttonFilter_clicked()
{
    int threshold = ui->sliderThreshold->value();

    QImage image = outputPixmap.toImage();
    if (image.isNull()) {
        return;
    }


    double averageValue = 0;
    for (int y = 1; y < image.height() - 1; y++) {
        for (int x = 1; x < image.width() - 1; x++) {
            averageValue = checkAverageValue(image, x, y);
            if (qAbs(qGray(image.pixel(x, y)) - averageValue) > threshold) {
                image.setPixel(x, y, qRgb(averageValue, averageValue, averageValue));
            }
        }
    }

    outputPixmap.convertFromImage(image);
    ui->outputImage->setPixmap(outputPixmap);
}


void MainWindow::on_sliderThreshold_sliderMoved(int position)
{
    ui->valueSlider->setText(QString::number(position));
}


void MainWindow::on_buttonSaveImage_clicked()
{
    QImage image = outputPixmap.toImage();
    if (image.isNull()) {
        return;
    }

    QString imageSavePath = QFileDialog::getSaveFileName(this, tr("Сохранить изображение"), "", tr("Изображения (*.png *.jpg *.bmp)"));

    if (!imageSavePath.isEmpty()) {
        if (!image.isNull()) {
            if (image.save(imageSavePath)) {
                qDebug() << "Изображение успешно сохранено по пути: " << imageSavePath;
            } else {
                qDebug() << "Ошибка при сохранении изображения.";
            }
        } else {
            qDebug() << "Изображение не загружено.";
        }
    }
}

