#!/usr/bin/env python3
"""
Telegram Bot Constructor — Main Entry Point
"""
import sys
import signal
import threading

from app.core.logger import logger
from app.core.database import init_db, get_db
from app.core.config import settings


def main():
    logger.info("=" * 60)
    logger.info("Starting Telegram Bot Constructor")
    logger.info(f"DB: {settings.DATABASE_URL[:40]}...")
    logger.info(f"Admin IDs: {settings.ADMIN_IDS}")
    logger.info("=" * 60)

    # 1. Init database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.critical(f"Database init failed: {e}")
        sys.exit(1)

    # 2. Seed templates
    try:
        from app.services.template_service import seed_templates
        with get_db() as db:
            seed_templates(db)
        logger.info("Templates seeded")
    except Exception as e:
        logger.error(f"Template seeding failed: {e}")

    # 3. Create constructor bot
    from app.bot.constructor_bot import create_constructor_bot
    import app.bot.constructor_bot as cbot_module
    bot = create_constructor_bot()
    cbot_module.constructor_bot = bot

    # 4. Setup scheduler
    from app.scheduler.tasks import setup_scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started")

    # 5. Restore previously running bots
    from app.runtime.bot_runtime_manager import runtime_manager
    restore_thread = threading.Thread(
        target=runtime_manager.restore_bots,
        name="bot_restore",
        daemon=True,
    )
    restore_thread.start()

    # 6. Graceful shutdown
    def shutdown(signum, frame):
        logger.info("Shutdown signal received...")
        scheduler.shutdown(wait=False)
        runtime_manager.stop_all()
        try:
            bot.stop_polling()
        except Exception:
            pass
        logger.info("Shutdown complete")
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # 7. Start polling
    logger.info("Bot started. Polling...")
    try:
        bot.infinity_polling(
            timeout=30,
            long_polling_timeout=20,
            logger_level=None,
            restart_on_change=False,
            skip_pending=True,
        )
    except Exception as e:
        logger.critical(f"Polling crashed: {e}")
        scheduler.shutdown(wait=False)
        runtime_manager.stop_all()
        sys.exit(1)


if __name__ == "__main__":
    main()
