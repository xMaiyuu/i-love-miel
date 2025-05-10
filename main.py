import os
import discord
from discord.ext import commands
from keep_alive import keep_alive  # Comment this out if you're not using keep_alive

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

    @discord.ui.button(label="claim", style=discord.ButtonStyle.danger)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.user.roles, id=ALLOWED_ROLE_ID)
        if role is None:
            await interaction.response.send_message("You don't have permission to claim this request.", ephemeral=True)
            return

        if not self.claimed:
            self.claimed = True
            button.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(
                f"꒰˘ᵌ˘꒱♡  .  .  {interaction.user.mention} has claimed this request *!*",
                mention_author=False,
                reference=interaction.message
            )
        else:
            await interaction.response.send_message("This request has already been claimed.", ephemeral=True)

@bot.command()
async def req(ctx, *, request: str):
    message = f"_ _\n　　<@&{ALLOWED_ROLE_ID}>\n　୨୧　{ctx.author.mention} requested **{request}**\n-# _ _　　　upldrs, click button to claim　:z__natsugroove:\n_ _"
    view = ClaimButton(requester=ctx.author)
    await ctx.send(content=message, view=view)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="over requests ೀ")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f'Logged in as {bot.user.name}')

keep_alive()  # Comment this line out if you're not using Flask/Render keep_alive
bot.run(TOKEN)
