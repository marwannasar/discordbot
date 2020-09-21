import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '%') #make this whatever you want to be the prefix to be for the bot commands
dictionary = {}

people = ['placeholder']


# initializing the bot and setting its online status
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name='with data'))
  print('bot is ready')

# reading message and string parsing to make it usable
@client.event
async def on_message(message):
  # if they are looking to match, check if theyve sent a message b4 (in dictionary) then start matching
  
  if message.content.startswith('%match'):
    author = str(message.author)
    if author in people:
      people.remove(author)
      people.append(author)
      await client.process_commands(message)
    else:
      await message.channel.send("Add your bio before attempting to match")

  else:
    author = str(message.author) #so we know who wrote the message

    if author == 'testbot#2437': # so bot doesnt add its own messages
      pass
    elif author in people: #so that new messages don't override the bio
      pass
    else: #therefore this is their bio
      content = message.content.lower().strip().replace(" ","").splitlines()
      if len(content) == 15: #theres 15 paramaters so checks if one was added/removed
        people.append(author)
        dictionary[author] = content
      else:
        await message.channel.send("Improper input, please follow exact format")
    #print(dictionary)

# the match function
@client.command()
async def match(ctx,author=people[-1]):
  print('in match function')
  print('you:',people[-1])
  a = list(dictionary)
  #print(a)
  bestmatch = {}

  for x in a:
    mylist = []
    theirlist = []
    points = 0

    print('them:',x)
    for e in dictionary[people[-1]]:
      location = e.find(':')
      mywords = e[location+1:]
      mylist.append(mywords)
    print('MINE:',mylist)
    
    for j in dictionary[x]:
      if x == author:
        print("this is you silly :p")
      else:
        location = j.find(':')
        word = j[location+1:]
        theirlist.append(word)
    print('THEIRS:',theirlist)


    #doing the comparison and adding to dictionary b4 variables reset
    for i in range(1,15):
      #gender
      if i == 1:
        if mylist[i] == theirlist[i]:
          points +=1 
      #program
      if i == 3:
        if mylist[i] == theirlist[i]:
          points +=2
      #residence
      if i == 4:
        if mylist[i] == theirlist[i]:
          points +=1 
      #hobbies
      if i == 7:
        myh = mylist[i].split(",")
        theirh = theirlist[i].split(",")
        for z in myh:
          if z in theirh:
            points+=3
      #games
      if i == 8:
        myg = mylist[i].split(",")
        theirg = theirlist[i].split(",")
        for x in myg:
          if x in theirg:
            points+=3
      #music
      if i == 9:
        mym = mylist[i].split(",")
        theirm = theirlist[i].split(",")
        for c in mym:
          if c in theirm:
            points+=2
      #shows/movies
      if i == 10:
        mys = mylist[i].split(",")
        theirs = theirlist[i].split(",")
        for v in mys:
          if v in theirs:
            points+=3
      #sports
      if i == 11:
        mysports = mylist[i].split(",")
        theirsports = theirlist[i].split(",")
        for p in mysports:
          if p in theirsports:
            points+=3
      #food
      if i == 12:
        myf = mylist[i].split(",")
        theirf = theirlist[i].split(",")
        for l in myf:
          if l in theirf:
            points+=2
      #clean/messy
      if i == 13:
        if mylist[i] == theirlist[i]:
          points +=2
      #morning/night
      if i == 14:
        if mylist[i] == theirlist[i]:
          points +=2

    if mylist == theirlist:
      points = -1

    print('POINTS:',points)  

    bestmatch[x] = points 
  
  print(bestmatch)
  best_person = max(bestmatch, key=bestmatch.get)  

  print("YOUR BEST MATCH IS:",best_person)

  await ctx.send("you're likely to vibe with %s" %best_person)

token = os.environ.get("DISCORD_BOT_SECRET") #put your unique token here (DON'T SHARE THIS WITH OTHERS)

client.run(token)
