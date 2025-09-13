import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from bot import handlers, lesson_handlers, payment_handlers

async def main():
    """Main bot function"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check bot token
    if not config.bot_token:
        logging.error("BOT_TOKEN not found in .env file!")
        return
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(handlers.router)
    dp.include_router(lesson_handlers.router) 
    dp.include_router(payment_handlers.router)
    
    # Start polling
    logging.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")