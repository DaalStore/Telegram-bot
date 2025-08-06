#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keyboard layouts for Daal Store Telegram Bot
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import COUNTRIES

def get_main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔐 VPN", callback_data="vpn")],
        [InlineKeyboardButton("🍎 Apple ID", callback_data="apple_id")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vpn_menu_keyboard():
    """VPN service selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔒 OpenVPN", callback_data="openvpn")],
        [InlineKeyboardButton("⚡ WireGuard", callback_data="wireguard")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_openvpn_keyboard():
    """OpenVPN options keyboard"""
    keyboard = [
        [InlineKeyboardButton("📦 یک ماهه ۵۰ گیگ - ۲۸۰ تومان", callback_data="openvpn_50gb")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_vpn")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_wireguard_keyboard():
    """WireGuard service type keyboard"""
    keyboard = [
        [InlineKeyboardButton("💰 اکونومی", callback_data="wireguard_economy")],
        [InlineKeyboardButton("⭐ پریمیوم", callback_data="wireguard_premium")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_vpn")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_wireguard_economy_keyboard():
    """WireGuard economy options keyboard"""
    keyboard = [
        [InlineKeyboardButton("📦 ۵۰ گیگ ماهانه - ۲۸۰ تومان", callback_data="wg_eco_50gb")],
        [InlineKeyboardButton("📦 ۱۰۰ گیگ ماهانه - ۵۰۰ تومان", callback_data="wg_eco_100gb")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_wireguard")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_wireguard_premium_keyboard():
    """WireGuard premium options keyboard"""
    keyboard = [
        [InlineKeyboardButton("📦 ۳۰ گیگ - ۲۸۰ تومان", callback_data="wg_pre_30gb")],
        [InlineKeyboardButton("📦 ۵۰ گیگ - ۴۰۰ تومان", callback_data="wg_pre_50gb")],
        [InlineKeyboardButton("📦 ۱۲۰ گیگ - ۷۰۰ تومان", callback_data="wg_pre_120gb")],
        [InlineKeyboardButton("🎮 ۳۰ گیگ (گیمینگ) - ۳۰۰ تومان", callback_data="wg_pre_30gb_gaming")],
        [InlineKeyboardButton("🎮 ۵۰ گیگ (گیمینگ) - ۴۳۵ تومان", callback_data="wg_pre_50gb_gaming")],
        [InlineKeyboardButton("🎮 ۱۲۰ گیگ (گیمینگ) - ۷۳۵ تومان", callback_data="wg_pre_120gb_gaming")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_wireguard")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_apple_id_keyboard():
    """Apple ID service options keyboard"""
    keyboard = [
        [InlineKeyboardButton("📧 ساخت با جیمیل شخصی - ۸۰۰ تومان", callback_data="apple_id_personal")],
        [InlineKeyboardButton("🆕 ساخت با جیمیل جدید - ۸۵۰ تومان", callback_data="apple_id_new")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_country_keyboard():
    """Country selection keyboard"""
    keyboard = []
    for i in range(0, len(COUNTRIES), 2):
        row = []
        row.append(InlineKeyboardButton(COUNTRIES[i], callback_data=f"country_{i}"))
        if i + 1 < len(COUNTRIES):
            row.append(InlineKeyboardButton(COUNTRIES[i + 1], callback_data=f"country_{i + 1}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_wireguard")])
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard():
    """Back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 بازگشت به منو اصلی", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_membership_check_keyboard():
    """Membership verification keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔍 بررسی عضویت", callback_data="check_membership")]
    ]
    return InlineKeyboardMarkup(keyboard)
