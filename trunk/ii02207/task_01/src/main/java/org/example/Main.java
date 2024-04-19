import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

public class Main extends JFrame {
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        System.out.println("Version: " + Core.VERSION);
    }

    private JLabel screen;
    private Mat originalImg; // для хранения первоначального изображения
    private Mat currentImg; // для текущего выбранного изображения
    private JSlider thresholdSlider;
    private int thresholdValue = 128; // Значение порога по умолчанию

    public static void main(String args[]) {
        Main window = new Main();
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.initUI();
    }

    private void initUI() {
        originalImg = Imgcodecs.imread("src/raccoon.png");
        currentImg = originalImg.clone();

        screen = new JLabel();
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(3, 3)); // установка сетки 3х3 для панели кнопок

        JButton dilateButton = new JButton("Dilate");
        dilateButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                Mat kernel = new Mat(3, 3, CvType.CV_8UC1, new Scalar(1.0));
                if (isGray(currentImg))
                {
                    currentImg = originalImg.clone();
                }
                Imgproc.dilate(currentImg, currentImg, kernel);
                updateImage(screen, currentImg);
            }
        });

        JButton erodeButton = new JButton("Erode");
        erodeButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                Mat kernel = new Mat(3, 3, CvType.CV_8UC1, new Scalar(1.0));
                if (isGray(currentImg))
                {
                    currentImg = originalImg.clone();
                }
                Imgproc.erode(currentImg, currentImg, kernel);
                updateImage(screen, currentImg);
            }
        });

        JButton grayButton = new JButton("Convert to Gray");
        grayButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                Imgproc.cvtColor(originalImg, currentImg, Imgproc.COLOR_BGR2GRAY);
                updateImage(screen, currentImg);
            }
        });

        JButton blurButton = new JButton("Apply Gaussian Blur");
        blurButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                Imgproc.GaussianBlur(originalImg, currentImg, new Size(15, 15), 0);
                updateImage(screen, currentImg);
            }
        });

        JButton thresholdButton = new JButton("Apply Threshold");
        thresholdButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                applyThreshold();
            }
        });

        JButton originalButton = new JButton("Original photo");
        originalButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                currentImg = originalImg.clone();
                updateImage(screen, currentImg);
            }
        });

        // Создание ползункового регулятора для выбора порога
        thresholdSlider = new JSlider(JSlider.HORIZONTAL, 0, 255, thresholdValue);
        Hashtable<Integer, JLabel> labelTable = new Hashtable<>();
        labelTable.put(0, new JLabel("0"));
        labelTable.put(128, new JLabel("128"));
        labelTable.put(255, new JLabel("255"));
        thresholdSlider.setLabelTable(labelTable);
        thresholdSlider.setPaintLabels(true);
        thresholdSlider.addChangeListener(new ChangeListener()
        {
            public void stateChanged(ChangeEvent e)
            {
                thresholdValue = thresholdSlider.getValue();
                applyThreshold();
            }
        });

        buttonPanel.add(dilateButton);
        buttonPanel.add(erodeButton);
        buttonPanel.add(grayButton);
        buttonPanel.add(blurButton);
        buttonPanel.add(thresholdButton);
        buttonPanel.add(originalButton);
        buttonPanel.add(new JLabel("Threshold:"));
        buttonPanel.add(thresholdSlider);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(screen, BorderLayout.CENTER);
        getContentPane().add(buttonPanel, BorderLayout.SOUTH);
        setSize(300, 300); // установка размера окна 300х300 пикселей
        setVisible(true);

        updateImage(screen, currentImg);
        setVisible(true);
    }

    private void applyThreshold()
    {
        Mat grayImg = new Mat();
        Imgproc.cvtColor(originalImg, grayImg, Imgproc.COLOR_BGR2GRAY);
        Mat thresholdImg = new Mat();
        Imgproc.threshold(grayImg, thresholdImg, thresholdValue, 255, Imgproc.THRESH_BINARY);
        updateImage(screen, thresholdImg);
    }

    public static void updateImage(JLabel screen, Mat img) {
        MatOfByte buf = new MatOfByte();
        Imgcodecs.imencode(".png", img, buf);
        ImageIcon ic = new ImageIcon(buf.toArray());
        screen.setIcon(ic);
        screen.repaint();
    }

    private boolean isGray(Mat img)
    {
        return img.channels() == 1;
    }
}