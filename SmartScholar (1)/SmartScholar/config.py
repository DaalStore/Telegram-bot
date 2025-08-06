#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for Daal Store Telegram Bot
"""

import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
CHANNEL_ID = "@daalstore"  # Channel username for membership verification
CHANNEL_URL = "https://t.me/daalstore"
ORDER_LOG_CHANNEL = "-1002692195953"  # Channel ID for order logging (@daalstoreorderlog)

# Welcome message
WELCOME_MESSAGE = "به ربات پشتیبانی فروشگاه دال استور خوش آمدید"

# Payment information
PAYMENT_INFO = """ملت:
🔺کارت:
🔺6104 3389 0854 5722
🔸حساب
🔸9516273837
🔹شبا
🔹IR87 0120 0000 0000 9516 2738 37
📍بنام: رضا خوشاب
📍لطفا پس از واریز عکس فیش را داخل دایرکت کانال ارسال بفرمایید🙏🏻"""

APPLE_ID_PAYMENT_INFO = """ملت:
🔺کارت:
🔺6104 3389 0854 5722
🔸حساب
🔸9516273837
🔹شبا
🔹IR87 0120 0000 0000 9516 2738 37
📍بنام: رضا خوشاب
📍لطفا پس از واریز عکس فیش را داخل دایرکت کانال ارسال بفرمایید🙏🏻

لطفا توجه بفرمایید که فرایند ساخت اپل آیدی کمی زمان بر بوده و بزودی براتون ارسال میشه"""

# Countries for VPN selection
COUNTRIES = [
    "🇺🇸 آمریکا", "🇬🇧 انگلیس", "🇩🇪 آلمان", "🇫🇷 فرانسه",
    "🇨🇦 کانادا", "🇯🇵 ژاپن", "🇰🇷 کره جنوبی", "🇸🇬 سنگاپور",
    "🇳🇱 هلند", "🇸🇪 سوئد", "🇨🇭 سوئیس", "🇦🇺 استرالیا"
]

# Error messages
ERROR_NOT_MEMBER = "❌ برای استفاده از ربات ابتدا باید عضو کانال باشید:\n" + CHANNEL_URL
ERROR_GENERAL = "❌ خطایی رخ داده است. لطفا دوباره تلاش کنید."
ERROR_INVALID_INPUT = "❌ ورودی نامعتبر است. لطفا دوباره تلاش کنید."
