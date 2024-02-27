#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->filterThreshold->setRange(0, 255);
    connect(ui->filterThreshold, &QSlider::valueChanged, this, &MainWindow::onThresholdSliderValueChanged);

    QAction *addButtonAction = findChild<QAction*>("add");
    connect(addButtonAction, &QAction::triggered, this, &MainWindow::onAddButtonClicked);

    QAction *saveButtonAction = findChild<QAction*>("save");
    connect(saveButtonAction, &QAction::triggered, this, &MainWindow::onSaveButtonClicked);

    QPushButton *addNoiseButton = findChild<QPushButton*>("addNoiseButton");
    connect(addNoiseButton, &QPushButton::clicked, this, &MainWindow::onAddNoiseButtonClicked);

    QPushButton *clearChangesButton = findChild<QPushButton*>("clearChangesButton");
    connect(clearChangesButton, &QPushButton::clicked, this, &MainWindow::onClearChangesButtonClicked);

    QPushButton *applyFilterButton = findChild<QPushButton*>("applyFilterButton");
    connect(applyFilterButton, &QPushButton::clicked, this, &MainWindow::onApplyFilterButtonClicked);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::onAddButtonClicked()
{
    QString filePath = QFileDialog::getOpenFileName(this, "Выберите изображение", "", "Images (*.png *.jpg *.bmp)");

    if (!filePath.isEmpty()) {

        originalImage.load(filePath);
        copiedImage = originalImage.copy();
        noisyImage = originalImage.copy();

        ui->before_view->setPixmap(QPixmap::fromImage(originalImage));
        ui->before_view->setScaledContents(true);

        ui->after_view->setPixmap(QPixmap::fromImage(copiedImage));
        ui->after_view->setScaledContents(true);
    }
}


void MainWindow::onSaveButtonClicked()
{
    QString saveFilePath = QFileDialog::getSaveFileName(this, "Сохранить изображение", "", "Images (*.png *.jpg *.bmp)");

    if (!saveFilePath.isEmpty()) {
        if (!noisyImage.isNull()) {
            if (noisyImage.save(saveFilePath)) {
                qDebug() << "Изображение успешно сохранено по пути: " << saveFilePath;
            } else {
                qDebug() << "Ошибка при сохранении изображения.";
            }
        } else {
            qDebug() << "Изображение не загружено.";
        }
    }
}


void MainWindow::onAddNoiseButtonClicked()
{
    float noisyLevel = ui->noisyLevel->value()/100.0;
    addImpulseNoise(noisyImage, noisyLevel);

    ui->after_view->setPixmap(QPixmap::fromImage(noisyImage));
    ui->after_view->setScaledContents(true);
}


void MainWindow::addImpulseNoise(QImage &image, float noiseLevel)
{
    if (image.isNull()) {
        return;
    }

    int width = image.width();
    int height = image.height();

    int numPixels = width * height;
    int numNoisePixels = static_cast<int>(noiseLevel * numPixels);

    for (int i = 0; i < numNoisePixels; ++i) {
        int x = QRandomGenerator::global()->bounded(width);
        int y = QRandomGenerator::global()->bounded(height);

        double rand = QRandomGenerator::global()->generateDouble();

        if (rand <= 0.3) {
            image.setPixel(x, y, qRgb(0, 0, 0)); // Добавляем "перец"
        } else if(rand > 0.3 && rand < 0.6){
            image.setPixel(x, y, qRgb(255, 255, 255)); // Добавляем "соль"
        } else {
            continue;
        }
    }
}


void MainWindow::onClearChangesButtonClicked()
{
    noisyImage = originalImage.copy();

    ui->after_view->setPixmap(QPixmap::fromImage(noisyImage));
    ui->after_view->setScaledContents(true);
}


void MainWindow::onApplyFilterButtonClicked()
{
    int thresholdValue = ui->filterThreshold->value();
    applyThresholdFilter(noisyImage, thresholdValue);

    ui->after_view->setPixmap(QPixmap::fromImage(noisyImage));
    ui->after_view->setScaledContents(true);
}

void MainWindow::applyThresholdFilter(QImage &image, int threshold)
{
    if (image.isNull()) {
        return;
    }

    int width = image.width();
    int height = image.height();

    QImage resultImage = image;

    for (int y = 1; y < height - 1; ++y) {
        for (int x = 1; x < width - 1; ++x) {
            int sum = 0;

            for (int i = -1; i <= 1; ++i) {
                for (int j = -1; j <= 1; ++j) {
                    if(i == 0 && j == 0){
                        continue;
                    }
                    QRgb color = image.pixel(x + i, y + j);
                    sum += qGray(color);
                }
            }

            int averageBrightness = sum / 8;

            if (qAbs(qGray(image.pixel(x, y)) - averageBrightness) > threshold) {
                resultImage.setPixel(x, y, qRgb(averageBrightness, averageBrightness, averageBrightness));
            }
        }
    }

    image = resultImage;
}

void MainWindow::onThresholdSliderValueChanged(int thresholdValue)
{
    ui->filterThresholdLabel->setText(QString("Порог фильтра: %1").arg(thresholdValue));
}

