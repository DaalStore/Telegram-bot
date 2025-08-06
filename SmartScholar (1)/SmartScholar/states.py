#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State management for Daal Store Telegram Bot
"""

from enum import Enum

class UserState(Enum):
    """User states for bot conversation flow"""
    MAIN_MENU = "main_menu"
    VPN_MENU = "vpn_menu"
    OPENVPN_MENU = "openvpn_menu"
    WIREGUARD_MENU = "wireguard_menu"
    WIREGUARD_ECONOMY = "wireguard_economy"
    WIREGUARD_PREMIUM = "wireguard_premium"
    APPLE_ID_MENU = "apple_id_menu"
    APPLE_ID_INFO = "apple_id_info"
    COUNTRY_SELECTION = "country_selection"
    WAITING_FOR_NAME = "waiting_for_name"
    WAITING_FOR_SURNAME = "waiting_for_surname"
    WAITING_FOR_BIRTHDATE = "waiting_for_birthdate"
    WAITING_FOR_EMAIL = "waiting_for_email"

# Global user states storage (in production, use Redis or database)
user_states = {}
user_data = {}

def get_user_state(user_id):
    """Get current user state"""
    return user_states.get(user_id, UserState.MAIN_MENU)

def set_user_state(user_id, state):
    """Set user state"""
    user_states[user_id] = state

def get_user_data(user_id):
    """Get user data"""
    return user_data.get(user_id, {})

def set_user_data(user_id, key, value):
    """Set user data"""
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value

def clear_user_data(user_id):
    """Clear user data"""
    if user_id in user_data:
        del user_data[user_id]
    if user_id in user_states:
        del user_states[user_id]
