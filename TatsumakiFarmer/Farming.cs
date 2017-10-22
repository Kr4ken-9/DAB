using System;
using System.Threading;
using System.Threading.Tasks;

namespace TatsumakiFarmer
{
    public class Farming
    {
        public static async Task Farm()
        {
            while (Vars.FarmingChannels.Length != 0)
            {
                for (int i = 0; i < Vars.FarmingChannels.Length; i++)
                    Vars.FarmingChannels[i].SendMessageAsync(Vars.GenerateResponse());
                
                Console.WriteLine("Farming complete.");
                
                Thread.Sleep(120000);
            }
            
            Task.Delay(-1);
        }
    }
}