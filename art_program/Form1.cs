using System.Windows.Forms;
using System;
using System.Drawing;

public class Form1 : Form
{
    private PictureBox canvasBox;
    private Bitmap canvasBitmap;
    private bool isDrawing = false;
    private Point lastPoint;
    private Pen pen;
    private Color currentColor = Color.Black;
    private Button colorButton;
    private Button clearButton;
    private TrackBar widthBar;

    // Constructor
    public Form1()
    {
    }

    // Layout of the window.
    public void FormLayout()
    {
        this.Name = "Form1";
        this.Text = "Simple Art Program";
        this.Size = new System.Drawing.Size(800, 600);
        this.StartPosition = FormStartPosition.CenterScreen;

        // Default pen settings.
        pen = new Pen(currentColor, 4f);
        pen.StartCap = System.Drawing.Drawing2D.LineCap.Round;
        pen.EndCap = System.Drawing.Drawing2D.LineCap.Round;
        pen.LineJoin = System.Drawing.Drawing2D.LineJoin.Round;

        // Creating the area on the window that has the buttons.
        var topPanel = new Panel();
        topPanel.Dock = DockStyle.Top;
        topPanel.Height = 44;
        topPanel.Padding = new Padding(6);

        // Creating the color button.
        colorButton = new Button();
        colorButton.Text = "Color";
        colorButton.AutoSize = true;
        colorButton.Click += ColorButton_Click;

        // Creating the clear button.
        clearButton = new Button();
        clearButton.Text = "Clear";
        clearButton.AutoSize = true;
        clearButton.Click += ClearButton_Click;

        // Creating the trackbar, which is the slider for the brush width.
        widthBar = new TrackBar();
        widthBar.Minimum = 1;
        widthBar.Maximum = 30;
        widthBar.Value = 4;
        widthBar.TickStyle = TickStyle.None;
        widthBar.Width = 120;
        widthBar.Scroll += WidthBar_Scroll;

        // Text that is next to slider.
        var widthLabel = new Label();
        widthLabel.Text = "Brush:";
        widthLabel.AutoSize = true;
        widthLabel.Padding = new Padding(6, 10, 6, 0);

        // Add controls to top panel
        topPanel.Controls.Add(colorButton);
        topPanel.Controls.Add(clearButton);
        topPanel.Controls.Add(widthLabel);
        topPanel.Controls.Add(widthBar);

        // Layout adjustments
        colorButton.Location = new Point(6, 6);
        clearButton.Location = new Point(colorButton.Right + 8, 6);
        widthLabel.Location = new Point(clearButton.Right + 8, 10);
        widthBar.Location = new Point(widthLabel.Right + 6, 6);

        // Canvas
        canvasBox = new PictureBox();
        canvasBox.Dock = DockStyle.Fill;
        canvasBox.BackColor = Color.White;
        canvasBox.MouseDown += CanvasBox_MouseDown;
        canvasBox.MouseMove += CanvasBox_MouseMove;
        canvasBox.MouseUp += CanvasBox_MouseUp;
        canvasBox.SizeChanged += CanvasBox_SizeChanged;

        this.Controls.Add(canvasBox);
        this.Controls.Add(topPanel);

        CreateBitmap(Math.Max(1, canvasBox.Width), Math.Max(1, canvasBox.Height));
    }

    // Creates a whitespace on the window that allows drawing.
    private void CreateBitmap(int width, int height)
    {
        if (width <= 0 || height <= 0) return;
        Bitmap newBmp = new Bitmap(width, height);
        using (Graphics g = Graphics.FromImage(newBmp))
        {
            g.Clear(Color.White);
            if (canvasBitmap != null)
            {
                g.DrawImageUnscaled(canvasBitmap, 0, 0);
            }
        }
        canvasBitmap?.Dispose();
        canvasBitmap = newBmp;
        canvasBox.Image = canvasBitmap;
    }

    // Allows the window to change size.
    private void CanvasBox_SizeChanged(object sender, EventArgs e)
    {
        CreateBitmap(Math.Max(1, canvasBox.Width), Math.Max(1, canvasBox.Height));
    }

    // Tracks if user is clicking down the left mouse button, and saves the location of where the click started.
    private void CanvasBox_MouseDown(object sender, MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left)
        {
            isDrawing = true;
            lastPoint = e.Location;
        }
    }

    // Draws the lines when the user clicks and drags the mouse.
    private void CanvasBox_MouseMove(object sender, MouseEventArgs e)
    {
        if (!isDrawing || canvasBitmap == null) return;
        using (Graphics g = Graphics.FromImage(canvasBitmap))
        {
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            g.DrawLine(pen, lastPoint, e.Location);
        }
        lastPoint = e.Location;
        canvasBox.Invalidate();
    }

    // When the user stops holding down left mouse button, stop drawing.
    private void CanvasBox_MouseUp(object sender, MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left)
            isDrawing = false;
    }

    // Creates another window for color choice.
    private void ColorButton_Click(object sender, EventArgs e)
    {
        using (ColorDialog dlg = new ColorDialog())
        {
            dlg.Color = currentColor;
            if (dlg.ShowDialog() == DialogResult.OK)
            {
                currentColor = dlg.Color;
                pen.Color = currentColor;
            }
        }
    }

    // Removes all drawings when clear button is clicked.
    private void ClearButton_Click(object sender, EventArgs e)
    {
        if (canvasBitmap == null) return;
        using (Graphics g = Graphics.FromImage(canvasBitmap))
        {
            g.Clear(Color.White);
        }
        canvasBox.Invalidate();
    }

    // Changes the size of the brush to the value in the slider.
    private void WidthBar_Scroll(object sender, EventArgs e)
    {
        if (pen != null) pen.Width = widthBar.Value;
    }
}