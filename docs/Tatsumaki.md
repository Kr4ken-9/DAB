# Tatsumaki.yaml

Configurations options for farming Tatsumaki related things. Right now, only
rep farming is supported.

## Config Options:

### Booleans (True/False)

| Bool       | Description                                                        |
|:----------:|:------------------------------------------------------------------:|
| firsttime  | Used for commandline configuration, disable to configure manually  |
| repfarming | Whether or not rep farming is enabled                              |

### Integers

| Integer | Description                                                             |
|:-------:|:-----------------------------------------------------------------------:|
| channel | Channel id for the channel Tatsumaki related things are automated in (Only one channel because they are mostly global stats) |
| delay   | Interval, in seconds, in which rep is farmed in the configured channels |

### Lists

| List         | Description                      |
|:------------:|:--------------------------------:|
| recipients   | List of user ids to farm rep for |

Additional notes [here](Additional.md)