import discord
import asyncio
import requests
import os
from keep_alive import keep_alive  # dein Webserver-Modul

TOKEN = os.getenv("DISCORD_TOKEN")

# TikTok-Nutzername → Discord-Kanal-ID
USER_CONFIG = {
    "asoka97eq": 1389205668291936256,
    "eliyaa85": 1389205668291936256,
    "brobrooo79": 1389206368044585101,
    "rebzyy.eh": 1389206368044585101,
    "": 1390434940197277756,
    "eh_snipezyaa": 1390434940197277756,
    "makavei.eh": 1391191711275028511,
    "": ,
    "": ,
    "": ,
}

LAST_VIDEO_IDS = {}

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_all_users():
    global LAST_VIDEO_IDS
    while True:
        for username, channel_id in USER_CONFIG.items():
            try:
                url = f"https://www.tiktok.com/@{username}"
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                if response.ok:
                    video_ids = list(set([
                        x.split("video/")[1].split("?")[0]
                        for x in response.text.split('"') if "video/" in x
                    ]))

                    if video_ids:
                        latest_id = video_ids[0]
                        if LAST_VIDEO_IDS.get(username) != latest_id:
                            LAST_VIDEO_IDS[username] = latest_id
                            channel = client.get_channel(channel_id)
                            if channel:
                                await channel.send(
                                    f"@everyone 📢 Neues TikTok von @{username}: https://www.tiktok.com/@{username}/video/{latest_id}"
                                )
                            else:
                                print(f"⚠ Kanal mit ID {channel_id} nicht gefunden")
            except Exception as e:
                print(f"Fehler bei {username}:", e)

        await asyncio.sleep(300)  # Alle 5 Minuten prüfen

@client.event
async def on_ready():
    print(f"✅ Bot läuft als {client.user}")
    client.loop.create_task(check_all_users())

if _name_ == "_main_":
    keep_alive()  # Starte den kleinen Webserver (für UptimeRobot)
    client.run(TOKEN)