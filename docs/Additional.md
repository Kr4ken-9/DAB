# Additional Notes

This doc covers common configuration options that may need more in-depth
explanations.

## Integer Delays

All integer delays are in seconds.

## Silent

Acceptable configuration options:
```yaml
silent: false
silent: [1, 5]
silent: 0
```

Silent can be configured as a boolean, list, or integer. It is the delay, in seconds
before a farming message is deleted. Or, if false, farming messages
won't be disabled. A list acts as a minimum and maximum. In the example,
1 is the minimum and 5 is the maximum. When configured as a list, the delay
will be a random number between the minimum and maximum.

Silent can be a zero, in which case messages will be deleted immediately after
being sent. Setting silent to a negative number will cause various issues.

The purpose of silent is to prevent bots such as Tatsumaki or users from
monitoring the bot's message history. When analyzed, the bot can be recognized
and blacklisted from the service. (This has happened to me) However, this does
not prevent bots from logging your messages and analyzing them that way.


## Random Channels

Acceptable configuration options:
```yaml
randomchannels: true
randomchannels: false
```

Random channels is a boolean. In order to understand it, first understand
how the bot handles farming. In any situation where a user can configure
multiple channels, the bot will loop through the configured list of channels,
and send farming messages to them in the configured order. If random channels
is configured, the list will be randomized and as such the bot will send messages
to channels in a random order.

The purpose of random channels is to make the bot seem more like a person
when scrutinized. The logic is that a bot would likely send a message to
channels in the same order, while a person might not.

## Pokecord Prefixes

Acceptable configuration options:
```yaml
prefixes: {499400204537586943: 'p!'}
prefixes: {499400204537586943: 'p!', 162005977647460481: ';'}
```

The prefixes option is important since Pokecord allows each server to have
a different prefix. Since the pokecord farmer is configured to operate in channels,
you need to specify the prefix for each channel. The easiest way to do that
is with a dictionary, or commonly known as a key value pair. The key is the
channel id `499400204537586943` in the example, and the value is the prefix
`p!` in the example.