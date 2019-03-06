# Discord Automation Bot

## WARNING

This selfbot can get you banned from Discord and WILL get you banned from Tatsumaki. Use at your own risk. I take no responsibility for you being banned. Selfbots are against both Discord's terms of service and Tatsumaki's rules.

## D. A. B. for short

### What is DAB?

DAB is a discord selfbot that automates certain other discord bots such as:
* Tatsumaki
* Pokecord
* Sushii

DAB is written in python and uses the discord.py library.

### What does it automate?

DAB primarily automates sending messages every x seconds. This is useful for
several bots because they award users experience or credits for sending
messages every x seconds.

However, DAB is also capable of automating bot-specific things such as Tatsumaki's
rep system, Sushii's fishy system, and Pokecord's pokemon system.

### How do I use it?

First, install python 3.6+ (Instructions can be found [here](https://www.python.org/))

Then, clone the repo (Or download a release, but I won't cover that)

`git clone git@github.com:Kr4ken-9/DAB`

Next, install the requirements with pip

`python -m pip install -r requirements.txt`

Finally, run the bot with python

`python main.py`

The first time you run DAB, it will give you the option to configure it
via commandline. This feature is still in progress and is not very reliable.
You will most likely get better results configuring it manually. (See Help)

### Help

Please look at the configuration documentation to help you understand both
how to use the bot, and how it works.

[Shared.yaml Configuration](docs/Shared.md)

[Messages.yaml Configuration](docs/Messages.md)

[Tatsumaki.yaml Configuration](docs/Tatsumaki.md)

[Sushii.yaml Configuration](docs/Sushii.md)

[Pokecord.yaml Configuration](docs/Pokecord.md)

[Additional Notes](docs/Additional.md)

### Thanks

Thanks @ExtraConcentratedJuice for your single contribution: https://github.com/Kr4ken-9/DAB/commit/13c38e058818d35334307d947088c70ae5a43233
