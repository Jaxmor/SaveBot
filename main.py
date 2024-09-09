import discord
from discord.ext import commands
import uuid
import requests
import shutil
import os

intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix='!', intents = intents)

@client.event
async def on_ready():
        print(f'Logged in as {client.user.name}!')
        print('------')

@client.command()
async def save(ctx):
    message = ctx.message
    folder_name = ctx.channel.name
    if not os.path.exists(folder_name):
         os.makedirs(folder_name)

         found_images = False

    async for message in ctx.channel.history(limit = 200):
        for attachment in message.attachments:
            if attachment.url[0:26] == "https://cdn.discordapp.com":
                found_images = True
                try:
                    r = requests.get(attachment.url, stream = True)
                    image_name = str(uuid.uuid4()) + '.png'
                    image_path = os.path.join(folder_name, image_name)
                    with open(image_path, 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                        print("Downloading image: " + image_name + " into folder " + folder_name)
                except Exception as e:
                    print ("Error: No Images")
                    await ctx.send("Error Downloading Images")
    if not found_images:
         await ctx.send("No images found")
         print("Error: No Images")
    else:
         await  ctx.send(f'Images saved in folder: {folder_name}')       

client.run(token) #replace 'token' with bot token