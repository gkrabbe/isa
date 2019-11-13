using System;
using System.Threading.Tasks;
using Microsoft.Owin;
using Owin;

[assembly: OwinStartup(typeof(isa_inter.Startup))]

namespace isa_inter
{
    public class Startup
    {
        public void Configuration(IAppBuilder app)
        {
           
        }
    }
}
