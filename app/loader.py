import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from redis.asyncio import Redis
from app.config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("adolat_ai_bot")

# Initialize Redis connection with MemoryStorage fallback
try:
    from aiogram.fsm.storage.memory import MemoryStorage
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    storage = RedisStorage(redis=redis_client)
    logger.info("Redis FSM Storage muvaffaqiyatli ulandi.")
except Exception as e:
    from aiogram.fsm.storage.memory import MemoryStorage
    logger.warning(f"Redis-ga ulanib bo'lmadi ({e}). MemoryStorage (xotira FSM) faollashtirildi.")
    redis_client = None
    storage = MemoryStorage()

# Initialize Bot with default HTML parse mode for premium rendering
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Initialize Dispatcher
dp = Dispatcher(storage=storage)
