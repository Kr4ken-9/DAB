using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Discord;
using Discord.WebSocket;
using MessagePack;

namespace TatsumakiFarmer
{
    class Program
    {
        private static String CPath = $"{Environment.CurrentDirectory}/channels.json";

        static async Task Main(string[] args)
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

            if (!File.Exists(CPath))
            {
                ulong ID = 1337;

                while (ID == 1337)
                {
                    Console.WriteLine("Enter channel id to farm\n");
                    String SID = Console.ReadLine();

                    if (!ulong.TryParse(SID, out ID))
                    {
                        Console.WriteLine($"{SID} is not a ulong. Try Again.");
                        continue;
                    }
                }

                Vars.FarmingChannels = new[] {(ITextChannel) Vars.Client.GetChannel(ID)};
                await SaveChannels();
            }
            
            Vars.FarmingChannels = LoadChannels();
            
            CancellationToken Token = new CancellationTokenSource().Token;

            new Task(() => Farming.Farm(), Token, TaskCreationOptions.LongRunning).Start();
        }

        private static async Task Testing(SocketMessage Message)
        {
            switch (Message.Content)
            {           
                case "_farm":
                    List<ITextChannel> NewChannels = Vars.FarmingChannels.ToList();
                    NewChannels.Add((ITextChannel)Message.Channel);

                    Vars.FarmingChannels = NewChannels;
                
                    Console.WriteLine($"Channel added: {Message.Channel.Name}");
                    break;
                case "_list":
                    foreach(ITextChannel Channel in Vars.FarmingChannels)
                        Console.WriteLine($"{Channel.Guild.Name}:{Channel.Name}");
                    break;
                case "_save":
                    await SaveChannels();
                    break;
                case "_load":
                    Vars.FarmingChannels = LoadChannels();
                    break;
            }
        }

        private static IEnumerable<ITextChannel> LoadChannels()
        {
            Byte[] jsonbytes = MessagePackSerializer.FromJson(File.ReadAllText(CPath));
            Channels Channels = MessagePackSerializer.Deserialize<Channels>(jsonbytes);
                    
            List<ITextChannel> TChannels = new List<ITextChannel>();
                    
            foreach(ulong id in Channels.FarmingChannels)
                TChannels.Add((ITextChannel)Vars.Client.GetChannel(id));

            return TChannels;
        }

        private static async Task SaveChannels()
        {
            Channels C = new Channels
            {
                FarmingChannels = Vars.FarmingChannels.Select(c => c.Id)
            };
                    
            foreach(ulong chasdf in C.FarmingChannels)
                Console.WriteLine(chasdf);
                    
            String json = MessagePackSerializer.ToJson(MessagePackSerializer.Serialize(C));

            Console.WriteLine($"Saved\n{json}\nto {CPath}");
            await File.WriteAllTextAsync(CPath, json);
        }
    }
}