using System;
using System.Collections.Generic;
using Discord;
using Discord.WebSocket;

namespace TatsumakiFarmer
{
    public class Vars
    {
        public static String Token = "";

        public static DiscordSocketClient Client;

        public static IEnumerable<ITextChannel> FarmingChannels;

        public static ITextChannel Test;

        public static Random Random;

        public static String GenerateResponse()
        {
            String GeneratedResponse = "";
            
            for(int i = 0; i < 20; i++)
                GeneratedResponse += $"{Responses[Random.Next(0, Responses.Length)]} ";

            return GeneratedResponse;
        }

        private static String[] Responses =
        {
            "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod",
            "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Sed", "turpis", "tincidunt",
            "id", "aliquet", "risus", "feugiat", "in", "ante.", "Pharetra", "pharetra", "massa", "massa", "ultricies.",
            "Risus", "commodo", "viverra", "maecenas", "accumsan", "lacus.", "Id", "faucibus", "nisl", "tincidunt",
            "eget", "nullam", "non", "nisi.", "Nibh", "tellus", "molestie", "nunc", "non", "blandit", "massa", "enim",
            "nec.", "Netus", "et", "malesuada", "fames", "ac", "turpis", "egestas.", "Dui", "sapien", "eget", "mi",
            "proin", "sed", "libero.", "Adipiscing", "commodo", "elit", "at", "imperdiet", "dui.", "Justo", "laoreet",
            "sit", "amet", "cursus", "sit.", "Mi", "proin", "sed", "libero", "enim", "sed", "faucibus", "turpis", "in.",
            "Dui", "id", "ornare", "arcu", "odio.", "Gravida", "quis", "blandit", "turpis", "cursus.", "Orci", "ac",
            "auctor", "augue", "mauris", "augue", "neque", "gravida", "in.", "Velit", "egestas", "dui", "id", "ornare",
            "arcu", "odio", "ut", "sem", "nulla.", "Varius", "quam", "quisque", "id", "diam", "vel", "quam.", "Mi",
            "ipsum", "faucibus", "vitae", "aliquet", "nec", "ullamcorper", "sit", "amet.", "Diam", "vel", "quam",
            "elementum", "pulvinar", "etiam", "non", "quam", "lacus", "suspendisse.", "Volutpat", "ac", "tincidunt",
            "vitae", "semper", "quis", "lectus", "nulla.", "Nisl", "suscipit", "adipiscing", "bibendum", "est",
            "ultricies", "integer", "quis", "auctor", "elit."
        };
    }
}