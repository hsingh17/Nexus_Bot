# Nexus Bot
Discord bot that fetchs League of Legends summoner data using Riot's public API.

# Motivation
I have been playing League of Legends for years, and I really wanted to use Riot's public API in some way. So after doing some research, I decided to create a simple Discord bot that would tell the user any summoner's top 3 champion masteries and ranked gameplay W/L ratio. Along the way, I gained some experience with JSON files, YAML files, and API keys.

![Ranked Data](https://i.imgur.com/7ZWjHX0.jpg)

![Champion Mastery](https://i.imgur.com/F5RFm28.jpg)
**Note: This was primarily for fun, I do not plan on launching this bot for actual use. If you want to run the bot, you wll have to obtain your own Riot Public API key and Discord API key**

# Installation
To run the bot, you need:
1. Python3 
2. Discord.py

## Python3
To install Python3, through the terminal, use the following:

`$ sudo apt-get update`

`$ sudo apt-get install python3.6`

For Windows, follow this [link](https://www.python.org/downloads/windows/)

## Discord.py
Installing Discord.py is simple, run the following:

`$ python3 -m pip install -U discord.py`

If this does not work, visit the [discord.py website](https://discordpy.readthedocs.io/en/latest/intro.html)

# Running the Bot
After obtaining a [Riot API key](https://developer.riotgames.com/) and [Discord API key](https://discordapp.com/developers/docs/intro) simply paste them in the `sample_config.yaml` file and rename this YAML file to `config.yaml`. To run the bot, run either:

`$ python3 NexusBot.py`

or

`$ chmod +x NexutBot.py`

`$ ./NexusBot.py`

Once the bot is up and running, add the bot to the server and type `.help` to see how to use the commands.

*Project by Harjot Singh*
