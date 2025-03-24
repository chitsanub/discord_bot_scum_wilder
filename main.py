import discord
import os
import requests
from discord.ext import commands

from myserver import server_on

# ตั้งค่า intents เพื่อให้ Bot สามารถเข้าถึงข้อความได้
intents = discord.Intents.default()
intents.message_content = True  # จำเป็นสำหรับการเข้าถึงเนื้อหาข้อความ

# สร้าง Bot โดยระบุ command prefix และ intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send('สวัสดีครับ!')

# ตัวอย่างการตอบสนองข้อความทั่วไป (Chat Response)

@bot.event
async def on_message(message):
    # ข้ามข้อความที่ Bot ส่งเอง
    if message.author == bot.user:
        return

    # ตัวอย่าง: ถ้าข้อความมีคำว่า "hi bot" จะตอบกลับ
    if 'รับ welcome pack' in message.content.lower():
        await message.channel.send(f"สวัสดีค่ะ {message.author.mention}! กรุณารอ Admin สักครู่นะคะ")

    if message.content.startswith('getbunkers'):
        url = 'https://api.whalleybot.com/bot/c1ba9fa8/GetBunkers'
        headers = {
            'accept': '*/*',
            'Authorization': 'WhalleyBotAPI_XBewKLRWae_mnw==',
            'Accept-Encoding': 'gzip'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # ตรวจสอบ HTTP error
            bunkers = response.json()  # ควรจะได้เป็น List

            if isinstance(bunkers, list):
                # สร้างข้อความสรุปสำหรับแต่ละ bunker
                lines = []
                for bunker in bunkers:
                    if bunker.get('status') == 'Active':
                        line = (f"Sector {bunker.get('sector')} : {bunker.get('status')}")
                        lines.append(line)
                output = "\n".join(lines)

                
                await message.channel.send(f"# รายการ Bunkers ค่ะ {message.author.mention} : \n```{output}```")
            else:
                await message.channel.send("ไม่พบข้อมูล bunkers ที่ถูกต้อง")
        except requests.exceptions.RequestException as e:
            await message.channel.send(f"เกิดข้อผิดพลาดในการเรียก API: {e}")

    # ให้ Bot ประมวลผลคำสั่งอื่นๆ ด้วย
    await bot.process_commands(message)

server_on()    
# รัน Bot ด้วย Token ของคุณ
bot.run(os.getenv('DISCORD_TOKEN'))
