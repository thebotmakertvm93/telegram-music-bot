import os
from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, PORT

# Initialize Bot and Userbot
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("UserBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user)

# --- DUMMY WEB SERVER (For Render) ---
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
ydl_opts = {
    'format': 'bestaudio/best',
    'geo_bypass': True,
    'nocheckcertificate': True,
    'quiet': True,
    'no_warnings': True,
}

# 1. NEW: /start command so the bot replies in private messages
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply(
        "👋 Hello! I am alive and working.\n\n"
        "To use me, add me to a group, **make me an admin**, and type:\n"
        "`/play <youtube link>`"
    )

# 2. UPDATED: /play command (Only works in groups)
@bot.on_message(filters.command("play") & filters.group)
async def play_song(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a YouTube link. Example: `/play https://youtube.com/...`")
    
    url = message.command[1]
    chat_id = message.chat.id
    status_msg = await message.reply("⏳ Fetching audio stream...")

    try:
        # Extract audio URL directly
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title', 'Unknown Track')
        
        # Stream directly to the voice chat
        await call_py.play(
            chat_id,
            MediaStream(audio_url)
        )
        await status_msg.edit(f"🎵 **Now Playing:** {title}")
    except Exception as e:
        await status_msg.edit(f"❌ **Error:** `{str(e)}`\n\nMake sure the bot and the Userbot account are both in this group, and a Voice Chat is currently active.")

# --- STARTUP ---
async def main():
    await start_web_server()
    
    # Start the clients
    await bot.start()
    await user.start()
    await call_py.start()
    print("Bot and PyTgCalls successfully started! Waiting for messages...")
    
    # Pyrogram's official idle() keeps the bot listening for commands
    await idle()

if __name__ == "__main__":
    # We must use Pyrogram's run instead of pure asyncio to ensure proper teardown
    bot.run(main())
