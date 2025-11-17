# youtubedatabase.py (ပြင်ဆင်ပြီး)

import logging
from typing import Union, Dict, Any

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError:
    raise ImportError(
        "motor package ကို ရှာမတွေ့ပါ (pip install motor)"
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URL = "mongodb+srv://wanglinmongodb:wanglin@cluster0.tny5vhz.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "youtubedb" 

try:
    _mongo_client = AsyncIOMotorClient(MONGO_URL)
    mongodb = _mongo_client[DATABASE_NAME]
    
    logger.info(f"Connecting to new MongoDB for YouTube Cache: {DATABASE_NAME}")

    onoffdb = mongodb.onoffper
    ytcache_db = mongodb.ytcache
    songfiles_db = mongodb.songfiles
    
    logger.info("New YouTube Database collections initialized successfully.")

except Exception as e:
    logger.critical(f"MongoDB connection အသစ် ({MONGO_URL}) ကို ချိတ်ဆက်ရာတွင် အမှားဖြစ်ပွားပါသည်: {e}")
    raise ConnectionError(f"YouTube Database connection failed: {e}") from e

# --- (Function (၁) - is_on_off) ---
async def is_on_off(on_off: int) -> bool:
    try:
        setting = await onoffdb.find_one({"on_off": on_off})
        return bool(setting)
    except Exception as e:
        logger.error(f"is_on_off check error for '{on_off}': {e}")
        return False

# --- (Function (၂) - get_yt_cache) ---
async def get_yt_cache(key: str) -> Union[dict, None]:
    try:
        cached_result = await ytcache_db.find_one({"key": key})
        if cached_result:
            return cached_result.get("details")
    except Exception as e:
        logger.error(f"Error getting YT cache for key '{key}': {e}")
    return None

# --- (Function (၃) - save_yt_cache) ---
async def save_yt_cache(key: str, details: dict):
    try:
        await ytcache_db.update_one(
            {"key": key},
            {"$set": {"details": details}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error saving YT cache for key '{key}': {e}")

# --- (Function (၄) - get_cached_song_path) ---
async def get_cached_song_path(video_id: str) -> Union[str, None]:
    try:
        cached_song = await songfiles_db.find_one({"video_id": video_id})
        if cached_song:
            return cached_song.get("file_path")
    except Exception as e:
        logger.error(f"Error getting song path cache for vid '{video_id}': {e}")
    return None

# --- (Function (၅) - save_cached_song_path) ---
async def save_cached_song_path(video_id: str, file_path: str):
    try:
        await songfiles_db.update_one(
            {"video_id": video_id},
            {"$set": {"file_path": file_path}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error saving song path cache for vid '{video_id}': {e}")

# --- (Function (၆) - remove_cached_song_path) ---
async def remove_cached_song_path(video_id: str):
    try:
        await songfiles_db.delete_one({"video_id": video_id})
    except Exception as e:
        logger.error(f"Error removing song path cache for vid '{video_id}': {e}")

# --- (Function (၇) (အသစ်) - Get ALL Cache for Pre-loading) ---
async def get_all_yt_cache() -> Dict[str, Any]:
    """MongoDB မှ cache လုပ်ထားသော YouTube search results အားလုံးကို ယူသည်"""
    all_cache: Dict[str, Any] = {}
    try:
        # filter မထည့်ဘဲ find() လုပ်ခြင်းဖြင့် document အားလုံးကို ယူပါ
        async for document in ytcache_db.find({}):
            key = document.get("key")
            details = document.get("details")
            if key and details:
                all_cache[key] = details
        
        count = len(all_cache)
        if count > 0:
            logger.info(f"MongoDB မှ cache {count} ခုကို အောင်မြင်စွာ Pre-load လုပ်ပြီး။")
        return all_cache
    except Exception as e:
        logger.error(f"Cache အားလုံးကို DB မှ ဆွဲထုတ်ရာတွင် အမှားဖြစ်ပွား: {e}")
        return {} # Error ဖြစ်လျှင် အလွတ် dictionary ပြန်ပေး
