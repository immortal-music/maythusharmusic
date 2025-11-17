import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from maythusharmusic import LOGGER, app, userbot, YouTube
from maythusharmusic.core.call import Hotty
from maythusharmusic.misc import sudo
from maythusharmusic.plugins import ALL_MODULES
from maythusharmusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("maythusharmusic.plugins" + all_module)
    LOGGER("maythusharmusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Hotty.start()
    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("maythusharmusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Hotty.decorators()
    LOGGER("maythusharmusic").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ @sasukevipmusicbotsupport ᴊᴏɪɴ @sasukevipmusicbot , @sasukevipmusicbotsupport ꜰᴏʀ ᴀɴʏ ɪꜱꜱᴜᴇꜱ"
    )
    
    # --- (ပြင်ဆင်ချက် ၂ - Cache Pre-load လုပ်ရန် ဒီမှာ ထည့်ပါ) ---
    LOGGER(__name__).info("ယာယီမှတ်ဉာဏ် (In-Memory Cache) ကို ကြိုတင်ဖြည့်နေပါသည်...")
    try:
        # youtube.py ထဲက load_cache() function ကို ခေါ်ပါ
        await YouTube.load_cache() 
    except Exception as e:
        LOGGER(__name__).error(f"YouTube Cache ကို ကြိုတင်ဖြည့်ရာတွင် မအောင်မြင်ပါ: {e}")
    # --- (ဒီအထိ) ---
    
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("maythusharmusic").info("Stopping Sasuke Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
