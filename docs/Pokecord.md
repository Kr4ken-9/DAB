# Pokecord.yaml

Configurations options for farming Pokecord (formerly) related things. Currently supports autocatching and releasing.

## Life After Pokecord

As of right now, DAB supports the Pokecord clones PokeTwo and PokeRealm. All options are blanket options that apply to both until they are eventually broken up when I have time.

Note: Blacklisting/Whitelisting and Intervals must be configured manually, in the Pokecord.yaml file

## Config Options:

### Booleans (True/False)

| Bool             | Description                                                             |
|:----------------:|:-----------------------------------------------------------------------:|
| firsttime        | Used for commandline configuration, disable to configure manually       |
| enabled          | Switch for all Pokecord related farming                                 |
| pokerealm        | Switch for PokeRealm related farming                                    |
| poketwo          | Switch for PokeTwo related farming                                      |
| autocatch        | Automatically catch Pokemon in configured channels                      |
| autorelease      | Automatically release configured Pokemon                                |
| lowercasepokemon | Catch pokemon using their name in lowercase (Possibly less conspicuous) |
| intervalcatching | Automatically catch pokemon in intervals                                |
| enablewhitelist  | Catch only whitelisted pokemon                                          |
| enableblacklist  | Ignore blacklisted pokemon                                              |

### Integers

| Integer          | Description                                                        |
|:----------------:|:------------------------------------------------------------------:|
| autocatchdelay   | Delay, in seconds, before Pokemon are automatically caught         |
| minimumiv        | Minimum IV required for pokemon not to be discarded by autorelease |

### Lists

| List      | Description                                                                                                                                                |
|:---------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------:|
| channels  | Channel ids to do Pokecord related things in (applies to both PokeRealm and PokeTwo)                                                                                                            |
| whitelist | Pokemon to catch (Only catch those listed)                                                                                                                 |
| blacklist | Pokemon to ignore (Catch anything except those listed                                                                                                      |
| interval  | First number is the amount of time to automatically catch pokemon, second is the time to wait before catching them again. Both are in seconds, and repeat. |

### Dictionaries (Key: Value)

| Dictionary | Description                                                       |
|:----------:|:------------------------------------------------------------------|
| prefixes   | Pokecord prefixes (values) corresponding with the channels (keys) |

Additional notes [here](Additional.md)
