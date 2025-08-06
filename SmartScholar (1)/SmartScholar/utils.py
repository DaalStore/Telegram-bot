#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for Daal Store Telegram Bot
"""

import logging
from telegram import Bot
from config import CHANNEL_ID, ORDER_LOG_CHANNEL

logger = logging.getLogger(__name__)

async def check_channel_membership(bot: Bot, user_id: int) -> bool:
    """
    Check if user is a member of the required channel
    
    Args:
        bot: Telegram Bot instance
        user_id: User ID to check
        
    Returns:
        bool: True if user is member, False otherwise
    """
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking membership for user {user_id}: {e}")
        return False

def validate_name(name: str) -> bool:
    """
    Validate user name input
    
    Args:
        name: Name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return len(name.strip()) >= 2 and name.strip().replace(' ', '').isalpha()

def validate_birthdate(birthdate: str) -> bool:
    """
    Validate birthdate format (YYYY/MM/DD or YYYY-MM-DD)
    
    Args:
        birthdate: Birthdate string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    import re
    pattern = r'^(19|20)\d{2}[/-](0[1-9]|1[0-2])[/-](0[1-9]|[12]\d|3[01])$'
    return bool(re.match(pattern, birthdate))

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_user_info(user_data: dict) -> str:
    """
    Format user information for Apple ID creation
    
    Args:
        user_data: Dictionary containing user information
        
    Returns:
        str: Formatted user information
    """
    info = f"""📋 اطلاعات شما:
👤 نام: {user_data.get('name', 'نامشخص')}
👤 نام خانوادگی: {user_data.get('surname', 'نامشخص')}
📅 تاریخ تولد: {user_data.get('birthdate', 'نامشخص')}
💰 نوع سرویس: {user_data.get('service_type', 'نامشخص')}"""
    
    # Add email if it's for personal Gmail service
    if user_data.get('email'):
        info += f"\n📧 ایمیل: {user_data.get('email')}"
    
    return info

async def log_order_to_channel(bot: Bot, user_info: dict, order_details: str):
    """
    Log order details to the specified Telegram channel
    
    Args:
        bot: Telegram Bot instance
        user_info: Dictionary containing user information
        order_details: String containing order details
    """
    try:
        # Format order message
        user_id = user_info.get('user_id', 'Unknown')
        username = user_info.get('username', 'No username')
        first_name = user_info.get('first_name', 'Unknown')
        last_name = user_info.get('last_name', '')
        
        order_message = f"""🛒 سفارش جدید
        
👤 کاربر: {first_name} {last_name}
🆔 شناسه کاربر: {user_id}
📱 نام کاربری: @{username}

{order_details}

⏰ زمان سفارش: {import_datetime().now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        # Send message to order log channel
        await bot.send_message(
            chat_id=ORDER_LOG_CHANNEL,
            text=order_message,
            parse_mode='HTML'
        )
        logger.info(f"Order logged for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error logging order to channel: {e}")

def import_datetime():
    """Import datetime module"""
    import datetime
    return datetime.datetime
