# WARNING: This project has been abandoned.
> It is not functional.

# Captcha for Discord! (discord.py)
A pre-built Discord bot running on [discord.py](https://discordpy.readthedocs.io/en/stable) using the [Manx7 Captcha API](https://captcha.manx7.net).

# How to set-up
The config.json should look like this after you start the bot
```json
{
    "token": "INSERT_TOKEN",
    "prefix": "!",
    "guild": "GUILD_ID",
    "captcha": {
        "length": 7
    },
    "role": "VERIFIED_ROLE_ID"
}
```
You have to replace `INSERT_TOKEN` with your bot token, you can get that from the [Discord Developers](https://discord.com/developers/applications) panel.
![image](https://user-images.githubusercontent.com/28667267/123458606-3a5d7e00-d5b3-11eb-948b-e4db5ef0679d.png)

Replace `GUILD_ID` with the ID of your server, you can get this by copying your server ID using developer mode.
![image](https://user-images.githubusercontent.com/28667267/123458898-91635300-d5b3-11eb-8bed-f54928f5cf45.png)

Replace `7` with the desired length of your code, I recommend 7 for normal difficulty and 5 for easy.

Replace `VERIFIED_ROLE_ID` with the ID of your member / verified role, you can get this (again with developer mode) in the role management tab.
![image](https://user-images.githubusercontent.com/28667267/123459282-13ec1280-d5b4-11eb-8c48-d7be51bd686c.png)

_And that's it, it should all be setup now, just open `run.cmd`!!_

# Requirements
You must have the following installed for this to work, at all.
 - [Pyhton 3](https://www.python.org/downloads/) (the microsoft store has it too, for a much easier windows installation)
 - [Help with Python 3](https://realpython.com/installing-python/) (incase you struggle with the install..like me)

# PyPI Requirements
This bot requires the following packages from [PyPI](https://pypi.org/).
 - [requests](https://pypi.org/project/requests/)
 - [discord.py](https://pypi.org/project/discord.py/)

These should automatically install when you run `run.cmd`, only on Windows though.
