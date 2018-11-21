# Sushii.yaml

Configurations options for farming Sushiibot related things. Currently
includes rep and fishies.

## Config Options:

### Booleans (True/False)

| Bool         | Description                                                        |
|:------------:|:------------------------------------------------------------------:|
| firsttime    | Used for commandline configuration, disable to configure manually  |
| repfarming   | Whether or not rep farming is enabled                              |
| fishyfarming | Whether or not fishy farming is enabled                            |

### Integers

| Integer    | Description                                                                  |
|:----------:|:----------------------------------------------------------------------------:|
| repdelay   | Interval, in seconds, in which rep is farmed in the configured channels      |
| fishydelay | Interval, in seconds, in which fishies are farmed in the configured channels |
| silent     | Delay before a farming message is deleted                                    |

### Lists

| List            | Description                          |
|:---------------:|:------------------------------------:|
| fishyrecipients | List of user ids to farm fishies for |
| reprecipients   | List of user ids to farm rep for     |

### Strings

| String  | Description                                                                                                  |
|:-------:|:------------------------------------------------------------------------------------------------------------:|
| channel | Channel id in which Sushii related things are farmed (Only one channel because they are mostly global stats) |