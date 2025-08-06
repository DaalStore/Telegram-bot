#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daal Store Telegram Bot
Main entry point for the Persian Telegram bot that handles VPN and Apple ID services
"""
from keep_alive import keep_alive
keep_alive()
import logging
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN, CHANNEL_ID
from bot_handlers import (
    start_handler,
    button_handler,
    message_handler,
    error_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot with improved error handling
    logger.info("Starting Daal Store Telegram Bot...")
    try:
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,  # Clear any pending updates
            close_loop=False
        )
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == '__main__':
    main()
