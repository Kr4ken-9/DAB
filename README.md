# TatsumakiFarmer

NOTICE: Tatsumaki devs are spooper smart, this bot may be detected. However, if you enable randomization on everything, and use lots of custom messages, you should be fine.

[JS Bot](https://github.com/ajmeese7/spambot) <-- This bot is essentially the same, and is not detected to my knowledge.

Commands:

| Command | Description                            |
|:-------:|:--------------------------------------:|
| _add    | Add a channel to the farming list      |
| _remove | Remove a channel from the farming list |
| _save   | Save channels to config.yaml           |

Config Options:

| Config         | Description                                                  |
|:--------------:|:------------------------------------------------------------:|
| token          | User token for login                                         |
| channels       | List of channels to farm in                                  |
| silent         | Time before deleting farming messages                        |
| delay          | Interval of farming messages                                 |
| messages       | List of messages to use for farming                          |
| randomchannels | Whether or not to shuffle order in which channels are farmed |
| owners         | List of ids of discord users which can control the bot       |

Rep Config Options:

| Config    | Description                                                                    |
|:---------:|:------------------------------------------------------------------------------:|
| recipient | ID of discord user who will be receiving rep from the bot                      |
| channel   | ID of discord channel which the rep will be sent in                            |
| delay     | Interval (in seconds) in which the rep will be sent (random format in example) |

Additional config notes in config.yaml or repconfig.yaml
