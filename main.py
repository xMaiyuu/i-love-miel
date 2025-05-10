import os
import discord
from discord.ext import commands
from keep_alive import keep_alive  # Keeps the bot alive on Render

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=",", intents=intents)

ALLOWED_ROLE_ID = 1370091989714079845  # Role that can click the button

class ClaimButton(discord.ui.View):
    def __init__(self, requester: discord.Member):
        super().__init__(timeout=None)
        self.requester = requester
        self.claimed = False

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.danger)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.user.roles, id=ALLOWED_ROLE_ID)
    if role is None:
        await interaction.response.send_message("You don't have permission to claim this request.", ephemeral=True)
        return

    if not self.claimed:
        self.claimed = True
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.message.reply(
            f"꒰˘ᵌ˘꒱♡  .  .  {interaction.user.mention} has claimed this request *!*"
        )
        await interaction.response.defer()
    else:
        await interaction.response.send_message("This request has already been claimed.", ephemeral=True)

@bot.command()
async def req(ctx, *, request: str):
    message = f"_ _\n　　<@&1370091989714079845>\n　୨୧　{ctx.author.mention} requested **{request}**\n-# _ _　　　upldrs, click button to claim　<a:z__natsugroove:1353422820335554632>\n_ _"
    view = ClaimButton(requester=ctx.author)
    await ctx.send(content=message, view=view)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="over requests ೀ")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f'Logged in as {bot.user.name}')

keep_alive()  # Start web server to prevent Render from sleeping
bot.run(TOKEN)
