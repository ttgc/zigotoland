

class PennyMachineCog(commands.Cog, name='PennyMachines'):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger


    const cherries = client.emojis.find(emoji => emoji.name === "cherries");
    const banana = client.emojis.find(emoji => emoji.name === "banana");
    const kiwi = client.emojis.find(emoji => emoji.name === "kiwi");
    const watermelon = client.emojis.find(emoji => emoji.name === "watermelon");
    const moneybag = client.emojis.find(emoji => emoji.name === "moneybag");
    const poop = client.emojis.find(emoji => emoji.name === "poop");
    const monkey_face = client.emojis.find(emoji => emoji.name === "monkey_face");



    #@commands.check()
    async def pennyMachine():

        message.reply(`${poop}`)
