#!/usr/bin/env python3
import discord
from discord.ext import commands
import requests
import yaml
import json

#Set command prefix and remove default help command
bot = commands.Bot(command_prefix = '.')
bot.remove_command("help")

#Open config.yaml and extract API keys
with open("config.yaml", "r") as file:
    keys = yaml.load(file)
    riot_key = keys['API']['RIOT']
    discord_key = keys['API']['DISCORD']

#Open champions.json 
with open("champions.json", "r", encoding = "utf-8") as file:
    champion_data = json.load(file)

#Fetch summoner ID 
def get_summoner_id(summoner_name):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={riot_key}"
    json = requests.get(url).json()
    summoner_id = json['id']
    return summoner_id

#Fetch ranked data of all ranked queue types for the current season 
def get_summoner_data(summoner_name):
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{get_summoner_id(summoner_name)}?api_key={riot_key}"
    json = requests.get(url).json()
    data = []
    for queue_type in json:
        data.append([queue_type['queueType'], queue_type['tier'], queue_type['rank'],
                    queue_type['leaguePoints'], queue_type['wins'], queue_type['losses']])
    
    return data

#Fetch top 3 champion masteries for summoner
def get_champion_mastery_data(summoner_name):
    url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{get_summoner_id(summoner_name)}?api_key={riot_key}"
    json = requests.get(url).json()
    top_three_champs = []
    for champ in json:
        top_three_champs.append([champ['championId'], champ['championLevel'], champ['championPoints']])
        if json.index(champ) == 2:
            break
    return top_three_champs

#Create embed for .summoner_data command
async def create_summoner_embed(ctx, data, summoner_name):
    stats = discord.Embed(colour = discord.Colour.teal())
    stats.set_thumbnail(url = f"https://avatar.leagueoflegends.com/NA/{summoner_name}.png")
    stats.set_author(name = summoner_name)
    stats.add_field(name = "Queue Type", value = " ".join(data[0].split('_')), inline = False)
    stats.add_field(name = "Rank", value = f"{data[1]} {data[2]}: {data[3]} LP", inline = False)
    stats.add_field(name = "W/L", value = f"{data[4]} / {data[5]}", inline = False)
    await ctx.send(embed = stats)

#Create embed for .champion_mastery command
async def create_champ_embed(ctx, top_three_champs, summoner_name):
    mastery_banner = {
        1: "d/d8/Champion_Mastery_Level_1_Flair.png",
        2: "4/4d/Champion_Mastery_Level_2_Flair.png",
        3: "e/e5/Champion_Mastery_Level_3_Flair.png",
        4: "e/ea/Champion_Mastery_Level_4_Banner.png",
        5: "7/7e/Champion_Mastery_Level_5_Banner.png",
        6: "f/f9/Champion_Mastery_Level_6_Banner.png",
        7: "7/77/Champion_Mastery_Level_7_Banner.png"
    }
    #At first this list contains IDs for champions, after parsing JSON this list contains names of champions
    champion_ids = [top_three_champs[0][0], top_three_champs[1][0], top_three_champs[2][0]]
    for json_data in champion_data:
        if int(json_data['key']) in champion_ids:
            champion_ids[champion_ids.index(int(json_data['key']))] = json_data['name']
    
    for champ in top_three_champs:
        stats = discord.Embed(colour = discord.Colour.blurple())
        champ_name = "".join(champion_ids.pop(0).split())
        stats.set_image(url = f"https://ddragon.leagueoflegends.com/cdn/8.24.1/img/champion/{champ_name}.png")
        stats.image.width = 30
        stats.image.height = 30
        stats.set_thumbnail(url = f"https://vignette.wikia.nocookie.net/leagueoflegends/images/{mastery_banner[champ[1]]}/revision/latest?cb=20150312005319")
        stats.add_field(name = f"Mastery {champ[1]}", value = f"{champ[2]} points", inline = False)
        await ctx.send(embed = stats)

@bot.event 
async def on_ready():
    print(f"{bot.user} is now ready for use!")

@bot.command()
async def help(ctx):
    await ctx.send("```Here are the list of available commands:\n.summoner_data <name> -Finds ranked data for summoner\n.champion_mastery <name> -Finds top 3 mastered champions for summoner```")

@bot.command()
async def summoner_data(ctx, summoner_name):
    try:
        all_data = get_summoner_data(summoner_name)
        for data in all_data:
            await create_summoner_embed(ctx, data, summoner_name)
    except: 
        await ctx.send(f"```\n{summoner_name} is not a valid summoner! Please try again.```")


@bot.command()
async def champion_mastery(ctx, summoner_name):
    try:
        champion_mastery_data = get_champion_mastery_data(summoner_name)
        await create_champ_embed(ctx, champion_mastery_data, summoner_name)
    except:
        await ctx.send(f"```\n{summoner_name} is not a valid summoner! Please try again.```")

bot.run(discord_key)


