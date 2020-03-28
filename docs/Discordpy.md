# Discord.py

This doc explains the modifications made to discord.py and how to use the original version by Rapptz.

## What is Different In The Modified Version?

The most prominent change made to discord.py is in the [http.py](https://github.com/Rapptz/discord.py/blob/master/discord/http.py) file. Starting in the [HttpClient](https://github.com/Rapptz/discord.py/blob/master/discord/http.py#L88), the HttpClient is used for all interaction with discord. The HttpClient has a set of headers that are used for all of these ineteractions. One of them is called the user agent, which you can see being set [here](https://github.com/Rapptz/discord.py/blob/master/discord/http.py#L108).

### User Agent Changes

Looking at the user agent, you can see that it is basically just telling discord that we are using the discord.py library to interact with them:
```python
user_agent = 'DiscordBot (https://github.com/Rapptz/discord.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
```
This is no good, because we want discord to think we aren't using a bot library. To fix this, those lines are replaced with this:

`self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'`

This is a generic user agent string that you can google, it is basically just saying that the user is using Firefox on Windows 10. That should be less suspicious than a user using a "DiscordBot".

### Authorization Changes

Another header, like the user agent, is called "Authorization." This is the header that your token is sent in. It can be seen being set [here](https://github.com/Rapptz/discord.py/blob/master/discord/http.py#L132):

`headers['Authorization'] = 'Bot ' + self.token if self.bot_token else self.token`

From that line we can see that discord.py is actually not just sending the token in the header. Instead, before the token, discord.py puts "Bot " in the header. Sending another clear signal to discord that the person is using a bot library to connect.

Besides that signal, why else is it a problem? Well, if you remember finding your token, you will remember finding the "Authorization" header where your token is stored. You may or may not remember that there was no "Bot " prefix in that header, just your token by itself. If you don't remember that, you can check again to see for yourself.

We want the "Authorization" header to be exactly the way it was when you found your token, so we will make the following change:

`headers['Authorization'] = self.token`

Now, there's no "Bot " prefix. Just the token.

### IDENTIFY

The next change is the biggest change, and is in a different file called [gateway.py](https://github.com/Rapptz/discord.py/blob/master/discord/gateway.py). In this file, discord.py sends an "IDENTIFY" packet to discord. And as you can imagine, it sends some identifying information about the user. You can read about the "IDENTIFY" packet and how it should interact with *bots* [here](https://discordapp.com/developers/docs/topics/gateway#identifying).

### What Should IDENTIFY Look Like?

Before we look at what discord.py sends as IDENTIFY, I'm first going to walk you through how to check what your browser is sending as IDENTIFY. In case you haven't caught on, we want all of this to look like it's coming from your browser, not a bot library.

This guide will be firefox based, because I just like firefox better. Below are the steps:
1. Open Discord tab
2. Press F12 or Ctrl + Shift + I
3. Select "Network"
4. Select "WS"
![Steps Three and Four](https://i.imgur.com/VAiWz7m.png)
5. Reload the discord tab
6. Click on the first (usually only) entry in the bottom left
7. Click Messages on the right
8. Click the message that starts with "op" and "token"
![Steps Six Through Eight](https://i.imgur.com/pqJkLbJ.png)
9. Copy the message (There are many ways to do this. Some are listed below)
    9a. Right click, and select "Copy Message"
    9b. Scroll down to "Raw Data" and copy from there

Now you have the "IDENTIFY" message, but it may be hard to read. The following steps are optional but will make it easier to read.

10. Navigate to https://jsonformatter.org/json-pretty-print
11. Paste the message on the left
12. Select "Make Pretty"
![Steps Eleven and Twelve](https://i.imgur.com/Kcs18X1.png)

Now you know what the IDENTIFY message should look like!

### What Is Discord.py Sending for IDENTIFY?

We can see what discord.py sends for the IDENTIFY message [here](https://github.com/Rapptz/discord.py/blob/master/discord/gateway.py#L285):
```python
payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'discord.py',
                    '$device': 'discord.py',
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'compress': True,
                'large_threshold': 250,
                'guild_subscriptions': self._connection.guild_subscriptions,
                'v': 3
            }
        }
```
This is basically the IDENTIFY message, although if you look at the code you can see discord.py is making some changes to this message based on conditionals afterwards. If you take a look, you can see that for "browser" and "device" discord.py is just sending, well, "discord.py".

This is different than what our browser is sending, and if you remember, we want it to send what our browser is sending. For instance, if we look back at the example of what it should look like, "browser" should be "Firefox" and "device" should be "" or an empty string.

There are also some properties that are just left out, such as "client_build_number". So, let's make some changes and make it look like what our browser is sending:
```python
payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    'os': 'Windows',
                    'browser': 'Firefox',
                    'device': '',
                    'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
                    'browser_version': '73.0',
                    'os_version': '10',
                    'referrer': '',
                    'referring_domain': '',
                    'referrer_current': '',
                    'referring_domain_current': '',
                    'release_channel': 'stable',
                    'client_build_number': 56718,
                    'client_event_source': None
                },
                'presence': {
                    'status': 'online',
                    'since': 0,
                    'activities': [],
                    'afk': False
                },
                'compress': False,
            }
        }

```

There are a couple other changes to the IDENTIFY message, but they are mostly commenting out things that would be added if the user was a bot.

### How can I check these changes for myself?

First, you need to understand how my modified version of discord.py is being used instead of Rapptz's official discord.py. If you follow the README, when you are preparing to use DAB you will run this command:

`python -m pip install -r requirements.txt`

This command works by installing dependencies listed in the "requirements.txt" file. So, let's have a look at [requirements.txt]():
```
git+https://github.com/Kr4ken-9/discord.py@00745a755c3e425f3f2317e2e7c9ce61f5188128
pyyaml
requests
Pillow
imagehash
````

Specifically, we are going to look at the first line:

`git+https://github.com/Kr4ken-9/discord.py@00745a755c3e425f3f2317e2e7c9ce61f5188128`

What this line means is that the dependency is located at https://github.com/Kr4ken-9/discord.py and the commit # we want to use is `00745a755c3e425f3f2317e2e7c9ce61f5188128`. If you want to use the official discord.py, you can actually change this line, which will be explained later.

Now that we understand where the dependency (in this case the modified discord.py) is being installed from, checking the changes is as simple as following some links:

The repository for the modified version can be found [here](https://github.com/Kr4ken-9/discord.py). 
The branch with all the changes is called "misc" and can be found [here](https://github.com/Kr4ken-9/discord.py/tree/misc).
All of the changes, listed as commits, can be viewed [here](https://github.com/Kr4ken-9/discord.py/commits/misc).
Finally, when you click on commits (for example [here](https://github.com/Kr4ken-9/discord.py/commit/05e606002f2e25b4039847abb160488fc93961d8) and [here](https://github.com/Kr4ken-9/discord.py/commit/00745a755c3e425f3f2317e2e7c9ce61f5188128)), you can view all the changes made:

![Example Changes](https://i.imgur.com/H5U2kOw.png)

### How Do I Use The Official Discord.py?

In the case that you want to use Rapptz's official discord.py, I will provide instructions below. However, I would first have you consider that discord has a strong stance against self-bots (going so far as to threaten account termination). And, after reading this document, it should be obvious how using bot libraries (in this instance discord.py) will make it extremely obvious to discord that you are using a self-bot.

That being said, I am not claiming that by using the modified discord.py will completely fool discord into thinking you are a legitimate human user. However, the changes that have been explained in this document should speak for themselves in how they make it more difficult for discord to determine that you are using a bot library.

However, you should consider that while you are using discord.py (or any bot library in general), almost everything you do in discord (for example, sending messages, changing channels) will practically shout from the rooftops (via headers) to discord that you are using a bot library.

Anyway, onto the instructions:
1. Navigate to https://github.com/Rapptz/discord.py
2. Find the most recent working commit (for example we will just use the latest one)
![Step Two](https://i.imgur.com/cAsmQLs.png)
3. Copy the commit hash for the selected commit
![Step Three](https://i.imgur.com/YcnMGmt.png)
4. Find your local copy of requirements.txt
5. Change Kr4ken-9 to Rapptz
6. Change the commit hash to the new one you copied
![Steps Five and Six](https://i.imgur.com/LkQtc9V.gif)
7. Run `python -m pip install -r requirements.txt --upgrade`
