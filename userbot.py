import asyncio
import os

import aiohttp
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ========= الإعدادات (من Railway Variables) =========
SESSION_STRING = os.environ["1BJWap1wBu1QvCZhuuQM4mdJiNo_997oXe730X--D_4AnysPhUFHmZ3FSkAVzNpqsTpt7M6RwCiCkvuPELj9ENtAEoYLY-J5YpRmzvYqZLisU7Ah1VPijxwMmUHmn3lRA35NhLb6oo2yvhYvnqMToW0v-09heTIMpXIVs6hiKWWVIGzFZB3tzqDs_Gj-LlfYKumv3EIuFx3ud2p1XaUeDZsBoL2AwJl7Y2TZsS96Y5wbPSxk_vXalV4-J7_18uuWLa3AGdScmw-Cs3fY-AF6JgMTUkYnpp3wKh2yteWqrOoo1Yg1NAUeh2ph0pse-QV7ThPngtPy73tcn-j_oK5PpkB_ViDuQzeo="]
API_ID = 35666596                     # من https://my.telegram.org
API_HASH = "42ba74dc2df82894d76616994019d20f"  # من https://my.telegram.org
N8N_WEBHOOK = "https://n.couponscopy.com/webhook/recommendation"

CHANNELS = [
    "ForexNewspaper",
    "FXGoldVisionMarkets",
    "saffahelgold01",
]
# =====================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = event.message.message or ""
    if not text.strip():
        return

    chat = await event.get_chat()
    payload = {
        "text": text,
        "chat_id": str(event.chat_id),
        "chat_title": getattr(chat, "title", None) or getattr(chat, "username", "Unknown"),
    }

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(N8N_WEBHOOK, json=payload) as resp:
                print(f"[{payload['chat_title']}] -> n8n status {resp.status}")
    except Exception as e:
        print("Failed to send to n8n:", e)


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        raise SystemExit(
            "SESSION_STRING is invalid or expired. "
            "Generate a new one with StringSession.py and update Railway Variables."
        )
    print("Listening to:", ", ".join(CHANNELS))
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
