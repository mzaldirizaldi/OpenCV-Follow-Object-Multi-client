using System;
using System.Diagnostics;
using System.Text;
using System.Windows.Forms;
using SimpleTCP;

namespace follow_object_Winform_CS
{
    public partial class Form1 : Form
    {
        private object syncGate = new object();
        private Process process;
        private StringBuilder output = new StringBuilder();
        private bool outputChanged;
        SimpleTcpClient client;
        string DataIn;
        sbyte indexOfB;
        sbyte indexOfA;
        sbyte indexOfX;
        sbyte indexOfY;
        int StarY;
        int StarA;
        int StarB;
        string ser1, ser2, ser3, ser4;
        public Form1()
        {
            InitializeComponent();
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            System.Net.IPAddress ip = System.Net.IPAddress.Parse(tbIP.Text);
            client.Connect(tbIP.Text, Convert.ToInt32(tbPort.Text));
            btnStart.Enabled = false;
            btnStop.Enabled = true;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            lock (syncGate)
            {
                if (process != null) return;
            }

            client = new SimpleTcpClient();
            client.Delimiter = 0x13;//enter
            client.StringEncoder = Encoding.UTF8;
            client.DataReceived += Servo_DataReceived;
            DataIn = "";
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            btnStart.Enabled = true;
            btnStop.Enabled = false;
        }

        private void OnOutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            lock (syncGate)
            {
                if (sender != process) return;
                output.AppendLine(e.Data);
                if (outputChanged) return;
                outputChanged = true;
                BeginInvoke(new Action(OnOutputChanged));
            }
        }

        private void OnOutputChanged()
        {
            lock (syncGate)
            {
                //richTextBox1.Text = output.ToString();
                outputChanged = false;
            }
        }

        private void OnProcessExited(object sender, EventArgs e)
        {
            lock (syncGate)
            {
                if (sender != process) return;
                process.Dispose();
                process = null;
            }
        }

        private void Servo_DataReceived(object sender, SimpleTCP.Message e)
        {

            lblX.Invoke((MethodInvoker)delegate ()
            {
                DataIn = e.MessageString;
                if (DataIn.Length > 5)
                {
                    //tbX.Text = DataIn;
                    indexOfX = Convert.ToSByte(DataIn.IndexOf("X"));
                    ser1 = DataIn.Substring(0, indexOfX);
                    lblX.Text = ser1;

                    StarY = indexOfX + 1;
                    indexOfY = Convert.ToSByte(DataIn.IndexOf("Y"));
                    ser2 = DataIn.Substring(StarY, indexOfY - StarY);
                    lblY.Text = ser2;

                    StarA = indexOfY + 1;
                    indexOfA = Convert.ToSByte(DataIn.IndexOf("A"));
                    ser3 = DataIn.Substring(StarA, indexOfA - StarA);
                    lblAzimuth.Text = ser3 + "°";

                    StarB = indexOfA + 1;
                    indexOfB = Convert.ToSByte(DataIn.IndexOf("B"));
                    ser4 = DataIn.Substring(StarB, indexOfB - StarB);
                    lblElevasi.Text = ser4 + "°";
                }
            });
        }
    }
}
