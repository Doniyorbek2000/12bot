import asyncio
import logging
from aiogram import Bot
from app.config import settings
from app.loader import dp, bot, redis_client
from app.db.database import engine, Base, AsyncSessionLocal
from app.db.repositories.plan_repo import PlanRepository

# Import Middlewares
from app.bot.middlewares.auth import AuthMiddleware
from app.bot.middlewares.throttling import ThrottlingMiddleware

# Import Handlers
from app.bot.handlers import start, menu, legal_question, document_analysis, document_generation, voice, profile, tariffs, help, history
from app.bot.admin import admin_menu, dashboard, users, payments

logger = logging.getLogger("adolat_ai_bot.main")

async def on_startup(bot: Bot):
    """Bot ishga tushganda bajariladigan birinchi amallar"""
    logger.info("Bot ishga tushmoqda...")

    # 1. Baza jadvallarini avtomatik yaratish (Alembic sinxronligi uchun qulaylik)
    logger.info("Ma'lumotlar bazasi jadvallari tekshirilmoqda/yaratilmoqda...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Bazaviy jadvallar tayyor.")

    # 2. Standart tariflarni bazaga kiritish (Seed Plans)
    async with AsyncSessionLocal() as session:
        plan_repo = PlanRepository(session)
        await plan_repo.seed_plans()
    logger.info("Tariflar (Plans) bazada muvaffaqiyatli seed qilindi.")

    # 3. Webhook sozlamalari (agar faollashtirilgan bo'lsa)
    if settings.APP_ENV == "production" and settings.WEBHOOK_URL:
        logger.info(f"Webhook o'rnatilmoqda: {settings.WEBHOOK_URL}")
        await bot.set_webhook(
            url=settings.WEBHOOK_URL,
            drop_pending_updates=True
        )
    else:
        # Long polling ishlashi uchun webhookni tozalash
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook tozalandi. Long Polling rejimida davom etiladi.")

async def on_shutdown(bot: Bot):
    """Bot to'xtatilganda ulanishlarni yopish"""
    logger.info("Bot to'xtatilmoqda...")
    # Close Redis connection if active
    if redis_client:
        try:
            await redis_client.close()
        except Exception as redis_close_err:
            logger.warning(f"Redis ulanishini yopishda xatolik: {redis_close_err}")
    # Close DB Engine
    await engine.dispose()
    logger.info("Ulanishlar yopildi. Xayr!")

def register_middlewares():
    """Middlewares-larni ro'yxatdan o'tkazish"""
    # Rate Limiter (Anti-Spam)
    dp.message.outer_middleware(ThrottlingMiddleware(limit=0.8))
    
    # Auth & Database session dynamic injector (Outer middleware barcha handlerlardan oldin ishlaydi)
    dp.message.outer_middleware(AuthMiddleware())
    dp.callback_query.outer_middleware(AuthMiddleware())

def register_routers():
    """Barcha handler routerlarini ro'yxatdan o'tkazish"""
    # Foydalanuvchi routerlari
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(legal_question.router)
    dp.include_router(document_analysis.router)
    dp.include_router(document_generation.router)
    dp.include_router(voice.router)
    dp.include_router(profile.router)
    dp.include_router(tariffs.router)
    dp.include_router(history.router)
    dp.include_router(help.router)

    # Admin routerlari
    dp.include_router(admin_menu.router)
    dp.include_router(dashboard.router)
    dp.include_router(users.router)
    dp.include_router(payments.router)

async def main():
    # Setup all configurations
    register_middlewares()
    register_routers()

    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Bot ishga tushishida jiddiy xatolik yuz berdi: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Windows platformasida asinxron event loop xatoliklarining oldini olish uchun
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
