using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Discord;
using Discord.WebSocket;

namespace TatsumakiFarmer
{
    class Program
    {
        static void Main(string[] args) => MainAsync().GetAwaiter().GetResult();

        private static async Task MainAsync()
        {
            while (String.IsNullOrWhiteSpace(Vars.Token))
            {
                Console.WriteLine("Please enter your token:");
                Vars.Token = Console.ReadLine();
            }
         
            Vars.Random = new Random();
            Vars.Client = new DiscordSocketClient();

            await Vars.Client.LoginAsync(TokenType.User, Vars.Token);
            await Vars.Client.StartAsync();

            Vars.Client.Ready += OnStart;
            Vars.Client.MessageReceived += Testing;
            
            await Task.Delay(-1);
        }

        private static async Task OnStart()
        {
            Console.WriteLine("Tatsumaki Farmer started.");
            
            Vars.Test = (SocketTextChannel) Vars.Client.GetChannel(371071699824803842);
            
            CancellationToken Token = new CancellationTokenSource().Token;

            new Task(() => Farming.Farm(), Token, TaskCreationOptions.LongRunning);
        }

        private static async Task Testing(SocketMessage Message)
        {
            switch (Message.Content)
            {
                case "_farm":
                    List<SocketTextChannel> NewChannels = Vars.FarmingChannels.ToList();
                    NewChannels.Add((SocketTextChannel)Message.Channel);

                    Vars.FarmingChannels = NewChannels.ToArray();
                
                    Console.WriteLine($"Channel added: {Message.Channel.Name}");
                    break;
                case "_list":
                    for (int i = 0; i < Vars.FarmingChannels.Length; i++)
                    {
                        SocketTextChannel Channel = Vars.FarmingChannels[i];
                        
                        Console.WriteLine($"{Channel.Guild.Name}:{Channel.Name}");
                    }
                    break;
            }
        }
    }
}