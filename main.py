
import discord
from discord.ext import commands
import asyncio
import datetime
from keep_alive import keep_alive

TOKEN = "MTM1NjMxNjQ1MDYxNjUwODY1Nw.GPr3a6.-k0VYT4v1qdPA-9KKosMW7-4DodzJQBPKl2Cxs"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_ID = 1395727825037688852
RECEIVER_ID = 1187761955184836615
OWNER_ID = 1187761955184836615
AUTHORIZED_USERS = [1187761955184836615, 1280518554193494119]  # Owner and authorized user

roles = [
    ("丂〢❲hσrízσn❳", 500000),
    ("V͇̿I͇̿P͇̿・⁂ᴬᴹᴼ⁂", 20000000),
    ("丂〢❲ᘜ𝙾𝙻𝙳𝙴𝙽ᘜ𝙻𝙾𝚁𝚈❳", 15000000),
    ("丂〢❲𝐊𝐈𝐍𝐆❳", 15000000),
    ("丂〢❲ᘜ 𝙙𝙧𝙖𝙜𝙤𝙣 ᘜ❳", 25000000),
    ("丂〢❲✵𝑳𝒐𝒓𝒅✵❳", 30000000),
    ("丂〢❲♛𝐆𝐄𝐍𝐄𝐑𝐀𝐋♛❳", 50000000),
    ("❲❄𝑹𝑨𝑮𝑵𝑨𝑹𝑶𝑲❄❳", 70000000),
    ("★彡𝑹𝑶𝒀𝑨𝑳👑 彡★", 100000000)
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"🔥 Bot is on fire! Owner: <@{OWNER_ID}>")
    bot.add_view(Buttons())

@bot.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel) and channel.category_id == CATEGORY_ID:
        await asyncio.sleep(1)
        await send_purchase_message(channel)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Ignore command not found errors silently
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ معلومات ناقصة في الأمر")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ خطأ في معلومات الأمر")
    else:
        print(f"Error: {error}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check for @everyone mention
    if "@everyone" in message.content or "@here" in message.content:
        try:
            owner = bot.get_user(OWNER_ID)
            if owner:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dm_message = f"🚨 **تنبيه منشن @everyone**\n"
                dm_message += f"👤 **المستخدم:** {message.author.mention} ({message.author.name})\n"
                dm_message += f"📍 **السيرفر:** {message.guild.name}\n"
                dm_message += f"💬 **القناة:** {message.channel.mention}\n"
                dm_message += f"⏰ **الوقت:** {current_time}\n"
                dm_message += f"📝 **الرسالة:** {message.content}"
                
                await owner.send(dm_message)
        except Exception as e:
            print(f"Error sending DM: {e}")
    
    await bot.process_commands(message)

# بنت command - gives role to user
@bot.command(name="بنت")
async def bint_command(ctx, member: discord.Member = None):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.send("❌ هذا الأمر متاح للمالك والمخولين فقط")
        return
    
    if member is None:
        await ctx.send("❌ يرجى منشن المستخدم المطلوب\nمثال: `!بنت @المستخدم`")
        return
    
    try:
        # Get the role by ID
        role = ctx.guild.get_role(1355196241792729138)
        
        if role is None:
            await ctx.send("❌ لم يتم العثور على الرتبة")
            return
        
        # Check if user already has the role
        if role in member.roles:
            await ctx.send(f"❌ {member.mention} لديه الرتبة بالفعل")
            return
        
        # Add the role to the user
        await member.add_roles(role)
        await ctx.send(f"✅ تم إعطاء رتبة {role.mention} إلى {member.mention}")
        
    except discord.Forbidden:
        await ctx.send("❌ ليس لدي صلاحية لإعطاء هذه الرتبة")
    except Exception as e:
        await ctx.send(f"❌ حدث خطأ: {e}")

# ترار command - repeat message
@bot.command(name="ترار", aliases=["تكرار"])
async def repeat_message(ctx, count: int = None, *, message = None):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ هذا الأمر متاح للمالك فقط")
        return
    
    if count is None or message is None:
        await ctx.send("❌ يرجى كتابة الأمر بالشكل الصحيح\nمثال: `!ترار 5 مرحبا بكم`")
        return
    
    if count > 20:
        await ctx.send("❌ لا يمكن تكرار الرسالة أكثر من 20 مرة")
        return
    
    if count < 1:
        await ctx.send("❌ يجب أن يكون العدد أكبر من 0")
        return
    
    try:
        await ctx.message.delete()
    except:
        pass
    
    for i in range(count):
        await ctx.send(message)
        await asyncio.sleep(0.5)  # Small delay to avoid rate limiting

# Voice channel join command
@bot.command(name="د")
async def join_voice(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ هذا الأمر متاح للمالك فقط")
        return
    
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
            await ctx.send(f"🎵 تم الدخول إلى {channel.name}")
        except Exception as e:
            if "PyNaCl" in str(e):
                await ctx.send("❌ مكتبة الصوت غير مثبتة. يتم تثبيتها الآن...")
            else:
                await ctx.send(f"❌ خطأ في الدخول للمكالمة: {e}")
    else:
        # Join any available voice channel in the guild
        voice_channels = [channel for channel in ctx.guild.voice_channels]
        if voice_channels:
            try:
                voice_client = await voice_channels[0].connect()
                await ctx.send(f"🎵 تم الدخول إلى {voice_channels[0].name}")
            except Exception as e:
                if "PyNaCl" in str(e):
                    await ctx.send("❌ مكتبة الصوت غير مثبتة. يتم تثبيتها الآن...")
                else:
                    await ctx.send(f"❌ خطأ في الدخول للمكالمة: {e}")
        else:
            await ctx.send("❌ لا توجد قنوات صوتية متاحة")

# Leave voice command
@bot.command(name="اخرج")
async def leave_voice(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ هذا الأمر متاح للمالك فقط")
        return
    
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔇 تم الخروج من المكالمة")
    else:
        await ctx.send("❌ البوت ليس في مكالمة")

async def send_purchase_message(channel):
    await channel.send("🎯 **اختر ماذا تريد:**", view=Buttons())

class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛒 شراء رتبة", style=discord.ButtonStyle.green, custom_id="buy_button")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="🔽 الرجاء اختيار الرتبة من القائمة:",
            view=RoleSelect(),
            ephemeral=True
        )

    @discord.ui.button(label="❌ إلغاء", style=discord.ButtonStyle.red, custom_id="cancel_button")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.delete()
        except:
            pass
        await interaction.channel.send("❌ تم إلغاء عملية الشراء. للاستفسار الرجاء التكلم مع أحد الإدمنية.")

class RoleSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

        options = [
            discord.SelectOption(
                label=name,
                description=f"سعرها: {price:,}",
                value=f"{name}|{price}"
            )
            for name, price in roles
        ]

        self.add_item(RoleDropdown(options))

class RoleDropdown(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="🪙 اختر الرتبة التي تريد شراءها", options=options)

    async def callback(self, interaction: discord.Interaction):
        role_name, price = self.values[0].split("|")

        await interaction.response.send_message(
            content="📢 **الرجاء نسخ الكود وتحويله ثم منشن @بنقل أو أحد المشرفين بعد الدفع**",
            ephemeral=False
        )

        await interaction.channel.send(
            f" \nC {RECEIVER_ID} {price}"
        )

keep_alive()
bot.run(TOKEN)
