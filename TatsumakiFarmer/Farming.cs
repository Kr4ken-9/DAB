using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Discord;

namespace TatsumakiFarmer
{
    public class Farming
    {
        public static async Task Farm()
        {
            while (true)
            {
                if (!Vars.FarmingChannels.Any()) continue;
                
                foreach(ITextChannel Channel in Vars.FarmingChannels)
                    await Channel.SendMessageAsync(Vars.GenerateResponse());
                
                Thread.Sleep(120000);
            }
        }
    }
}