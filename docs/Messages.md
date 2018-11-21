# Messages.yaml

Configuration options used for message farming. Message farming is
 the sending of a message in certain channels repeatedly. This farms points
 and/or levels from several bots, such as Tatsumaki.

## Config Options:

### Booleans (True/False)

| Bool           | Description                                                        |
|:--------------:|:------------------------------------------------------------------:|
| firsttime      | Used for commandline configuration, disable to configure manually  |
| enabled        | Whether or not message farming is enabled                          |
| randomchannels | Determines whether messages are sent to channels in a random order |

### Integers

| Integer | Description                                                                                 |
|:-------:|:-------------------------------------------------------------------------------------------:|
| delay   | Interval, in seconds, in which messages are sent to configured channels                     |
| silent  | Delay before a message is deleted; Can be set to false to disable deleting farming messages |

### Lists

| List       | Description                                                                                                |
|:----------:|:----------------------------------------------------------------------------------------------------------:|
| channels   | List of channel ids in which messages are sent in order to farm points                                     |
| messages   | List of messages sent to configured channels to farm points (These should be as inconspicuous as possible) |
