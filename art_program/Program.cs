using System;
using System.Windows.Forms;

// This is the main program that runs the art program.
// Type "dotnet run" in the terminal to run program.
public static class Program
{
    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);

        using (var form = new Form1())
        {
            form.FormLayout();
            Application.Run(form);
        }
    }
}