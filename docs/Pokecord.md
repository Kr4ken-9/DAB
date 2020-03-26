# Pokecord.yaml

Configurations options for farming Pokecord related things. Currently supports autocatching and releasing.

Note: Blacklisting/Whitelisting must be configured manually, in the Pokecord.yaml file

## Config Options:

### Booleans (True/False)

| Bool             | Description                                                                         |
|:----------------:|:-----------------------------------------------------------------------------------:|
| firsttime        | Used for commandline configuration, disable to configure manually                   |
| enabled          | Whether or not all Pokecord related farming is enabled                              |
| autocatch        | Whether or not automatic Pokemon catching is enabled                                |
| autorelease      | Whether or not automatic releasing of configured Pokemon is enabled                 |
| lowercasepokemon | If enabled, catch pokemon using their name in lowercase (Possibly less conspicuous) |
| enablewhitelist  | Enable/Disable catching only whitelisted pokemon                                    |
| enableblacklist  | Enable/Disable ignoring blacklisted pokemon                                         |

### Integers

| Integer          | Description                                                                  |
|:----------------:|:----------------------------------------------------------------------------:|
| autocatchdelay   | Delay, in seconds, before Pokemon are automatically caught                   |
| minimumiv        | Minimum IV required for pokemon not to be discarded by autorelease           |

### Lists

| List      | Description                                                   |
|:---------:|:-------------------------------------------------------------:|
| channels  | List of channel ids to do Pokecord related things in          |
| whitelist | List of pokemon to catch (Only catch those listed)            |
| blacklist | List of pokemon to ignore (Catch anything except those listed |

### Dictionaries (Key: Value)

| Dictionary | Description                                                       |
|:----------:|:------------------------------------------------------------------|
| prefixes   | Pokecord prefixes (values) corresponding with the channels (keys) |

Additional notes [here](Additional.md)
