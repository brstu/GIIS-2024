using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Drawing.Imaging;

namespace giis_1LAB{
    public partial class Form1 : Form{
        private Bitmap originalImage;
        private Bitmap currentImage;
        private int noiseLevel;
        public Form1(){
            InitializeComponent();
            textBox1.Enter += textBox1_Enter;
            label2.Visible = false;
            label1.Visible = false;
            label3.Visible = true;
        }

        private void oPENToolStripMenuItem_Click(object sender, EventArgs e){
            if (openFileDialog1.ShowDialog() == DialogResult.OK){
                originalImage = new Bitmap(openFileDialog1.FileName);
                currentImage = new Bitmap(originalImage);
                pictureBox1.Image = currentImage;
                label3.Visible = false;
                label2.Visible = false;
                label1.Visible = true;
            }
        }

        private void sAVEToolStripMenuItem_Click(object sender, EventArgs e){
            if (saveFileDialog1.ShowDialog() == DialogResult.OK){
                try{
                    currentImage.Save(saveFileDialog1.FileName, ImageFormat.Png);
                    MessageBox.Show("Image successfully saved.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex){
                    MessageBox.Show($"Error saving the image: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
        private void textBox1_Enter(object sender, EventArgs e){ textBox1.Text = "";}
        private void button1_Click(object sender, EventArgs e){
            currentImage = new Bitmap(originalImage);
            noiseLevel = 0;
            pictureBox1.Image = currentImage;
            label3.Visible = false;
            label2.Visible = false;
            label1.Visible = true;
            
        }

        private void button2_Click(object sender, EventArgs e){
            ApplyNoise();
            pictureBox1.Image = currentImage;
            label3.Visible = false;
            label2.Visible = true;
            label1.Visible = false;
            
        }

        private void button3_Click(object sender, EventArgs e){
            ApplyThresholdFilter();
            pictureBox1.Image = currentImage;
            label3.Visible = false;
            label2.Visible = true;
            label1.Visible = false;
        }
        
        private void ApplyNoise(){
     Random random = new Random();
     noiseLevel += 10;

     BitmapData bmpData = currentImage.LockBits(new Rectangle(0, 0, currentImage.Width, currentImage.Height), ImageLockMode.ReadWrite, currentImage.PixelFormat);

     int bytesPerPixel = Image.GetPixelFormatSize(currentImage.PixelFormat) / 8;
     int byteCount = bmpData.Stride * currentImage.Height;

     byte[] rgbValues = new byte[byteCount];
     System.Runtime.InteropServices.Marshal.Copy(bmpData.Scan0, rgbValues, 0, byteCount);

     for (int i = 0; i < rgbValues.Length; i += bytesPerPixel){
         for (int j = 0; j < bytesPerPixel; j++){
             int noise = random.Next(-noiseLevel, noiseLevel + 1);
             rgbValues[i + j] = (byte)Math.Max(0, Math.Min(255, rgbValues[i + j] + noise));
         }
     }

     System.Runtime.InteropServices.Marshal.Copy(rgbValues, 0, bmpData.Scan0, byteCount);
     currentImage.UnlockBits(bmpData);
 }
        private void ApplyThresholdFilter(){
            int thresholdValue;
            if (int.TryParse(textBox1.Text, out thresholdValue)){
                BitmapData bmpData = currentImage.LockBits(new Rectangle(0, 0, currentImage.Width, currentImage.Height),
                                                           ImageLockMode.ReadWrite, currentImage.PixelFormat);

                int bytesPerPixel = Image.GetPixelFormatSize(currentImage.PixelFormat) / 8;
                int byteCount = bmpData.Stride * currentImage.Height;

                byte[] rgbValues = new byte[byteCount];
                System.Runtime.InteropServices.Marshal.Copy(bmpData.Scan0, rgbValues, 0, byteCount);

                int width = currentImage.Width;
                int height = currentImage.Height;

                for (int y = 0; y < height; y++){
                    for (int x = 0; x < width; x++){
                        
                        int sum = 0;
                        for (int offsetY = -1; offsetY <= 1; offsetY++){
                            for (int offsetX = -1; offsetX <= 1; offsetX++){
                                int pixelX = x + offsetX;
                                int pixelY = y + offsetY;

                                if (pixelX >= 0 && pixelX < width && pixelY >= 0 && pixelY < height){
                                    int index = (pixelY * width + pixelX) * bytesPerPixel;
                                    sum += rgbValues[index]; 
                                }
                            }
                        }

                        int average = sum / 9; 
                        int currentIndex = (y * width + x) * bytesPerPixel;

                        for (int j = 0; j < 3; j++){
                            int index = currentIndex + j;
                            rgbValues[index] = (byte)(rgbValues[index] < average - thresholdValue ? 0 : 255);
                        }
                    }
                }

                System.Runtime.InteropServices.Marshal.Copy(rgbValues, 0, bmpData.Scan0, byteCount);
                currentImage.UnlockBits(bmpData);
            }
            else{
                MessageBox.Show("Invalid threshold value. Please enter a valid integer.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
