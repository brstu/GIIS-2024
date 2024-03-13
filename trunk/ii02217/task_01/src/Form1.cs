using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace laba1Giis
{
    public partial class Form1 : Form
    {
        Image image;
        public Form1()
        {
            InitializeComponent();
            trackBar1.Maximum = 100;
            trackBar2.Maximum = 255;
            trackBar1.TickStyle = TickStyle.None;
            trackBar2.TickStyle = TickStyle.None;
        }

        private void menuStrip1_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {

        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();

            openFileDialog1.InitialDirectory = "c:\\";
            openFileDialog1.Filter = "Image files (*.png, *.jpg)|*.png;*.jpg";
            openFileDialog1.FilterIndex = 0;
            openFileDialog1.RestoreDirectory = true;

            if (openFileDialog1.ShowDialog() != DialogResult.OK)
            {
                return;

            }
            pictureBox1.Image = new Bitmap(openFileDialog1.FileName);
        }

        private void pictureBox1_SizeChanged(object sender, EventArgs e)
        {
            if (pictureBox1.Image != null)
            {
                pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            pictureBox1.SizeChanged += pictureBox1_SizeChanged;
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            label1.Text = String.Format("Уровень зашумления: {0} %", trackBar1.Value);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            image = pictureBox1.Image;
            Bitmap bmp = new Bitmap(image);
            int countPixels = pictureBox1.Image.Height * pictureBox1.Width;
            Random random = new Random();
            for (int i = 0; i < countPixels * trackBar1.Value / 100; i++)
            {
                int x = random.Next(0,bmp.Width);
                int y = random.Next(0, bmp.Height);
                Color color = (random.Next(0, 2) == 0 ? Color.Black : Color.White);
                bmp.SetPixel(x,y,color);
            }
            pictureBox1.Image = bmp;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = image;
        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            label4.Text = String.Format("Порог фильтра: {0} ", trackBar2.Value);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            
            Bitmap bmp = new Bitmap(image);
            for (int y = 0; y < bmp.Height; y++)
            {
                for (int x = 0; x < bmp.Width; x++)
                {
                    Color pixel = bmp.GetPixel(x, y);
                    int sum = 0;
                    int count = 0;
                    for (int j = -1; j <= 1; j++)
                    {
                        for (int i = -1; i <= 1; i++)
                        {
                            int newX = x + i;
                            int newY = y + j;
                            if (newX >= 0 && newX < bmp.Width && newY >= 0 && newY < bmp.Height)
                            {
                                Color neighborPixel = bmp.GetPixel(newX, newY);
                                int intensity = (neighborPixel.R + neighborPixel.G + neighborPixel.B) / 3;
                                sum += intensity;
                                count++;
                            }
                        }
                    }
                    int averageIntensity = sum / count;
                    if (Math.Abs((pixel.R + pixel.G + pixel.B) / 3 - averageIntensity) > trackBar2.Value)
                    {
                       
                        Color newPixel = Color.FromArgb(averageIntensity, averageIntensity, averageIntensity);
                        bmp.SetPixel(x, y, newPixel);
                    }
                }
            }
            pictureBox2.Image = bmp;
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }

        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
           
            saveFileDialog.Filter = "Image files (*.png, *.jpg)|*.png;*.jpg"; ;
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filename = saveFileDialog.FileName;
                if (pictureBox1.Image != null)
                {
                    pictureBox2.Image.Save(filename);
                }
                else
                {
                    MessageBox.Show("No image to save.");
                }
            }
        }
    }
}
