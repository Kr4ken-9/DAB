using System.Collections.Generic;
using MessagePack;

namespace TatsumakiFarmer
{
    [MessagePackObject]
    public class Channels
    {
        [Key(0)]
        public IEnumerable<ulong> FarmingChannels { get; set; }
    }
}