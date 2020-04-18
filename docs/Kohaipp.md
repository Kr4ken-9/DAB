# Kohaipp.yaml

Configurations options for automating Kohaipp related things. Currently
includes begging, raiding, mining, and pet bonding.

## Info

Delays for all automated tasks must be adjusted manually. The delays are automatically set to comply with Kohaipp cooldowns.

Assigning a channel to each task is support but must be configured manually. By default all tasks are automated in the same channel.

## Config Options:

### Booleans (True/False)

| Bool      | Description                                                       |
|:---------:|:-----------------------------------------------------------------:|
| firsttime | Used for commandline configuration, disable to configure manually |
| enabled   | Toggles all kohaipp automation                                    |
| begging   | Toggles automating begging                                        |
| raiding   | Toggles automating raiding                                        |
| mining    | Toggles automating mining                                         |
| bonding   | Toggles automating pet bonding                                    |

### Integers

| Integer     | Description                                                       |
|:-----------:|:-----------------------------------------------------------------:|
| begchannel  | Channel id for the channel begging is automated in                |
| raidchannel | Channel id for the channel raiding is automated in                |
| minechannel | Channel id for the channel mining is automated in                 |
| bondchannel | Channel id for the channel bonding is automated in                |
| begdelay    | Interval in which begging is automated in the configured channels |
| raiddelay   | Interval in which raiding is automated in the configured channels |
| minedelay   | Interval in which mining is automated in the configured channels  |
| bonddelay   | Interval in which bonding is automated in the configured channels |

Additional notes [here](Additional.md)
