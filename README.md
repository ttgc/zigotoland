# ZigotoBot (aka. Financial district manager)
ZigotoBot is an entertainement bot created for the discord hack week. This bot is able to create its own guild, to share it, to manage it and to allow you playing some financial games inside of it.
Once you've entered the financial district, you can play some casino games, maybe win, or maybe lose. The bank will generously give you money when you'll enter the guild.

Unfortunately, if you are bankrupt, the bank will exclude you forever from the financial district (i.e. ban). Don't hope to be allowed again, the bot won't let you enter again.

There is no real money, all of features using "money", use virtual money with no conversion from real money to virtual money or from virtual money to real money. This is just a game !

# How to install
Install at least [python3.5](https://www.python.org/downloads/) then run pip command to install dependencies :
```
pip3 install -r requirements.txt
```

# How to deploy
To run the bot you'll need a `config.json` file located at the root of the repo, put the following informations in it :
```json
{
  "token": "PUT YOUR DISCORD TOKEN HERE",
  "owner": [],
  "self-guild": {
    "ID": null,
    "mode": "create",
    "region": "us_west"
  }
}
```
Insert user ID in owner list to let theese IDs be recognized by the bot as bot owner and able to run some owner's commands (such as `/shutdown`). For the `self-guild` field, the first run need to be in `create` mode to allow bot creating the self managed guild. Once it has run, the logs will contains the ID of generated guild, reboot the bot by placing this ID in the `ID` in the matching field, change `mode` to `load` instead of  `create`. The `region` field is used to determine the region of the generated guild when `mode` is equal to `create`

# Getting help
Use command `/help` to have more informations about commands.<br/>
The bot use the prefix : `/` to execute commands

# Commands list
## Utils commands
- `/debug <code>` **(Bot owner only)** : run python code
- `/invite` : Invite the bot to your guild
- `/shutdonw` **(Bot owner only)** : Shutdown the bot
- `/destroy` **(Bot owner only)** : Destroy definitively the self-managed guild. This cannot be undone.
- `/opendeal` : Get the invite to the financial district (self-managed guild)

## Economy commands (only in self managed guild)
- `/wallet` : Show your current wallet
- `/transfer <amount> <target>` : Transfer money from your wallet to the target's wallet
- `/economy` : Show current economy factor of the financial district guild
- `/rotarypress rotate <amount>` **(Darkness Member only)** : Rotate the rotary press, producing money, distributing the same amount on each account but decreasing money earned in games in the future for everyone.
- `/rotarypress reverse <amount>` **(Darkness Member only)** : Reverse the rotary press rotation, returning previously money produced by the rotary press and restoring economy factor (increasing back money earned in games).

## Games commands (only in self managed guild)
- `/roulette <bet> <area>` : Play roulette game, set up your bet and pray for the ball stops on your selected area. There are 18 areas (from 1 to 18) for each colors, and there are only two colors : R(ed) and B(lack)
- `/poker lobby create <name>` : Create a lobby for playing poker, other players can join it with the `poker lobby join` command (see below)
- `/poker lobby join <name>` : Join an existing poker lobby
- `/poker lobby leave` : Leave the current lobby where you are. Only works when executed in a poker lobby
- `/poker lobby disband` : Disband the current lobby where you are. Only works when executed in a poker lobby by the owner of the lobby
- `/poker start [kick_if_not_ready]` : Start a poker round in the current lobby where you are. Only works when executed by lobby owner.
- `/pennymachine <bet>` : Play to the pennymachine and pray for winning
