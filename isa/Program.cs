using Microsoft.AspNet.SignalR;
using Microsoft.Owin.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace isa
{
    class Program
    {
        static string url = "http://127.0.0.1:8088/";
        static void Main(string[] args)
        {            
            var SignalR = WebApp.Start(url);
            Console.ReadKey();
        }

    }
    public class IsaHub : Hub
    {

        public void Sendlocalization(string name, Boolean status)
        {
            Clients.All.statusLocalization(name, status);
        }

        public void SendLamp(string name, Boolean status)
        {
            Clients.All.statusLamp(name, status);
        }

    }
}
