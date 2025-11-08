import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import aiohttp
from datetime import datetime
from typing import Optional

# Load configuration
def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Please copy config.example.json to config.json and fill in your details.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON.")
        exit(1)

config = load_config()

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True  # Required to manage roles
intents.dm_messages = True  # Required to receive DMs

class BocikBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',  # Fallback prefix, we'll use slash commands mainly
            intents=intents
        )
        self.dm_log_file = 'dm_logs.json'
        
    async def setup_hook(self):
        """This is called when the bot is starting up"""
        # Sync slash commands with Discord
        await self.tree.sync()
        print(f"Synced slash commands")

    async def on_ready(self):
        """Called when the bot is ready"""
        print(f'Bot zalogowany jako {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Handle DM messages
        if isinstance(message.channel, discord.DMChannel):
            await self.handle_dm(message)
            return

        # Check for response triggers in guild messages
        if message.guild:
            await self.check_response_triggers(message)

        # Process commands (for the command prefix)
        await self.process_commands(message)

    async def handle_dm(self, message):
        """Handle DM messages - log them and send via webhook"""
        # Log the DM
        dm_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'author': str(message.author),
            'author_id': message.author.id,
            'content': message.content,
            'attachments': [att.url for att in message.attachments]
        }
        
        # Save to file
        self.save_dm_log(dm_data)
        
        # Send via webhook
        await self.send_dm_webhook(message)
        
        # Confirm receipt to user
        await message.channel.send("✅ Twoja wiadomość została zapisana i przekazana!")

    def save_dm_log(self, dm_data):
        """Save DM to JSON file"""
        logs = []
        if os.path.exists(self.dm_log_file):
            try:
                with open(self.dm_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        
        logs.append(dm_data)
        
        with open(self.dm_log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    async def send_dm_webhook(self, message):
        """Send DM content via webhook"""
        webhook_url = config.get('webhook_url')
        if not webhook_url or webhook_url == "YOUR_WEBHOOK_URL_HERE":
            print("Warning: Webhook URL not configured, skipping webhook send")
            return

        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(webhook_url, session=session)
                
                embed = discord.Embed(
                    title="📨 Nowa wiadomość prywatna",
                    description=message.content,
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                embed.set_author(
                    name=str(message.author),
                    icon_url=message.author.display_avatar.url
                )
                embed.set_footer(text=f"ID: {message.author.id}")
                
                # Add attachments if any
                if message.attachments:
                    embed.add_field(
                        name="Załączniki",
                        value='\n'.join([att.url for att in message.attachments]),
                        inline=False
                    )
                
                await webhook.send(embed=embed, username="Bocik DM Logger")
                print(f"Sent DM webhook for message from {message.author}")
        except Exception as e:
            print(f"Error sending webhook: {e}")

    async def check_response_triggers(self, message):
        """Check if message contains any trigger words and respond"""
        response_triggers = config.get('response_triggers', {})
        content_lower = message.content.lower()
        
        for trigger, response in response_triggers.items():
            if trigger.lower() in content_lower:
                await message.channel.send(response)
                break  # Only respond once per message

# Create bot instance
bot = BocikBot()

@bot.tree.command(name="mute", description="Wycisz użytkownika nadając mu rolę Muted")
@app_commands.describe(
    user="Użytkownik do wyciszenia",
    reason="Powód wyciszenia (opcjonalny)"
)
@app_commands.checks.has_permissions(manage_roles=True)
async def mute(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: Optional[str] = "Nie podano powodu"
):
    """Mute a user by assigning them the Muted role"""
    # Check if the bot has permission to manage roles
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message(
            "❌ Nie mam uprawnień do zarządzania rolami!",
            ephemeral=True
        )
        return

    # Get or create the Muted role
    muted_role_name = config.get('muted_role_name', 'Muted')
    muted_role = discord.utils.get(interaction.guild.roles, name=muted_role_name)
    
    if not muted_role:
        # Create the Muted role if it doesn't exist
        try:
            muted_role = await interaction.guild.create_role(
                name=muted_role_name,
                reason="Utworzono automatycznie przez bota"
            )
            
            # Set permissions for the muted role in all channels
            for channel in interaction.guild.channels:
                try:
                    await channel.set_permissions(
                        muted_role,
                        send_messages=False,
                        speak=False,
                        add_reactions=False
                    )
                except discord.Forbidden:
                    print(f"Nie można ustawić uprawnień w kanale {channel.name}")
                    
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Nie mogę utworzyć roli Muted!",
                ephemeral=True
            )
            return

    # Check if user already has the role
    if muted_role in user.roles:
        await interaction.response.send_message(
            f"⚠️ {user.mention} już ma rolę {muted_role.name}!",
            ephemeral=True
        )
        return

    # Assign the role
    try:
        await user.add_roles(muted_role, reason=reason)
        
        # Send confirmation
        embed = discord.Embed(
            title="🔇 Użytkownik wyciszony",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Użytkownik", value=user.mention, inline=True)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Powód", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
        
        # Try to notify the user
        try:
            await user.send(
                f"Zostałeś wyciszony na serwerze **{interaction.guild.name}**\n"
                f"Powód: {reason}"
            )
        except discord.Forbidden:
            # User has DMs disabled
            pass
            
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Nie mam uprawnień do nadania tej roli!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Wystąpił błąd: {str(e)}",
            ephemeral=True
        )

@mute.error
async def mute_error(interaction: discord.Interaction, error):
    """Handle errors for the mute command"""
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❌ Nie masz uprawnień do używania tej komendy!",
            ephemeral=True
        )

# Run the bot
if __name__ == "__main__":
    token = config.get('token')
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("Error: Bot token not configured in config.json")
        exit(1)
    
    bot.run(token)
