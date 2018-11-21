# Sushii.yaml

Configurations options for farming Sushiibot related things. Currently
includes rep and fishies.

## Config Options:

### Booleans (True/False)

| Bool      | Description                                                        |
|:---------:|:------------------------------------------------------------------:|
| firsttime | Used for commandline configuration, disable to configure manually  |
| enabled   | Whether or not all Pokecord related farming is enabled             |
| autocatch | Whether or not automatic Pokemon catching is enabled               |

### Integers

| Integer          | Description                                                                  |
|:----------------:|:----------------------------------------------------------------------------:|
| autocatchdelay   | Delay, in seconds, before Pokemon are automatically caught                   |
| silent           | Delay before a farming message is deleted                                    |

### Lists

| List     | Description                                          |
|:--------:|:----------------------------------------------------:|
| channels | List of channel ids to do Pokecord related things in |

### Dictionaries (Key: Value)

| Dictionary | Description                                                       |
|:----------:|:------------------------------------------------------------------|
| prefixes   | Pokecord prefixes (values) corresponding with the channels (keys) |