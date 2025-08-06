#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handler functions for Daal Store Telegram Bot
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from config import (
    WELCOME_MESSAGE, PAYMENT_INFO, APPLE_ID_PAYMENT_INFO,
    ERROR_NOT_MEMBER, ERROR_GENERAL, ERROR_INVALID_INPUT, COUNTRIES
)
from keyboards import (
    get_main_menu_keyboard, get_vpn_menu_keyboard, get_openvpn_keyboard,
    get_wireguard_keyboard, get_wireguard_economy_keyboard,
    get_wireguard_premium_keyboard, get_apple_id_keyboard,
    get_country_keyboard, get_back_to_main_keyboard, get_membership_check_keyboard
)
from states import (
    UserState, get_user_state, set_user_state, get_user_data,
    set_user_data, clear_user_data
)
from utils import check_channel_membership, validate_name, validate_birthdate, validate_email, format_user_info, log_order_to_channel

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    
    try:
        # Check channel membership
        if not await check_channel_membership(context.bot, user_id):
            await update.message.reply_text(
                ERROR_NOT_MEMBER,
                reply_markup=get_membership_check_keyboard()
            )
            return
        
        # Send welcome message with main menu
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=get_main_menu_keyboard()
        )
        
        # Set user state to main menu
        set_user_state(user_id, UserState.MAIN_MENU)
        
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await update.message.reply_text(ERROR_GENERAL)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    try:
        # Handle membership check button
        if data == "check_membership":
            if await check_channel_membership(context.bot, user_id):
                # User is now a member, show welcome message
                await query.edit_message_text(
                    WELCOME_MESSAGE,
                    reply_markup=get_main_menu_keyboard()
                )
                set_user_state(user_id, UserState.MAIN_MENU)
            else:
                # Still not a member
                await query.edit_message_text(
                    ERROR_NOT_MEMBER,
                    reply_markup=get_membership_check_keyboard()
                )
            return
        
        # Check channel membership for all other interactions
        if not await check_channel_membership(context.bot, user_id):
            await query.edit_message_text(
                ERROR_NOT_MEMBER,
                reply_markup=get_membership_check_keyboard()
            )
            return
        
        # Handle main menu buttons
        if data == "vpn":
            await query.edit_message_text(
                "🔐 لطفا نوع VPN مورد نظر خود را انتخاب کنید:",
                reply_markup=get_vpn_menu_keyboard()
            )
            set_user_state(user_id, UserState.VPN_MENU)
            
        elif data == "apple_id":
            await query.edit_message_text(
                "🍎 لطفا نوع سرویس Apple ID مورد نظر خود را انتخاب کنید:",
                reply_markup=get_apple_id_keyboard()
            )
            set_user_state(user_id, UserState.APPLE_ID_MENU)
            
        # Handle VPN menu buttons
        elif data == "openvpn":
            await query.edit_message_text(
                "🔒 OpenVPN - لطفا پلن مورد نظر خود را انتخاب کنید:",
                reply_markup=get_openvpn_keyboard()
            )
            set_user_state(user_id, UserState.OPENVPN_MENU)
            
        elif data == "wireguard":
            await query.edit_message_text(
                "⚡ WireGuard - لطفا کشور مورد نظر خود را انتخاب کنید:",
                reply_markup=get_country_keyboard()
            )
            set_user_state(user_id, UserState.COUNTRY_SELECTION)
            set_user_data(user_id, "vpn_type", "wireguard")
            
        # Handle WireGuard menu buttons
        elif data == "wireguard_economy":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            await query.edit_message_text(
                f"💰 WireGuard اکونومی - {country}\n\n"
                "لطفا پلن مورد نظر خود را انتخاب کنید:",
                reply_markup=get_wireguard_economy_keyboard()
            )
            set_user_state(user_id, UserState.WIREGUARD_ECONOMY)
            
        elif data == "wireguard_premium":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n\n"
                "لطفا پلن مورد نظر خود را انتخاب کنید:",
                reply_markup=get_wireguard_premium_keyboard()
            )
            set_user_state(user_id, UserState.WIREGUARD_PREMIUM)
            
        # Handle country selection
        elif data.startswith("country_"):
            country_index = int(data.split("_")[1])
            selected_country = COUNTRIES[country_index]
            vpn_type = get_user_data(user_id).get("vpn_type", "")
            
            if vpn_type == "wireguard":
                await query.edit_message_text(
                    f"⚡ WireGuard - {selected_country}\n\n"
                    "لطفا نوع سرویس مورد نظر خود را انتخاب کنید:",
                    reply_markup=get_wireguard_keyboard()
                )
                set_user_state(user_id, UserState.WIREGUARD_MENU)
                set_user_data(user_id, "country", selected_country)
            
        # Handle OpenVPN purchase
        elif data == "openvpn_50gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "نامشخص")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"🔒 OpenVPN\n📦 پلن: یک ماهه ۵۰ گیگ\n💰 قیمت: ۲۸۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"🔒 OpenVPN\n"
                f"📦 پلن: یک ماهه ۵۰ گیگ\n"
                f"💰 قیمت: ۲۸۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        # Handle WireGuard Economy purchases
        elif data == "wg_eco_50gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⚡ WireGuard اکونومی - {country}\n📦 پلن: ۵۰ گیگ ماهانه\n💰 قیمت: ۲۸۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⚡ WireGuard اکونومی - {country}\n"
                f"📦 پلن: ۵۰ گیگ ماهانه\n"
                f"💰 قیمت: ۲۸۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_eco_100gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⚡ WireGuard اکونومی - {country}\n📦 پلن: ۱۰۰ گیگ ماهانه\n💰 قیمت: ۵۰۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⚡ WireGuard اکونومی - {country}\n"
                f"📦 پلن: ۱۰۰ گیگ ماهانه\n"
                f"💰 قیمت: ۵۰۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        # Handle WireGuard Premium purchases
        elif data == "wg_pre_30gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۳۰ گیگ\n💰 قیمت: ۲۸۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۳۰ گیگ\n"
                f"💰 قیمت: ۲۸۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_pre_50gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۵۰ گیگ\n💰 قیمت: ۴۰۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۵۰ گیگ\n"
                f"💰 قیمت: ۴۰۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_pre_120gb":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۱۲۰ گیگ\n💰 قیمت: ۷۰۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۱۲۰ گیگ\n"
                f"💰 قیمت: ۷۰۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_pre_30gb_gaming":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۳۰ گیگ (مخصوص گیمینگ)\n💰 قیمت: ۳۰۰ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۳۰ گیگ (مخصوص گیمینگ)\n"
                f"💰 قیمت: ۳۰۰ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_pre_50gb_gaming":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۵۰ گیگ (مخصوص گیمینگ)\n💰 قیمت: ۴۳۵ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۵۰ گیگ (مخصوص گیمینگ)\n"
                f"💰 قیمت: ۴۳۵ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        elif data == "wg_pre_120gb_gaming":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            
            # Log order to channel
            user_info = {
                'user_id': user_id,
                'username': query.from_user.username or 'No username',
                'first_name': query.from_user.first_name or 'Unknown',
                'last_name': query.from_user.last_name or ''
            }
            order_details = f"⭐ WireGuard پریمیوم - {country}\n📦 پلن: ۱۲۰ گیگ (مخصوص گیمینگ)\n💰 قیمت: ۷۳۵ تومان"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            await query.edit_message_text(
                f"⭐ WireGuard پریمیوم - {country}\n"
                f"📦 پلن: ۱۲۰ گیگ (مخصوص گیمینگ)\n"
                f"💰 قیمت: ۷۳۵ تومان\n\n"
                f"{PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
        # Handle Apple ID menu
        elif data == "apple_id_personal":
            await query.edit_message_text(
                "🍎 ساخت Apple ID با جیمیل شخصی\n"
                "💰 قیمت: ۸۰۰ تومان\n\n"
                "لطفا نام خود را وارد کنید:"
            )
            set_user_state(user_id, UserState.WAITING_FOR_NAME)
            set_user_data(user_id, "service_type", "Apple ID با جیمیل شخصی (۸۰۰ تومان)")
            set_user_data(user_id, "needs_email", True)
            
        elif data == "apple_id_new":
            await query.edit_message_text(
                "🍎 ساخت Apple ID با جیمیل جدید\n"
                "💰 قیمت: ۸۵۰ تومان\n\n"
                "لطفا نام خود را وارد کنید:"
            )
            set_user_state(user_id, UserState.WAITING_FOR_NAME)
            set_user_data(user_id, "service_type", "Apple ID با جیمیل جدید (۸۵۰ تومان)")
            set_user_data(user_id, "needs_email", False)
            
        # Handle back buttons
        elif data == "back_to_main":
            await query.edit_message_text(
                WELCOME_MESSAGE,
                reply_markup=get_main_menu_keyboard()
            )
            set_user_state(user_id, UserState.MAIN_MENU)
            clear_user_data(user_id)
            
        elif data == "back_to_vpn":
            await query.edit_message_text(
                "🔐 لطفا نوع VPN مورد نظر خود را انتخاب کنید:",
                reply_markup=get_vpn_menu_keyboard()
            )
            set_user_state(user_id, UserState.VPN_MENU)
            
        elif data == "back_to_wireguard":
            user_data = get_user_data(user_id)
            country = user_data.get("country", "")
            if country:
                await query.edit_message_text(
                    f"⚡ WireGuard - {country}\n\n"
                    "لطفا نوع سرویس مورد نظر خود را انتخاب کنید:",
                    reply_markup=get_wireguard_keyboard()
                )
            else:
                await query.edit_message_text(
                    "⚡ WireGuard - لطفا کشور مورد نظر خود را انتخاب کنید:",
                    reply_markup=get_country_keyboard()
                )
                set_user_state(user_id, UserState.COUNTRY_SELECTION)
                set_user_data(user_id, "vpn_type", "wireguard")
                return
            set_user_state(user_id, UserState.WIREGUARD_MENU)
            
    except Exception as e:
        logger.error(f"Error in button handler: {e}")
        await query.edit_message_text(ERROR_GENERAL)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    current_state = get_user_state(user_id)
    
    try:
        # Check channel membership
        if not await check_channel_membership(context.bot, user_id):
            await update.message.reply_text(
                ERROR_NOT_MEMBER,
                reply_markup=get_membership_check_keyboard()
            )
            return
        
        # Handle Apple ID information collection
        if current_state == UserState.WAITING_FOR_NAME:
            if not validate_name(text):
                await update.message.reply_text(
                    "❌ نام وارد شده نامعتبر است. لطفا نام خود را به درستی وارد کنید:"
                )
                return
                
            set_user_data(user_id, "name", text)
            set_user_state(user_id, UserState.WAITING_FOR_SURNAME)
            await update.message.reply_text("لطفا نام خانوادگی خود را وارد کنید:")
            
        elif current_state == UserState.WAITING_FOR_SURNAME:
            if not validate_name(text):
                await update.message.reply_text(
                    "❌ نام خانوادگی وارد شده نامعتبر است. لطفا نام خانوادگی خود را به درستی وارد کنید:"
                )
                return
                
            set_user_data(user_id, "surname", text)
            set_user_state(user_id, UserState.WAITING_FOR_BIRTHDATE)
            await update.message.reply_text(
                "لطفا تاریخ تولد خود را به فرمت YYYY/MM/DD وارد کنید:\n"
                "مثال: 1990/01/15"
            )
            
        elif current_state == UserState.WAITING_FOR_BIRTHDATE:
            if not validate_birthdate(text):
                await update.message.reply_text(
                    "❌ تاریخ تولد وارد شده نامعتبر است. لطفا تاریخ تولد خود را به فرمت YYYY/MM/DD وارد کنید:\n"
                    "مثال: 1990/01/15"
                )
                return
                
            set_user_data(user_id, "birthdate", text)
            user_data = get_user_data(user_id)
            
            # Check if email is needed (for personal Gmail service)
            if user_data.get("needs_email", False):
                set_user_state(user_id, UserState.WAITING_FOR_EMAIL)
                await update.message.reply_text(
                    "لطفا آدرس جیمیل خود را وارد کنید:\n"
                    "مثال: example@gmail.com"
                )
            else:
                # Log Apple ID order to channel (without email for new Gmail service)
                user_info = {
                    'user_id': user_id,
                    'username': update.effective_user.username or 'No username',
                    'first_name': update.effective_user.first_name or 'Unknown',
                    'last_name': update.effective_user.last_name or ''
                }
                order_details = f"🍎 {user_data.get('service_type', 'Apple ID')}\n👤 نام: {user_data.get('name', 'نامشخص')}\n👤 نام خانوادگی: {user_data.get('surname', 'نامشخص')}\n📅 تاریخ تولد: {user_data.get('birthdate', 'نامشخص')}"
                await log_order_to_channel(context.bot, user_info, order_details)
                
                # Show user information and payment details
                info_text = format_user_info(user_data)
                await update.message.reply_text(
                    f"{info_text}\n\n{APPLE_ID_PAYMENT_INFO}",
                    reply_markup=get_back_to_main_keyboard()
                )
                
                # Reset state
                set_user_state(user_id, UserState.MAIN_MENU)
                
        elif current_state == UserState.WAITING_FOR_EMAIL:
            if not validate_email(text):
                await update.message.reply_text(
                    "❌ آدرس ایمیل وارد شده نامعتبر است. لطفا آدرس جیمیل خود را به درستی وارد کنید:\n"
                    "مثال: example@gmail.com"
                )
                return
                
            set_user_data(user_id, "email", text)
            user_data = get_user_data(user_id)
            
            # Log Apple ID order to channel
            user_info = {
                'user_id': user_id,
                'username': update.effective_user.username or 'No username',
                'first_name': update.effective_user.first_name or 'Unknown',
                'last_name': update.effective_user.last_name or ''
            }
            order_details = f"🍎 {user_data.get('service_type', 'Apple ID')}\n👤 نام: {user_data.get('name', 'نامشخص')}\n👤 نام خانوادگی: {user_data.get('surname', 'نامشخص')}\n📅 تاریخ تولد: {user_data.get('birthdate', 'نامشخص')}\n📧 ایمیل: {user_data.get('email', 'نامشخص')}"
            await log_order_to_channel(context.bot, user_info, order_details)
            
            # Show user information and payment details
            info_text = format_user_info(user_data)
            await update.message.reply_text(
                f"{info_text}\n\n{APPLE_ID_PAYMENT_INFO}",
                reply_markup=get_back_to_main_keyboard()
            )
            
            # Reset state
            set_user_state(user_id, UserState.MAIN_MENU)
            
        else:
            # Unknown state or invalid input
            await update.message.reply_text(
                ERROR_INVALID_INPUT + "\n\n" + WELCOME_MESSAGE,
                reply_markup=get_main_menu_keyboard()
            )
            set_user_state(user_id, UserState.MAIN_MENU)
            
    except Exception as e:
        logger.error(f"Error in message handler: {e}")
        await update.message.reply_text(ERROR_GENERAL)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(ERROR_GENERAL)
        except TelegramError:
            logger.error("Failed to send error message to user")
