import discord, requests, time, json, os
from discord.ext import commands, tasks

def getConfig():
    if os.path.isfile("./config.json"):
        with open("./config.json", "r") as fp:
            return json.load(fp)
    else:
        NC = {"token": "INSERT_TOKEN", "prefix": "!", "guild": "GUILD_ID", "captcha": {"length": 7},
              "role": "VERIFIED_ROLE_ID"}
        with open("./config.json", "w") as fp: json.dump(NC, fp, indent=4);
        return NC

def getSavedData():
    if os.path.isfile("./data.json"):
        with open("./data.json", "r") as fp: return json.load(fp)
    else: return {}

client = commands.Bot(command_prefix="")
config = getConfig()
data = getSavedData()

def check():
    if not isinstance(config["prefix"], str) or len(config["prefix"]) < 1: print("Prefix must be a string with at least one character."); raise SystemExit
    if not isinstance(config["guild"], int):
        try:
            config["guild"] = int(config["guild"])
        except:
            print(f"Guild not found: {config['guild']}. Guild ID must be int.")
            raise SystemExit
    if not isinstance(config["captcha"]["length"], int): 
        try:
            config["captcha"]["length"] = int(config["captcha"]["length"])
        except:
            print(f"Captcha length is not a number, defaulting to 7")
            config["captcha"]["length"] = 7
    if not isinstance(config["role"], int):
        try:
            config["role"] = int(config["role"])
        except:
            print(f"Role ID {config['role']} was not found, make sure it's up-to-date!")
            raise SystemExit

check()

def gCD():
    level = "Easy"
    if (config["captcha"]["length"] > 80) or (config["captcha"]["length"] < 0): config["captcha"]["length"] = 7
    if config["captcha"]["length"] > 6: level = "Normal"
    if config["captcha"]["length"] > 9: level = "Hard"
    if config["captcha"]["length"] > 14: level = "Impossible"
    if config["captcha"]["length"] > 19: level = "Literally Impossible"
    return level

if config["token"] == "INSERT_TOKEN":
    print("A configuration file (config.json) has been generated, please set it up. \n\n[Alert] Closing in 5 seconds.")
    TIME_LEFT = 5
    for i in range(TIME_LEFT):
        print(f"[Alert] Closing in {TIME_LEFT - i} seconds.")
        time.sleep(1)
    raise SystemExit

class captcha:
    opt = {"captcha-length": str(config["captcha"]["length"])}
    limit = 3

def create_captcha():
    return requests.get("https://captcha.manx7.net/insecure/new", headers=captcha.opt).json()["response"] if requests.get("https://captcha.manx7.net/insecure/new", headers=captcha.opt).json()["response"] is not None else False


messages = {
    "captchaTitle": "{GUILD_NAME} - Verification",
    "captchaEmbed": "Hello, {USER}, we're sorry to trouble you, but to ensure the safety of our community we require you to solve this simple captcha.",
    "captchaFooter": "Captcha Verification Level: " + gCD()
}

@client.event
async def on_ready():
    print(f"Captcha client connected as {str(client.user)}! (Ready for business)")
    autoSave.start()
    messages["captchaTitle"] = messages["captchaTitle"].replace("{GUILD_NAME}", client.get_guild(int(config["guild"])).name)
    messages["captchaFooter"] = messages["captchaFooter"].replace("{GUILD_NAME}", client.get_guild(int(config["guild"])).name)
    if client.get_guild(int(config["guild"])) is None: print(f"Guild not found: {config['guild']}. Guild ID must be int."); raise SystemExit
    if client.get_guild(int(config["guild"])).get_role(int(config["role"])) is None: print(f"Role ID {config['role']} was not found on {client.get_guild(int(config['guild'])).name}, make sure it's up-to-date!"); raise SystemExit

@client.event
async def on_message(message):
    if message.author.bot: return
    channelType = str(message.channel.type).lower()
    if channelType == "text":
        if (int(message.guild.id) != int(config["guild"])): return
        if not (str(message.content).startswith(config["prefix"])): return
        args = str(message.content)[len(config["prefix"]):].split(" ")
        if args[0].lower() in ["verify", "recaptcha", "captcha", "iamhuman"]:
            if client.get_guild(int(config["guild"])).get_role(int(config["role"])) in message.author.roles:
                try:
                    return await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"You are already verified, {message.author.mention}"))
                except Exception as e: return print(e)
            else:
                try:
                    if str(message.author.id) in data:
                        return await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"You have an open session already, {message.author.mention}, check your DMs!"))
                    try:
                        res = create_captcha()
                        if not res: return print("API Down")
                        emb = discord.Embed(color=0xc5c970, title=messages["captchaTitle"], description=messages["captchaEmbed"].replace("{USER}", message.author.mention))
                        emb.set_image(url=res["raw"]); emb.set_footer(text=messages["captchaFooter"])
                        await message.author.send(embed=emb)
                        data[str(message.author.id)] = { "code": res["code"], "attempt": 0 }
                        await message.channel.send(f"Check your DMs, {message.author.mention}!", delete_after=2.25)
                    except Exception as e:
                        await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"I can't send you messages, {message.author.mention}, make sure your Direct Messages are open!"))
                        return print(e)
                except Exception as e: print(e)
    elif channelType == "private":
        if str(message.author.id) not in data:
            try:
                return await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"No session found, please create one by running `{config['prefix']}verify` in {client.get_guild(int(config['guild'])).name}!"))
            except Exception as e: print(e)
        else:
            if data[str(message.author.id)]["code"] == message.content:
                try:
                    member = await client.get_guild(int(config["guild"])).fetch_member(message.author.id)
                    del data[str(message.author.id)]
                    await member.add_roles(client.get_guild(int(config["guild"])).get_role(int(config["role"])))
                    await message.channel.send(embed=discord.Embed(color=0x70c975, description=f"Congratulations, you've been verified on {client.get_guild(int(config['guild'])).name}!"))
                except Exception as e:
                    await message.channel.send("Sorry, I was unable to grant you the verification role.")
                    print("Captcha Role Error", e)
            else:
                data[str(message.author.id)]["attempt"] += 1
                await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"The code `{message.content}` is incorrect, you have `{captcha.limit - data[str(message.author.id)]['attempt']}` attempts left."))
                captcha.limit = captcha.limit if captcha.limit > 0 else 3
                if captcha.limit - data[str(message.author.id)]["attempt"] < 1:
                    del data[str(message.author.id)]
                    await message.channel.send(embed=discord.Embed(color=0xc97070, description=f"You are out of attempts, please create a new session by running `{config['prefix']}iamhuman` in {client.get_guild(int(config['guild'])).name}!"))

@tasks.loop(seconds=30)
async def autoSave():
    try:
        with open("./data.json", "w") as fp: return json.dump(data, fp, indent=4)
    except Exception as e: print("Autosave Error: ", e)



client.run(config["token"])