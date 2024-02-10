import discord
from discord.ext import commands
import os
from PIL import Image
import requests
from io import BytesIO
import json
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
class Bot(commands.Bot): 
    def __init__(self, intents: discord.Intents, **kwargs):

        super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Ready to draw !'))
        print(f"Logged in as {self.user}")
        await self.tree.sync()
bot = Bot(intents=intents)




@bot.hybrid_command(name='hello', description='Say hello!.')
@commands.has_permissions(administrator=True)
async def hello(interaction: discord.Interaction):
    await interaction.reply("Hello!")


@bot.hybrid_command(name='free_gen', description='Generate your favorite image.')
@commands.has_permissions(administrator=True)
async def free_gen(interaction: discord.Interaction, image_url, name, delay):
    if interaction.channel is not None and not interaction.channel.id == 1203245557523546133:
        await interaction.reply("You can only use this command in <#1203245557523546133>")
        return
    message = await interaction.reply("Generating your image <a:gloading:1203243862261375016>")
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]
      
    for txt_file in txt_files:
        try:
            os.remove(txt_file)
        except Exception as e:
            print(f"Error removing {txt_file}: {e}")
    
    try:
        delay_time = delay
        response = requests.get(image_url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        resized_image = image.resize((32, 32))

        pixels = resized_image.getdata()
        display_size = (256, 256)
        pixelated_image = resized_image.resize(display_size, resample=Image.NEAREST)

        buffer = BytesIO()
        pixelated_image.save(buffer, format="PNG")
        buffer.seek(0)

        data = {}
        for y in range(resized_image.height):
            for x in range(resized_image.width):
                pixel = resized_image.getpixel((x, y))
                if len(pixel) == 3:
                    r, g, b = pixel
                else:
                    r, g, b = 0, 0, 0
                data[f"{x},{y}"] = f"{{R = {r}, G = {g}, B = {b}}}"

        with open(f"{name}.txt", "w") as file:
            file.write(f"local data = {{['{name}']={{{', '.join(data.values())}}}}}\n")
            file.write(f"local Pixels = data['{name}']\n")
            file.write("local UI = game.Players.LocalPlayer.PlayerGui.MainGui.PaintFrame.GridHolder.Grid\n")
            file.write("for i,v in pairs(Pixels) do\n")
            file.write(f"    UI[i].BackgroundColor3 = Color3.fromRGB(v.R, v.G, v.B)\n")
            if delay_time is not None:
                file.write(f"    wait({delay_time})\n")
            file.write("end\n")

        with open(f"{name}.txt", "rb") as file:
            file_data = file.read()

        dpaste_response = requests.post('https://dpaste.com/api/v2/', data={'content': file_data})
        dpaste_response.raise_for_status()

        with open(f"{name}_loadstring.txt", "w") as file:
            file.write(f"loadstring(game:HttpGet('{dpaste_response.text.rstrip()}.txt'))()")

        dpaste_link = dpaste_response.text.rstrip() + '.txt'
        loadstring = (f"loadstring(game:HttpGet('{dpaste_response.text.rstrip()}.txt'))()")
        loadstri_response = requests.post('https://dpaste.com/api/v2/', data={'content': loadstring})
        link1 = loadstri_response.text.rstrip() + '.txt'
        apikey = os.environ['Cutykey']
        response = requests.get(f"https://api.cuty.io/quick?token={apikey}&url={link1}").text
        data = json.loads(response)
        link = data["short_url"]
        embed = discord.Embed(
            title=f'The art: {name} has been generated successfully\nHere is your link:',
            description=f'[[Click Here]]({link})',
            color=discord.Color.random(),
        )

        await interaction.reply(embed=embed, file=discord.File(buffer, 'pixel_art.png'))

    except Exception as e:
        await interaction.reply(f"Error: {e}")


@bot.hybrid_command(name='paid_gen', description='Generate your favourite image.')
@commands.has_permissions(administrator=True)
async def paid_gen(interaction: discord.Interaction, image_url, name, delay):
    if interaction.channel is not None and not interaction.channel.id == 1203245557523546133:
        await interaction.reply("You can only use this command in <#1203245557523546133>")
        return
    if interaction.author.roles is not None and not any(role.id == 1200702095599353866 for role in interaction.author.roles):
     await interaction.reply("You are not allowed to use this command.")
     return


      
    message = await interaction.reply("Generating your image <a:gloading:1203243862261375016>")
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]
      
    for txt_file in txt_files:
        try:
            os.remove(txt_file)
        except Exception as e:
            print(f"Error removing {txt_file}: {e}")
    
    try:
        delay_time = delay
        response = requests.get(image_url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        resized_image = image.resize((32, 32))

        pixels = resized_image.getdata()
        display_size = (256, 256)
        pixelated_image = resized_image.resize(display_size, resample=Image.NEAREST)

        buffer = BytesIO()
        pixelated_image.save(buffer, format="PNG")
        buffer.seek(0)

        data = {}
        for y in range(resized_image.height):
            for x in range(resized_image.width):
                pixel = resized_image.getpixel((x, y))
                if len(pixel) == 3:
                    r, g, b = pixel
                else:
                    r, g, b = 0, 0, 0
                data[f"{x},{y}"] = f"{{R = {r}, G = {g}, B = {b}}}"

        with open(f"{name}.txt", "w") as file:
            file.write(f"local data = {{['{name}']={{{', '.join(data.values())}}}}}\n")
            file.write(f"local Pixels = data['{name}']\n")
            file.write("local UI = game.Players.LocalPlayer.PlayerGui.MainGui.PaintFrame.GridHolder.Grid\n")
            file.write("for i,v in pairs(Pixels) do\n")
            file.write(f"    UI[i].BackgroundColor3 = Color3.fromRGB(v.R, v.G, v.B)\n")
            if delay_time is not None:
                file.write(f"    wait({delay_time})\n")
            file.write("end\n")

        with open(f"{name}.txt", "rb") as file:
            file_data = file.read()

        dpaste_response = requests.post('https://dpaste.com/api/v2/', data={'content': file_data})
        dpaste_response.raise_for_status()

        with open(f"{name}_loadstring.txt", "w") as file:
            file.write(f"loadstring(game:HttpGet('{dpaste_response.text.rstrip()}.txt'))()")

        dpaste_link = dpaste_response.text.rstrip() + '.txt'
        loadstring = (f"loadstring(game:HttpGet('{dpaste_response.text.rstrip()}.txt'))()")
        loadstri_response = requests.post('https://dpaste.com/api/v2/', data={'content': loadstring})
        link1 = loadstri_response.text.rstrip() + '.txt'
        apikey = os.environ['Cutykey']
        response = requests.get(f"https://api.cuty.io/quick?token={apikey}&url={link1}").text
        data = json.loads(response)
        link = data["short_url"]
        embed = discord.Embed(
            title=f'The art: {name} has been generated successfully\nHere is your link:',
            description=f'[[Click Here]]({link1})',
            color=discord.Color.random(),
        )
        await interaction.reply("Your image has been generated successfully. Check your DMs.")
        await interaction.author.send(embed=embed, file=discord.File(buffer, 'pixel_art.png'))
    except Exception as e:
        await interaction.reply(f"Error: {e}")
        
        
      



token = os.environ['token']

bot.run(token)
              
