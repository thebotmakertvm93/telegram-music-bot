import asyncio
import os
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, PORT

# Initialize Bot and Userbot Clients
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("UserBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Initialize PyTgCalls using the updated 3.x GroupCallFactory structure
group_call_factory = GroupCallFactory(user)

# --- DUMMY WEB SERVER ---
# Render requires Web Services to bind to a port, otherwise the deploy fails.
async def handle_ping(request):
    return web.Response(text="Bot is awake and listening!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Web server started on port {PORT}")

# --- MUSIC LOGIC ---
@bot.on_message(filters.command("play") & filters.group)
async def play_song(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a YouTube link. Example: `/play https://youtube.com/...`")
    
    # FIX: Change from 'message.command' to 'message.command[1]' to get the string URL
    url = message.command[1] 
    chat_id = message.chat.id
    status_msg = await message.reply("⏳ Initializing audio stream wrapper...")

    try:
        group_call = group_call_factory.get_file_group_call()
        await group_call.join(chat_id)
        await group_call.start_audio_streaming(url, repeat=False)
        
        await status_msg.edit(f"🎵 **Now Playing:** `{url}`")
    except Exception as e:
        await status_msg.edit(f"❌ **Error:** `{str(e)}`\nMake sure the bot and assistant account are admins.")

# --- STARTUP ---
async def main():
    await start_web_server()
    await bot.start()
    await user.start()
    print("Bot clients and components successfully started!")
    
    # Keep the event loop running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
