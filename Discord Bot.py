#!/usr/bin/env python
import discord
import random
import asyncio
import datetime
import time
import platform
from time import gmtime, strftime
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix="/")
bot.remove_command("help")


### Whitelisted servers certain commands will work in
global server; server = ['164529829490851841','530632363684659200','393652537733152768']

### Start time
global startTime; startTime = strftime("%B-%d-%Y %H:%M:%S", time.localtime())

@bot.event
async def on_ready():
    global startTime
    await bot.change_presence(game=discord.Game(name="Gaem Suxs"))
    t = datetime.datetime.now()
    print(bot.user.name + " started up at " + startTime)
    random.seed(time.time())

@bot.event
async def on_member_join(member):
    return
    #if not(str(member.id) == "155815162945863680" or str(member.id) == "183239506630017024" or str(member.id) == "155418602239950848" or str(member.id) == "161665220148723714" or str(member.id) == "286037221658853400"):
        #serverchannel = member.server.default_channel
        #await bot.send_message(serverchannel, "Welcome " + member.mention + "! \nWe hope you enjoyed having brain cells and not having tumors! \nhttps://www.youtube.com/watch?v=5jK5QBUFFYE")

@bot.event #Commands that start with numbers
async def on_message(message):
    if message.content.startswith('/5050'):
        await bot.send_message(message.channel, goodOrBad[random.randint(0,len(goodOrBad) - 1)]);
    elif message.content.startswith('/1to100'):
        await bot.send_message(message.channel, "The number is: " +  str(random.randint(1,100)))
    elif message.content.startswith('/say'):
        async for x in bot.logs_from(message.channel, limit = 1):
            await bot.delete_message(x)
        await bot.send_message(message.channel, message.content[5:])
    else:
        await bot.process_commands(message) #Other commands


@bot.command(pass_context=True)
async def f(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say(str(ctx.message.author.mention) + " has paid respects." + "\n" + "https://imgur.com/a/2B4ce")

@bot.command()
async def ping():
    global startTime
    await bot.say("Pong - " + platform.system() + " Bot started on " + startTime)

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx,person="",time=""):
    global banned
    if (time==""):
        async for x in bot.logs_from(ctx.message.channel, limit = 1):
            await bot.delete_message(x)
        await bot.say("Please enter a duration in seconds")
    else:
        await bot.start_private_message(ctx.message.mentions[0])
        await bot.send_message(ctx.message.mentions[0],"You have been soft-banned for " + str(time) + " second(s)")
        banned.append(ctx.message.mentions[0])
        banned.append(int(time))
        await bot.say("Banned "+ str(person) + " for " + str(time) + " seconds")
        await bot.kick(ctx.message.mentions[0])
        x = 0
        try:
            while (len(banned)>1):
                await bot.kick(banned[x])
                if (int(banned[x+1]) < 1 and len(banned)>1):
                    try:
                        banned.pop(x)
                        banned.pop(x)
                    except:
                        break
                else:
                    banned[x+1] = int(banned[x+1]) - 1
                if(len(banned)-(x+2) > 1):
                    x += 2
                await asyncio.sleep(1)
        except discord.Forbidden:
            await bot.say("I do not have permission to soft-ban this user")
        #except:
            #await bot.say("An error has occured. Is the user the owner or has a higher role than the bot")

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx):
    global banned
    banned = []
    await bot.say("All users that were soft-banned have been unbanned")

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def banlist(ctx):
    global banned
    string = ""
    if (len(banned) > 1):
        for x in range (0,len(banned)-1):
            string += str(banned[x]) + " is banned for " + str(banned[x+1]) + " more second(s).\n"
        await bot.say(string)
    else:
        await bot.say("No one is soft-banned in my memory")

@bot.command(pass_context=True)
async def ht(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    headsList = ["heads","tails"]
    await bot.say("The coin landed on " + headsList[random.randint(0,1)]) 


@bot.command(pass_context=True)
async def rng(ctx,num='10'):
    try:
        num =(int(num))
    except:
        await bot.say("Enter a valid number")
    await bot.say("The RNG gods have chosen from 1 to " + str(num) + ": " + str(random.randint(1,num))) 

@bot.command(pass_context=True)
async def rtd(ctx):
    await bot.say("The dice landed on " + str(random.randint(1,6))) 
        
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def bad(ctx):
    msg = [] 
    async for x in bot.logs_from(ctx.message.channel, limit = 11):
        msg.append(x)
    await bot.delete_messages(msg)


@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx,num=""):
    msg = []
    toDelete = []
    number = 0
    try:
        number = int(num) #get amount of messsages to delete
        async for x in bot.logs_from(ctx.message.channel, limit = (number+1)): #add messages at the time of creating
            toDelete.append(x)
        async for x in bot.logs_from(ctx.message.channel, limit = 1):  #add inital command for if the clear fails
            msg.append(x)
    except:
        async for x in bot.logs_from(ctx.message.channel, limit = 1):#delete initial command call
            await bot.delete_message(x)
        await bot.say("Please enter an integer")
        return
    if (number > 10): # if amount to delete is large
        await bot.say("Are you sure you want to delete " + str(number) + ' messages? Type "y" to confirm')
        async for x in bot.logs_from(ctx.message.channel, limit = 1): #add bot message to delete list
            msg.append(x)
        answer = await bot.wait_for_message(timeout=10.0, author=ctx.message.author) #wait for answer
        if (answer.content == None):
            for x in msg:
                await bot.delete_message(x) #delete current messages, not including the answer if one given
            await bot.say("No answer was given, operation canceled")
            return
        elif (answer.content.lower() == "y" or answer.content.lower() == "yes"):
            async for x in bot.logs_from(ctx.message.channel, limit = 1):  #add answer to delete list
                msg.append(x)
        else:
            async for x in bot.logs_from(ctx.message.channel, limit = 1):  #add answer to delete list
                msg.append(x)
            for x in msg:
                await bot.delete_message(x) #delete current messages, not including the answer if one given
            await bot.say("Operation Canceled")
            return
    for x in msg: #might have 1 or 2 messages to delete
        await bot.delete_message(x) #delete stored messages
    try:
        await bot.delete_messages(toDelete) #delete specified messages
        return
    except discord.ClientException:
        async for x in bot.logs_from(ctx.message.channel, limit = 1):
            await bot.delete_message(x)
        await bot.say("Can not delete messages")

            
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def k(ctx):
    try:
        victim = ctx.message.mentions[0]
        kick_channel = await bot.create_channel(ctx.message.server, "kick", type=discord.ChannelType.voice)
        await bot.move_member(victim,kick_channel)
        await bot.delete_channel(kick_channel)
    except:
        await bot.say("Enter a person to kick")


@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx):
    try:
        victim = ctx.message.mentions[0]
        kick_channel = await bot.create_channel(ctx.message.server, "kick", type=discord.ChannelType.voice)
        await bot.move_member(victim,kick_channel)
        await bot.delete_channel(kick_channel)
    except:
        await bot.say("Enter a person to kick")


@bot.command(pass_context=True)
async def rr(ctx,slot=""):
    if (ctx.message.author.voice.voice_channel is None):
        await bot.say("Join a channel, theres no point playing a risky game without a risk")
    else:
        if (slot==""):
            await bot.say("Input a number from 1-6 which slot to put the bullet in.")
        else:
            try:
                bullet = int(slot)
                if (bullet <= 6 and bullet >= 1):
                    rng = random.randint(0,5) + 1
                    await bot.say("You spin the barrel of a 6-shot revolver")
                    await asyncio.sleep(3)
                    await bot.say("You land on a slot and pull the trigger")
                    await asyncio.sleep(3)
                    if (rng == bullet):
                        await bot.say("You shot yourself. Play stupid games, win stupid prizes")
                        ded_channel = await bot.create_channel(ctx.message.server, "ded", type=discord.ChannelType.voice)
                        await bot.move_member(ctx.message.author,ded_channel)
                        await bot.delete_channel(ded_channel)
                    else:
                        await bot.say("It landed on slot " + str(rng) + ". You survived this time, that sucks.")
                else:
                    await bot.say("Enter a number from 1-6")
            except:
                await bot.say("Please enter a number")

@bot.command(pass_context=True)
async def test(ctx,slot=""):
    print(ctx.message.mentions[0])
    print(ctx.message.author)
    await bot.start_private_message(ctx.message.mentions[0])
    await bot.send_message(ctx.message.mentions[0],"You have been soft-banned for " + str(time) + " second(s)")

@bot.command(pass_context=True)
async def getserverid(ctx):
    if (str(ctx.message.author.id) == '164559470343487488'):
        await bot.say(str(ctx.message.server.id))
    
@bot.command(pass_context=True)
async def new(ctx):                           
    await bot.say("."+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+
                      "\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+".")


@bot.command(pass_context=True)
async def butwhy(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say("https://imgur.com/a/n4sFB") 

@bot.command(pass_context=True)
async def m2t(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say("http://i0.kym-cdn.com/entries/icons/original/000/021/505/mtt.jpg")

@bot.command(pass_context=True)
async def mspaint(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say(paint[random.randint(0,len(paint) - 1)]) 
    random.seed(time.time())

@bot.command(pass_context=True)
async def norussian(ctx):                      
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say("https://imgur.com/a/Ydxic") 

@bot.command(pass_context=True)
async def zach(ctx):
    global server
    for x in server:
        if (str(ctx.message.server.id) == x):
            async for x in bot.logs_from(ctx.message.channel, limit = 1):
                await bot.delete_message(x)
            await bot.say(zach[random.randint(0,len(zach) - 1)]) 
            
@bot.command(pass_context=True)
async def corgo(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say(corgi[random.randint(0,len(corgi) - 1)])  
    random.seed(time.time())

@bot.command(pass_context=True)
async def old(ctx):
    global server
    for x in server:
        if (str(ctx.message.server.id) == x):
            async for x in bot.logs_from(ctx.message.channel, limit = 1):
                await bot.delete_message(x)
            await bot.say(gull[random.randint(0,len(gull) - 1)])  

@bot.command(pass_context=True)
async def otter(ctx):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    await bot.say(otter[random.randint(0,len(otter) - 1)])  
    random.seed(time.time())

@bot.command(pass_context=True)
async def isdannyaweeb(ctx):
    global server
    for x in server:
        if (str(ctx.message.server.id) == x):
            await bot.say("Yes")

@bot.command(pass_context=True)
async def synned(ctx):
    global server
    for x in server:
        if (str(ctx.message.server.id) == x):
            await bot.say(synJoke[random.randint(0,len(synJoke)-1)])

@bot.command(pass_context=True)
async def madE(ctx,victim=""):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    if (victim==""):
        await bot.say("Please enter a name")
    else:
        weaponChoiceE = weaponsE[random.randint(0,len(weaponsE) - 4)] #3 options that wont work
        actionChoice = action[random.randint(0,len(action) - 1)]
        await bot.say(ctx.message.author.mention + " " + actionChoice + victim + " using a" + weaponChoiceE)
    
        
@bot.command(pass_context=True)
async def mad(ctx,victim=""):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    if (victim==""):
        await bot.say("Please enter a name")
    else:
        weaponChoice = weapons[random.randint(0,len(weapons) - 4)] #3 options that wont work 
        actionChoice = action[random.randint(0,len(action) - 1)]
        await bot.say(ctx.message.author.mention + " " + actionChoice + victim + " using a" + weaponChoice)
    random.seed(time.time())

        
@bot.command(pass_context=True)
async def throwE(ctx,victim=""):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    if (victim==""):
        await bot.say("Please enter a name")
    else:
        weaponChoiceE = weaponsE[random.randint(0,len(weaponsE) - 1)]
        await bot.say(ctx.message.author.mention + " throws a" + weaponChoiceE + " at" + victim)
    random.seed(time.time())

@bot.command(pass_context=True)
async def throw(ctx,victim=""):
    async for x in bot.logs_from(ctx.message.channel, limit = 1):
        await bot.delete_message(x)
    if (victim==""):
        await bot.say("Please enter a name")
    else:
        weaponChoice = weapons[random.randint(0,len(weapons) - 1)]
        await bot.say(ctx.message.author.mention + " throws a" + weaponChoice + " at" + victim)
    random.seed(time.time())
        
@bot.command(pass_context=True)
async def game(ctx):
    global server
    for x in server:
        if (str(ctx.message.server.id) == x):
            await bot.say("What game should I play?")
            answer = await bot.wait_for_message(timeout=20.0, author=ctx.message.author)
            if answer.content is None:
                await bot.say("Guess I'm not going to play any games")
            else:
                msg = [] 
                async for x in bot.logs_from(ctx.message.channel, limit = 3):
                    msg.append(x)
                await bot.delete_messages(msg)
                await bot.change_presence(game=discord.Game(name=answer.content))
    
        
@bot.command(pass_context=True)
async def commands(ctx):
    global server
    await bot.say(
            "```http\n Random Generators ```" +
            "```" +
            "/1to100                   --------------  Generates a random number between and including 1 to 100\n" +
            "/5050                     --------------  Selects either a bad or good picture. Currently " + str(len(goodOrBad)) +" different pictures\n" +
            "/ht                       --------------  Heads or tails\n" +
            "/rtd                      --------------  Rolls the dice\n" +
            "/rng #                    --------------  Picks a number from 1 to number given. Default 10.\n" +   
            "```" +
            "```http\n Moderation ```" + 
            "```" +
            "/bad                      --------------  Danny is posting porn again (deletes the past 10 messages)\n" +
            "/clear                    --------------  Deletes the previous 3 messages unless specified\n" +
            "/kick @User               --------------  Kick someone but doesnt require a new invite\n" +
            "/new                      --------------  Adds a large block of blank text to hide previous messages\n" +
            "/ban @User time(seconds)  --------------  Kicks a user for amount of seconds specified. User is kicked if they join back \n" +
            "/banlist                  --------------  Displays all users who are banned and for the amount of time they are banend for\n"+
            "/unban                    --------------  Unbans all users in the bot's list \n" +
            "```" +
            "```http\n Pictures ```" + 
            "```" +
            "/butwhy                   --------------  A bird in MS Paint\n" +
            "/f                        --------------  Pay Respects\n" +
            "/mspaint                  --------------  A random MS Paint picture\n" +
            "/norussian                --------------  NO RASSIAN\n" +
            "/otter                    --------------  Otters\n" +   
            "/corgo                    --------------  Corgi pics\n" +
            "```")
    await bot.say("```http\n Random Crap ```" +
            "```" + 
            "/mad         @User        --------------  Hurt someone with a random object, more ways to be in pain\n" +
            "/madE        @User        --------------  Hurt someone with a random object, more ways to be in pain. Changes object to an emoji\n" +
            "/throw       @User        --------------  Throws a random object, must mention a user\n" +
            "/throwE      @User        --------------  Same as throw, but you throw emojis\n" +
            "```" +
            "```http\n Games ```" + 
            "```" +
            "/game                     --------------  Changes what game the bot is playing\n" +
            "/connect4    @User        --------------  Starts a game of Connect 4. Currently moved to a new bot\n" +
            "/rr          #1-6         --------------  Russian Roulette; you get kicked if you die. Also input a number from 1-6\n" +
            "```\n")
    for x in server:
        if (str(ctx.message.server.id) == x):
            await bot.say("```http\n Others ```" +
                          "```" +
                          "/isdannyaweeb             --------------  Returns Yes\n" +
                          "/m2t                      --------------  Me too, thanks.\n" +
                          "/zach                     --------------  Zach pics\n" +
                          "/old                      --------------  Gull pics\n" +
                          "/synned                   --------------  Syn killed the family horse\n" +
                          "/game                     --------------  Changes game Bot is playing\n" +
                          "```")
    
@bot.command(pass_context=True)
async def help(ctx):
    await bot.say(
            "```http\n Random Generators ```" +
            "```" +
            "/1to100                   --------------  Generates a random number between and including 1 to 100"  +  "\n" +
            "/5050                     --------------  Selects either a bad or good picture. Currently " + str(len(goodOrBad)) +" different pictures"  +  "\n" +
            "/ht                       --------------  Heads or tails"  +  "\n" +
            "/rtd                      --------------  Rolls the dice" + "\n" +
            "/rng #                    --------------  Picks a number from 1 to number given. Default 10." + "\n" +   
            "```" +
            "```http\n Moderation ```" + 
            "```" +
            "/bad                      --------------  Danny is posting porn again (deletes the past 10 messages)\n" +
            "/clear                    --------------  Deletes the previous 3 messages unless specified\n" +
            "/kick @User               --------------  Kick someone but doesnt require a new invite\n" +
            "/new                      --------------  Adds a large block of blank text to hide previous messages\n" +
            "/ban @User time(seconds)  --------------  Kicks a user for amount of seconds specified. User is kicked if they join back \n" +
            "/banlist                  --------------  Displays all users who are banned and for the amount of time they are banend for\n"+
            "/unban                    --------------  Unbans all users in the bot's list \n" +
            "```" +
            "```http\n Pictures ```" + 
            "```" +
            "/butwhy                   --------------  A bird in MS Paint"  +  "\n" +
            "/f                        --------------  Pay Respects"  +  "\n" +
            "/mspaint                  --------------  A random MS Paint picture"  +  "\n" +
            "/norussian                --------------  NO RASSIAN"  +  "\n" +
            "/otter                    --------------  Otters" + "\n" +   
            "/corgo                    --------------  Corgi pics" + "\n" +
            "```")
    await bot.say("```http\n Random Crap ```" +
            "```" + 
            "/mad         @User        --------------  Hurt someone with a random object, more ways to be in pain" +  "\n" +
            "/madE        @User        --------------  Hurt someone with a random object, more ways to be in pain. Changes object to an emoji" +  "\n" +
            "/throw       @User        --------------  Throws a random object, must mention a user" +  "\n" +
            "/throwE      @User        --------------  Same as throw, but you throw emojis" + "\n" +
            "```" +
            "```http\n Games ```" + 
            "```" +
            "/game                     --------------  Changes what game the bot is playing" + "\n" +
            "/connect4    @User        --------------  Starts a game of Connect 4. Currently moved to a new bot"  +  "\n" +
            "/rr          #1-6         --------------  Russian Roulette; you get kicked if you die. Also input a number from 1-6"  +  "\n" +
            "```\n")
    for x in server:
        if (str(ctx.message.server.id) == x):
            await bot.say("```http\n Others ```" +
                          "```" +
                          "/isdannyaweeb             --------------  Returns Yes\n" +
                          "/m2t                      --------------  Me too, thanks.\n" +
                          "/zach                     --------------  Zach pics\n" +
                          "/old                      --------------  Gull pics\n" +
                          "/synned                   --------------  Syn killed the family horse\n" +
                          "/game                     --------------  Changes game Bot is playing\n" +
                          "```")



#---------------------------------------------Lists for Commands------------------------------------------#

synJoke = ["They asked to make a bot that does Syn jokes, it was synple they said",
           "You know, Syn would hate me for many reasyns",
           'Guyle would feel synpathetic for you, except we dont cause these jokes are aids',
           'What do you call a cold Isabelle? Frosyn',
           'I cant belleave we made a bot that specifically does this',
           "You know, she's a persyn, why do we have to do stuff like this to hurt her sanity?",
           'Salt was hoping you were syngle',
           'If you were a dried grape, you would be a raysyn',
           'If you were to set everyone involved with making this bot houses on fire, we would be trialed for arsyn',
           'I like how the bot only makes jokes about you. Doesnt it make you feel syngled out?',
           'Belle is probably syncerely disappointed at everyone involved in the making of these jokes',
           'These jokes are like the Titanic when it was Synking',
           'This was all a synister plan to make you hate us',
           "There are many theories about life and how we're probably in a synmulation",
           'There are people who study the Chinese culture. They are called Synologist.',
           "I've seen paino's tuned before, but how Isabelle tuned?",
           "What do you call a ringing device on Zach's cat? Izzy's Bell",
           "Don't you feel that sometimes when you buy something organic, that it might actually be synthetic?",
           "If you knew how to make food in the sun, I'm pretty sure thats called photoSynthesis",
           'If you tried swimming and dancing, maybe you should take up synchronized swimming',
           'I have a feeling that if you take someone hostage, they would develop Stockholm Syndrome pretty easily',
           "Making these puns wasn't easy, I had to look up Synonyms to think of some of these",
           'Did your mom ever tell you to stop cursyn? Probably not',
           "You probably would hate these jokes. It wouldn't really matter synce the jokes were already made",
           'If you are still here with us, your expectations of us has definitely not risyn',
           'Out of everyone here, you were chosyn to be pun-ished by words',
           'If you are angry that we added something to make syn jokes, you should loosyn up',
           "In half the times you died in Rust, it could have been prevented if you weren't absynt in this Discord",
           'Your reputation of us definitely worsyned ever since you joined',
           'There is a whole arsynal of puns. If you got more, feel free to add to it',
           "The bot's essynce of inspiration to make puns is people telling someone to add it",
           "The point of this bot is esyntually useless",
           ]

           

goodOrBad = ["https://imgur.com/a/30qc4", 
            "https://imgur.com/a/n8sC5",
            "https://imgur.com/a/T3mXf",
            "https://imgur.com/a/zRNEx",
            "https://imgur.com/a/4P2l8",#5
            "https://imgur.com/a/0FURP",
            "https://imgur.com/a/aWGzQ",
            "https://imgur.com/a/LsLBl",
            "https://imgur.com/a/3wANW",
            "https://imgur.com/a/0OaIs",#10
            "https://imgur.com/a/ZBpOn",
            #Bad Images/Gifs
            "https://imgur.com/a/CINb4",
            "https://imgur.com/a/sXwf7",
            "https://gfycat.com/FastPopularAfricanbushviper",
            "https://i.imgur.com/NOGHJLn.gifv",
            "https://i.imgur.com/G3p01RW.gifv",#5
            "https://imgur.com/a/SEt3r",
            "https://imgur.com/a/j17Jn",
            "https://i.imgur.com/darMoXI.gifv (He lived though)",
            "https://gfycat.com/FrequentAlienatedCaribou",
            "https://i.imgur.com/uy7cKJy.gifv",#10
            "https://i.imgur.com/y3nefos.gifv"]
                  
gull = ["https://imgur.com/a/tSdPz",
        "https://imgur.com/a/76WSV",
        'https://imgur.com/a/wO1va',
        'https://imgur.com/a/Frl7R',
        'https://imgur.com/a/ITT4I',
        'https://imgur.com/a/DWKun',
        'https://imgur.com/a/bQ5ZK',
        'https://imgur.com/a/xGvWm',
        'https://imgur.com/a/0uEQf',
        'https://imgur.com/a/06M7m',
        'https://imgur.com/a/kAXXZ',
        'https://imgur.com/a/GwOsd',
        'https://imgur.com/a/sv4dq',
        'https://imgur.com/a/tSjOD',
        'https://imgur.com/a/MNg5D']
        
weeb = ['https://imgur.com/a/uy7hv',#Taiga
        'https://imgur.com/a/tYRZW',
        'https://imgur.com/a/y4lmX',
        'https://imgur.com/a/RkR0o',
        'https://imgur.com/a/X1DVR',
        'https://imgur.com/a/TVF3V']

zach = ["https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/Bq5SE",
        "https://imgur.com/a/d6m6V",
        "https://imgur.com/a/gE1cy",
        "https://imgur.com/a/qFYzG",
        "https://imgur.com/a/Ht67C",
        "https://imgur.com/a/V8a6C",
        "https://imgur.com/a/fmqLP",
        "https://imgur.com/a/waqI1",
        "https://imgur.com/a/PQbwM",
        'https://imgur.com/a/u6rvp',
        'https://imgur.com/a/t7mjb',
        "https://imgur.com/a/d7tgk",]

paint =["https://imgur.com/a/uf218",
        "https://imgur.com/a/GJABR",
        "https://imgur.com/a/0RUjM",
        "https://imgur.com/a/gHmcc",
        "https://imgur.com/a/j9y7R",
        "https://imgur.com/a/Dl97G",
        "https://imgur.com/a/7aSNd",
        "https://imgur.com/a/8ccB8",
        "https://imgur.com/a/3RsuA",
        "https://imgur.com/a/jhPhR",
        "https://imgur.com/a/qTQWn",
        "https://imgur.com/a/VJifz",
        "https://imgur.com/a/efyYy",
        "https://imgur.com/a/D5SdU",
        "https://imgur.com/a/buvCm",
        "https://imgur.com/a/csH8o",
        "https://imgur.com/a/KVc2u",
        'https://imgur.com/a/MInLC',
        'https://imgur.com/a/UgTKt',
        'https://imgur.com/a/NMbMo',
        'https://imgur.com/a/Fg1WI',
        'https://imgur.com/a/LQyFf',
        'https://imgur.com/a/Aot22',
        'https://imgur.com/a/ZFOxJ',
        'https://imgur.com/a/s3lcx',
        'https://imgur.com/a/oYaH3',]

weapons =  [" brick",
            " bucket of salt",
            " pile of fecal matter",
            " rusty spork",
            " very small dildo",
            " potted plant",
            " pie",
            " half used syringe",
            " 1366x768 monitor",
            " pebble shaped like a dick",
            " sawblade",
            " soggy hotdog",
            " Hotwheels toy car",
            " white shoe that has been stepped on and obviously marked",
            " weaboo desu sword",
            " fidget spinner ninja star",
            " wii remote",
            " rock from Rust",
            " grenade",
            "n appology note",
            " pen that most likely hasnt been fully used",
            " used battery",
            " hot cross bun",
            " Nintendo Switch that a kid didn't get for Christmas",
            " curveball",
            " large assault rifle",
            " wrench",
            " sad trombone",
            " toilet seat",
            "n abnormaly large eraser",
            " cross of Christ",
            " half empty juice pouch of Stawberry Kool Aid",
            " ruler that has been bent slightly and cant draw straight lines anymore",
            " bouncy ball you can get at a mall gacha machine",
            " very angry Zachary",
            " hardened condom",
            " hot potato",
            " bunch of lego that you both will probably step on later",
            " tissue box",
            " car tire",
            " cum sock",
            "n anime pillow",
            #Only works for 2nd option
            " tantrum harder than a 18 year old caucasian teen who didn't get a car for her 18th birthday",
            " party because we all care about each other, except the cake is poisoned",
            " syntax error"]

weaponsE = [" :potato:",
            " :eggplant:",
            " :apple:",
            " :package:",
            " :coffin:",
            " :gun:",
            " :pick:",
            " :moneybag:",
            " :mouse_three_button:",
            " :desktop:",
            " :camera:",
            " :red_car:",
            " :boxing_glove:",
            " :trophy:",
            " :soccer:",
            " :basketball:",
            " :football:",
            " :tennis:",
            " :egg:",
            " :spoon:",
            " :lollipop:",
            " :taco:",
            " :pencil2:",
            " :scissors:",
            " :paperclip:",
            " :newspaper2:",
            " :urn:",]

action  =  ["slaps",
            "hits",
            "injures",
            "kills",
            "fists",
            "smashes",
            "cuts",
            "stabs",]

otter = ["https://imgur.com/9wcIB",
         "https://imgur.com/uJK0Iy8",
         "https://imgur.com/L8Fea",
         "https://imgur.com/FwMUEL8",
         "https://imgur.com/7Bsb1",
         'https://imgur.com/XY4EwcA',
         'https://imgur.com/pnmjMjI',
         'https://imgur.com/whvMG',
         'https://imgur.com/LrMym',
         'https://imgur.com/v4fFZ',
         'https://imgur.com/GTJCIVQ',
         'https://imgur.com/GTJCIVQ',
         'https://imgur.com/FOxcjG6',
         'https://imgur.com/rdwsaWT',
         'https://imgur.com/LXGRVdw',
         'https://imgur.com/vUIoXdf',
         'https://imgur.com/t34fjha',
         'https://imgur.com/9lo1iRB',
         'https://imgur.com/EBZkeTP',
         'https://imgur.com/XLepPYo',
         'https://imgur.com/smirnSm',
         'https://imgur.com/rdwsaWT',
         'https://imgur.com/O9EMndn',
         'https://imgur.com/O9EMndn',
         'https://imgur.com/zdL0ryy',
         'https://i.redd.it/hdbjh6pbo2jz.jpg',
         'https://i.imgur.com/rf3TUna.gifv',
         'https://i.redd.it/30vz1bwuainy.jpg',
         'https://i.imgur.com/8VDgjD3.gifv',
         'https://i.imgur.com/O4iCWTZ.gifv',
         'https://i.redd.it/40ryr1ujv6cy.jpg',
         'https://i.imgur.com/IJGtpQM.jpg',
         'https://i.imgur.com/KXqaE91.gif',
         'https://i.redd.it/9af8ctjb7lbz.jpg',
         'https://i.redd.it/9rno9smrbahy.jpg',
         'https://24.media.tumblr.com/ae51c7b24987c3043a4a608350cd510d/tumblr_mq8makdksg1qbyxr0o1_400.gif',
         'https://i.imgur.com/7u6b9CU.jpg',
         'https://i.redd.it/rkm7jq21rv6y.jpg',
         'https://i.imgur.com/PTQgZUs.gifv',
         'https://i.pinimg.com/originals/28/c0/73/28c07338bd7999dff055e20ebbc84fbf.jpg',
         'https://i.imgur.com/5YqLQYi.gifv',
         'https://gfycat.com/SneakyLeadingDarklingbeetle',
         'https://i.redd.it/b65d5k5xvd2y.png',
         'https://i.imgur.com/kLPOopc.gifv',
         'https://i.imgur.com/tGlEOAu.jpg',
         'https://i.redd.it/zzynilqtca8x.jpg',
         'https://i.redd.it/aqo68fedz1fz.jpg',
         'https://i.imgur.com/TmyZgXg.jpg',
         'https://i.redd.it/puajub0a0tiz.jpg',
         'https://i.pinimg.com/originals/15/dd/da/15dddaac3740ad66a4f6769e26e5f244.jpg',
         'https://i.imgur.com/9lo1iRB.jpg',
         'https://i.imgur.com/a71kZI4.gifv',
         'https://i.redd.it/i7c3ffay7v5y.jpg',
         'https://i.imgur.com/S64pojs.jpg',
         'https://i.redd.it/uu5slaxz1bsx.jpg',
         'https://i.imgur.com/X8CEuB3.jpg',
         'https://i.imgur.com/koFfZIf.gifv',
         'https://i.imgur.com/GHgkbWz.jpg',
         'https://i.reddituploads.com/918547f2aac84c79a21f3873e3211ef0?fit=max&h=1536&w=1536&s=30d1a64f5734b28211fa024c82d82d68',
         'https://i.imgur.com/PrAQyuW.jpg',
         'https://i.imgur.com/epPjEeG.gifv',
         'https://i.imgur.com/mIz7bNb.gifv',
         'https://i.imgur.com/eHEyjqd.jpg',
         'https://i.imgur.com/PXjZVWr.jpg',
         'https://i.imgur.com/XY4EwcA.jpg',]

corgi = ['https://imgur.com/r/corgi/d269l1Q',
         'https://imgur.com/r/corgi/xbb7tn0',
         'https://imgur.com/r/corgi/kJHpvii',
         'https://imgur.com/r/corgi/qeUxn',
         'https://imgur.com/r/corgi/Jt0ees7',
         'https://imgur.com/r/corgi/1tAeJxJ',
         'https://imgur.com/r/corgi/BVYdH3l',
         'https://imgur.com/r/corgi/WuSki',
         'https://imgur.com/r/corgi/Dd8otdV',
         'https://imgur.com/r/corgi/aeOqM',
         'https://imgur.com/r/corgi/5aKdEuN',
         'https://imgur.com/r/corgi/TzQmi9N',
         'https://i.redd.it/1og0oczt3hiz.jpg',
         'https://i.redd.it/cdgz8cwgovez.jpg',
         'https://i.reddituploads.com/30ac40687f5d410c92417658e24987ea?fit=max&h=1536&w=1536&s=504ffb13b33de9c02d3b5cb247f5e828',
         'https://i.redd.it/did4au03cbfz.jpg',
         'https://f.thumbs.redditmedia.com/Z_mNohqi5VCWL3gM.jpg',
         'https://i.redd.it/sahgcxo1eiez.jpg',
         'https://i.redd.it/kp1x1kte3ogz.jpg',
         'https://i.imgur.com/tK4ICYW.jpg',
         'https://i.redd.it/96qemycl17qy.jpg',
         'https://i.imgur.com/j7po4ZB.gifv',
         'https://i.imgur.com/6za4G7s.jpg',
         'https://i.imgur.com/63mcqGK.jpg',
         'https://i.redd.it/tpzhmka3evjz.jpg',
         'https://i.redd.it/egbplrzrmryy.jpg',
         'https://i.redd.it/h85kcqyuoidz.jpg',
         'https://i.imgur.com/uhPDZ58.jpg',
         'https://i.redd.it/fthyj2ha5e5z.jpg',
         'https://i.redd.it/gt8e36yf5k8z.jpg',
         'https://imgur.com/vE7TLA2',
         'https://imgur.com/3CBGzWy',
         'https://imgur.com/LVA1GEc',
         'https://i.redd.it/ickp7vzuwvwy.jpg',
         'https://imgur.com/v0ZzD8O',
         'https://i.imgur.com/99fM7pl.jpg',
         'https://i.redd.it/8id6srlqglky.jpg',
         'https://i.redd.it/xjd4d4rohg1z.jpg',
         'https://i.redd.it/wkosgrpg3mly.jpg',
         'https://gfycat.com/RaggedBountifulLadybug',
         'https://i.imgur.com/f9Xa8DQ.gifv',
         'https://imgur.com/xxstpMQ',
         'https://i.redd.it/80kl53x93s9z.jpg',
         'https://i.redd.it/em4kva2aapry.jpg',
         'https://i.imgur.com/WTMkOpx.jpg',
         'https://imgur.com/DbTQ6XI',
         'https://i.imgur.com/QxCL2ik.jpg',
         'https://gfycat.com/LeafyIcyArcticfox',
         'https://i.redd.it/usclv4jz944z.jpg',
         'https://i.imgur.com/XBNueYD.jpg',
         'https://i.redd.it/6z0wcrlujpez.jpg',
         'https://i.imgur.com/Pqsa4JN.gifv',
         'https://imgur.com/bg1nZ5w',
         'https://i.imgur.com/mcRZ1up.jpg',
         'https://i.redd.it/ng1f3jbdg8dz.jpg',
         'https://i.redd.it/91c2ut46368z.jpg',
         'https://gfycat.com/BaggyRingedBluegill',
         'https://imgur.com/YtdrlMy',
         'https://gfycat.com/IndelibleFatCrossbill',
         'https://i.imgur.com/yEM7KI4.jpg',
         'https://imgur.com/roOrAMG',
         'https://i.redd.it/b1g0zi82u8iz.jpg',
         'https://i.redd.it/iy08mqjcar5z.jpg',
         'https://i.imgur.com/n40tsqx.jpg',
         'https://i.imgur.com/pbCHM2w.jpg',
         'https://i.imgur.com/sfaAEoz.gifv',
         'https://i.redd.it/nuee2j01s7qz.jpg',
         'https://i.redd.it/qvagf02u9mpz.png',
         'https://i.redd.it/32z4gasy7gpz.jpg',
         'https://i.redd.it/rxzo2m2vggpz.jpg',
         'https://i.redd.it/8ucdx92hh6pz.jpg',
         'https://imgur.com/8ub4mKw',
         'https://i.redd.it/r84whz8wdmpz.jpg',
         'https://i.redd.it/vv8fjl8t3hpz.jpg',
         'https://i.redd.it/itpue7na46qz.jpg',
         'https://i.redd.it/jvfre4w7cgpz.jpg',
	]


###################################  VARIABLES  ###################################

global banned
banned = []

###################################  Connect 4  ###################################
@bot.command(pass_context=True)
async def connect4(ctx,player=""):
    msg = [] 
    async for x in bot.logs_from(ctx.message.channel, limit = 1): #delete command call
        await bot.delete_message(x)
    if (player==""):    #if no mentioned user
        await bot.say("Please enter the challenger's name")
        return
    else:
        try:                                        #get the 2 players
            challenger = ctx.message.mentions[0]    #player 1 = mentioned user
            challengerM = challenger.mention        #player 2 = challenger
        except:     #if any errors with users
            await bot.say("Please @ mention a user") 
            return
    #=================================================================  CONNECT 4 BOARD  =================================================================#
    board = ['`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',
             '`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',
             '`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',
             '`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',
             '`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',
             '`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`','`:black_large_square:`',]

    #roof = "`__________________________________________________`"
    display6 = "`|" + board[35] + "|" + board[36] + "|" + board[37] + "|" + board[38] + "|" + board[39] + "|" + board[40] + "|" + board[41] + "|`"
    display5 = "`|" + board[28] + "|" + board[29] + "|" + board[30] + "|" + board[31] + "|" + board[32] + "|" + board[33] + "|" + board[34] + "|`"
    display4 = "`|" + board[21] + "|" + board[22] + "|" + board[23] + "|" + board[24] + "|" + board[25] + "|" + board[26] + "|" + board[27] + "|`"
    display3 = "`|" + board[14] + "|" + board[15] + "|" + board[16] + "|" + board[17] + "|" + board[18] + "|" + board[19] + "|" + board[20] + "|`"
    display2 = "`|" + board[7]  + "|" + board[8]  + "|" + board[9]  + "|" + board[10] + "|" + board[11] + "|" + board[12] + "|" + board[13] + "|`"
    display1 = "`|" + board[0]  + "|" + board[1]  + "|" + board[2]  + "|" + board[3]  + "|" + board[4]  + "|" + board[5]  + "|" + board[6]  + "|`"
    #bottom = "`‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾`"
    display =  display6 + "\n" + display5 + "\n" + display4 + "\n" + display3 + "\n" + display2 + "\n" + display1 
    #=====================================================================================================================================================#
    #1d array for a 2d board, yay. Too lazy to change that, everything should work with the 1d array
    await bot.say(display + "\n" + str(ctx.message.author.mention) + " challenges " + str(challengerM) + " to a connect 4 match!\n"
                  + str(challengerM) + " goes first, type 1-7 to choose a slot. You have 15 seconds to respond")
    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add message to delete list
        msg.append(x)
    firstMove = True
    while firstMove: #while mentioned user is making a valid move
        answer = await bot.wait_for_message(timeout=15.0, author=challenger)
        if (answer is None):
            for x in msg:
                await bot.delete_message(x)
            await bot.say("Connect 4 challenge ignored")
            return
        elif (answer.content=="1" or answer.content=="2" or answer.content=="3" or answer.content=="4" or answer.content=="5" or answer.content=="6" or answer.content=="7"):
            try:
                answer = int(answer.content)
                board[answer-1] = "`:large_blue_circle:`"
                firstMove = False
                async for x in bot.logs_from(ctx.message.channel, limit = 1): #delete answer
                    await bot.delete_message(x)
                for x in msg:
                    await bot.delete_message(x) #delete board and error messages
            except: #should never happen
                bot.say("Please enter a number")
        else:
            try:
                answer = int(answer.content)
                if (answer > 7 or answer < 1):
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #delete answer
                        await bot.delete_message(x)
                    bot.say("Please enter a number between 1 and 7")
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add message to delete list
                        msg.append(x)
            except:
                async for x in bot.logs_from(ctx.message.channel, limit = 1): #delete answer
                    await bot.delete_message(x)
                bot.say("Please enter a number")
                async for x in bot.logs_from(ctx.message.channel, limit = 1): #add message to delete list
                    msg.append(x)
    msg = [] #clear delete list
    winnerFound = False
    playGame = True
    winner = ""
    turns = 1           #Check if board fills up
    refresh = False     #If error occours
    player = 1          #switch from player 1 to player 0
    skip = 0            #if players abandon game, exit program
    updateBoard = True  #refresh board
    lookForWin = True  #looks for winner if any
    while playGame: #back and forth loop between the 2 players
        if (updateBoard):
            display6 = "`|" + board[35] + "|" + board[36] + "|" + board[37] + "|" + board[38] + "|" + board[39] + "|" + board[40] + "|" + board[41] + "|`"##refresh display
            display5 = "`|" + board[28] + "|" + board[29] + "|" + board[30] + "|" + board[31] + "|" + board[32] + "|" + board[33] + "|" + board[34] + "|`"
            display4 = "`|" + board[21] + "|" + board[22] + "|" + board[23] + "|" + board[24] + "|" + board[25] + "|" + board[26] + "|" + board[27] + "|`"
            display3 = "`|" + board[14] + "|" + board[15] + "|" + board[16] + "|" + board[17] + "|" + board[18] + "|" + board[19] + "|" + board[20] + "|`"
            display2 = "`|" + board[7]  + "|" + board[8]  + "|" + board[9]  + "|" + board[10] + "|" + board[11] + "|" + board[12] + "|" + board[13] + "|`"
            display1 = "`|" + board[0]  + "|" + board[1]  + "|" + board[2]  + "|" + board[3]  + "|" + board[4]  + "|" + board[5]  + "|" + board[6]  + "|`"
            display = display6 + "\n" + display5 + "\n" + display4 + "\n" + display3 + "\n" + display2 + "\n" + display1 
            updateBoard = False
            #=============================================================  CHECK WINNING COMBOS  =============================================================#
            player0 = "`:large_blue_circle:`"
            player1 = "`:red_circle:`"
            player0win = ":regional_indicator_o:"
            player1win = ":o2:"
            c = 0   #int used to check for winning combos
            hor0 = True #player 0 horizontal
            ver0 = True #player 0 vertical
            dial0 = True #player 0 diagonal left /
            diar0 = True #player 0 diagonal right \
            hor1 = True #player 1 horizontal
            ver1 = True #player 1 vertical
            dial1 = True #player 1 diagonal left / 
            diar1 = True #player 1 diagonal right \
            if lookForWin:
                c = 0
                if (player == 1):
                    while (hor0): #horizontal player 0 (Blue)
                        if (c == 39):
                            hor0 = False
                            c = 0
                            break
                        elif (c % 7 > 3):  #move row
                            c += 3
                        elif (board[c] == player0 and board[c+1] == player0 and board[c+2] == player0 and board[c+3] == player0):
                            board[c] = player0win; board[c+1] = player0win; board[c+2] = player0win; board[c+3] = player0win
                            winner = challengerM
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break
                        else:
                            c += 1
                    while (ver0 and lookForWin): #vertical
                        if (c > 20):
                            ver0 = False
                            c = 0
                            break
                        elif (board[c] == player0 and board[c+7] == player0 and board[c+14] == player0 and board[c+21] == player0):
                            board[c] = player0win; board[c+7] = player0win; board[c+14] = player0win; board[c+21] = player0win;
                            winner = challengerM
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break
                        else:
                            c += 1
                    while (dial0 and lookForWin): #diagonal left
                        if (c == 18):
                            dial0 = False
                            c = 0
                        elif (c % 7 > 3): #move row
                            c += 3
                        elif (board[c] == player0 and board[c+8] == player0 and board[c+16] == player0 and board[c+24] == player0):
                            board[c] = player0win; board[c+8] = player0win; board[c+16] = player0win; board[c+24] = player0win
                            winner = challengerM
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break            
                        else:
                            c += 1
                    while (diar0 and lookForWin): #diagonal right
                        if (c == 21):
                            diar0 = False
                            c = 0
                        elif (c % 7 == 0):
                            c += 3
                        elif (board[c] == player0 and board[c+6] == player0 and board[c+12] == player0 and board[c+18] == player0):
                            board[c] = player0win; board[c+6] = player0win; board[c+12] = player0win; board[c+18] = player0win
                            winner = challengerM
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break            
                        else:
                            c += 1
                if (player == 0):
                    while (hor1 and lookForWin): #horizontal player 1 (Red)
                        if (c == 39):
                            hor1 = False
                            c = 0
                        elif (c % 7 > 3):  #move row
                            c += 3
                        elif (board[c] == player1 and board[c+1] == player1 and board[c+2] == player1 and board[c+3] == player1):
                            board[c] = player1win; board[c+1] = player1win; board[c+2] = player1win; board[c+3] = player1win
                            winner = ctx.message.author.mention
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break            
                        else:
                            c += 1
                    while (ver1 and lookForWin): #vertical
                        if (c > 20):
                            ver1 = False
                            c = 0
                        elif (board[c] == player1 and board[c+7] == player1 and board[c+14] == player1 and board[c+21] == player1):
                            board[c] = player1win; board[c+7] = player1win; board[c+14] = player1win; board[c+21] = player1win;
                            winner = ctx.message.author.mention
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break
                        else:
                            c += 1
                    while (dial1 and lookForWin): #diagonal left
                        if (c == 18):
                            dial1 = False
                            c = 0
                        elif (c % 7 > 3):  #move row
                            c += 3
                        elif (board[c] == player1 and board[c+8] == player1 and board[c+16] == player1 and board[c+24] == player1):
                            board[c] = player1win; board[c+8] = player1win; board[c+16] = player1win; board[c+24] = player1win
                            winner = ctx.message.author.mention
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break            
                        else:
                            c += 1
                    while (diar1 and lookForWin): #diagonal right
                        if (c == 21):
                            diar1 = False
                            c = 0
                        elif (c % 7 == 0):
                            c += 3
                        elif (board[c] == player1 and board[c+6] == player1 and board[c+12] == player1 and board[c+18] == player1):
                            board[c] = player1win; board[c+6] = player1win; board[c+12] = player1win; board[c+18] = player1win
                            winner = ctx.message.author.mention
                            lookForWin = False
                            winnerFound = True
                            player = 2 #bypass player detection
                            break            
                        else:
                            c += 1 
        #==================================================================================================================================================#
        if (skip == 2 or turns == 42): #if both players skip or board is full
            playGame = False
            winnerFound = False
        elif (refresh): #switch playing user, used to give 2nd chance
            if (player == 1):
                player = 0
                refresh = False
            elif (player == 0):
                player = 1
                refresh = False
        elif (player == 1):
            await bot.say(display + "\n" + "Its " + str(ctx.message.author.mention) + " turn, choose a number from 1-7. You have 30 seconds to answer")
            async for x in bot.logs_from(ctx.message.channel, limit = 1):
               msg.append(x)
            answer = await bot.wait_for_message(timeout=30.0, author=ctx.message.author)
            if (answer is None):
                skip += 1
                await bot.delete_message(msg)
                await bot.say("You took too long, skipping turn.")
                player = 0
            elif (answer.content=="1" or answer.content=="2" or answer.content=="3" or answer.content=="4" or answer.content=="5" or answer.content=="6" or answer.content=="7"):
                try:
                    answer = int(answer.content)
                    while (player == 1):
                        if (board[answer-1] is '`:black_large_square:`'):
                            board[answer-1] = "`:red_circle:`"
                            updateBoard = True
                            skip = 0
                            player = 0
                            turns += 1
                            lookForWin = True
                            async for x in bot.logs_from(ctx.message.channel, limit = 1):
                               msg.append(x)
                            for x in msg:
                                await bot.delete_message(x)
                        else:
                            while (board[answer-1] is not '`:black_large_square:`'):
                                answer += 7
                                if (answer > 42):
                                    player = 0
                                    refresh = True
                                    async for x in bot.logs_from(ctx.message.channel, limit = 1):
                                       msg.append(x)
                                    for x in msg:
                                        await bot.delete_message(x)
                                    await bot.say("You cant place a chip here")
                                    async for x in bot.logs_from(ctx.message.channel, limit = 1):
                                       msg.append(x)
                except:
                    bot.say("Please enter a number")
            else:
                try:
                    answer = int(answer.content)
                    if (answer > 7 or answer < 1):
                        async for x in bot.logs_from(ctx.message.channel, limit = 1): #add invalid answer to delete list
                            msg.append(x)
                        for x in msg:   #delete invalid answer
                            await bot.delete_message(x)
                        bot.say("Please enter a number between 1 and 7")
                        async for x in bot.logs_from(ctx.message.channel, limit = 1): #add output statement to delete list
                            msg.append(x)
                except:
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add invalid answer to delete list
                       msg.append(x)
                    for x in msg: #delete invalid answer
                        await bot.delete_message(x)
                    bot.say("Please enter a number")
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add output statement to delete list
                        msg.append(x)
                    
        elif (player == 0):
            await bot.say(display + "\n" + "Its " + str(challengerM) + " turn, choose a number from 1-7. You have 30 seconds to answer")
            answer = await bot.wait_for_message(timeout=30.0, author=challenger)
            if (answer is None):
                skip += 1
                await bot.delete_message(msg)
                await bot.say("You took too long, skipping turn.")
                player = 1
            elif (answer.content=="1" or answer.content=="2" or answer.content=="3" or answer.content=="4" or answer.content=="5" or answer.content=="6" or answer.content=="7"):
                try:
                    answer = int(answer.content)
                    while (player == 0):
                        if (board[answer-1] is '`:black_large_square:`'):
                            board[answer-1] = "`:large_blue_circle:`"
                            updateBoard = True
                            skip = 0
                            player = 1
                            turns += 1
                            lookForWin = True
                            async for x in bot.logs_from(ctx.message.channel, limit = 1):
                               msg.append(x)
                            for x in msg:
                                await bot.delete_message(x)
                        else:
                            while (board[answer-1] is not '`:black_large_square:`'):
                                answer += 7
                                if (answer > 42):
                                    player = 1
                                    refresh = True
                                    async for x in bot.logs_from(ctx.message.channel, limit = 1):
                                       msg.append(x)
                                    for x in msg:
                                        await bot.delete_message(x)
                                    await bot.say("You cant place a chip here")
                except:
                    bot.say("Please enter a number")
            else:
                try:
                    answer = int(answer.content)
                    if (answer > 7 or answer < 1):
                        async for x in bot.logs_from(ctx.message.channel, limit = 1): #add invalid answer to delete list
                            msg.append(x)
                        for x in msg:   #delete invalid answer
                            await bot.delete_message(x)
                        bot.say("Please enter a number between 1 and 7")
                        async for x in bot.logs_from(ctx.message.channel, limit = 1): #add output statement to delete list
                            msg.append(x)
                except:
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add invalid answer to delete list
                       msg.append(x)
                    for x in msg: #delete invalid answer
                        await bot.delete_message(x)
                    bot.say("Please enter a number")
                    async for x in bot.logs_from(ctx.message.channel, limit = 1): #add output statement to delete list
                        msg.append(x)
        elif (player == 2): ##Finish game
            updateBoard = True
            playGame = False
    if winnerFound:
        display6 = "`|" + board[35] + "|" + board[36] + "|" + board[37] + "|" + board[38] + "|" + board[39] + "|" + board[40] + "|" + board[41] + "|`"##refresh display 1 last time
        display5 = "`|" + board[28] + "|" + board[29] + "|" + board[30] + "|" + board[31] + "|" + board[32] + "|" + board[33] + "|" + board[34] + "|`"
        display4 = "`|" + board[21] + "|" + board[22] + "|" + board[23] + "|" + board[24] + "|" + board[25] + "|" + board[26] + "|" + board[27] + "|`"
        display3 = "`|" + board[14] + "|" + board[15] + "|" + board[16] + "|" + board[17] + "|" + board[18] + "|" + board[19] + "|" + board[20] + "|`"
        display2 = "`|" + board[7]  + "|" + board[8]  + "|" + board[9]  + "|" + board[10] + "|" + board[11] + "|" + board[12] + "|" + board[13] + "|`"
        display1 = "`|" + board[0]  + "|" + board[1]  + "|" + board[2]  + "|" + board[3]  + "|" + board[4]  + "|" + board[5]  + "|" + board[6]  + "|`"
        display = display6 + "\n" + display5 + "\n" + display4 + "\n" + display3 + "\n" + display2 + "\n" + display1 
        for x in msg:
            await bot.delete_message(x) #clear chat if not already
        await bot.say(display + "\n" + str(winner) + " has won!")
    else:
        for x in msg:
            await bot.delete_message(x) #clear chat if not already
        await bot.say(display + "\nMatch has ended. There are no winners")





###################################  BOT TOKEN  ###################################
bot.run('*******************************************************')

