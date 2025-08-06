# Daal Store Telegram Bot

## Overview

This is a Persian Telegram bot for Daal Store that provides VPN and Apple ID services. The bot implements a menu-driven interface with channel membership verification and structured navigation for different service offerings.

**Current Status**: Bot is fully operational and running successfully with all requested features implemented.

**Recent Changes (July 14, 2025)**:
- Added membership verification button to non-member error messages
- Users can now click "بررسی عضویت" to check membership status and automatically start the bot if they're members
- Moved country selection from OpenVPN to WireGuard service
- OpenVPN now directly shows plan options without country selection
- WireGuard requires country selection before showing economy/premium options
- Added email collection for "Apple ID with personal Gmail" service
- Personal Gmail service now collects: name, surname, birthdate, and email address
- Implemented automatic order logging to Telegram channel for all services
- All completed purchases are now automatically logged to https://t.me/daalstoreorderlog with full order details
- Fixed order logging channel configuration and verified bot connection

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Architecture
- **Language**: Python 3
- **Framework**: python-telegram-bot library
- **Pattern**: Handler-based event-driven architecture
- **State Management**: In-memory storage with enum-based state tracking
- **Deployment**: Single-file application with modular component structure

### Key Design Decisions
- **Modular Structure**: Separated concerns into distinct modules (handlers, keyboards, config, states, utils)
- **State Management**: Implemented custom state tracking for conversation flow management
- **Channel Verification**: Mandatory channel membership check before bot access
- **Persian Language**: Full Persian language support for Iranian users

## Key Components

### 1. Main Application (`main.py`)
- **Purpose**: Entry point and bot initialization
- **Components**: Handler registration, logging setup, polling management
- **Pattern**: Single responsibility with clean handler delegation

### 2. Bot Handlers (`bot_handlers.py`)
- **Purpose**: Core business logic and user interaction handling
- **Responsibilities**: Command processing, callback handling, message processing
- **Pattern**: Handler pattern with state-based routing

### 3. Keyboard Layouts (`keyboards.py`)
- **Purpose**: UI component generation for Telegram inline keyboards
- **Components**: Menu keyboards for VPN services, Apple ID options, and navigation
- **Pattern**: Factory pattern for keyboard generation

### 4. Configuration (`config.py`)
- **Purpose**: Centralized configuration management
- **Components**: Bot token, channel info, payment details, country lists
- **Pattern**: Environment variable integration with fallback values

### 5. State Management (`states.py`)
- **Purpose**: User session and conversation state tracking
- **Components**: State enum definitions, user data storage, state utilities
- **Pattern**: Finite state machine with in-memory storage

### 6. Utilities (`utils.py`)
- **Purpose**: Common helper functions and validation
- **Components**: Channel membership verification, input validation
- **Pattern**: Pure functions with error handling

## Data Flow

### User Interaction Flow
1. **Start Command**: User sends `/start` → Channel membership check → Main menu display
2. **Service Selection**: User selects VPN or Apple ID → Service-specific menu
3. **Option Selection**: User chooses specific service → Payment information display
4. **Payment Process**: User receives payment details → Manual payment verification

### State Transitions
- **Main Menu** → VPN Menu → Service Type → Payment
- **Main Menu** → Apple ID Menu → Service Type → User Info Collection → Payment
- **Navigation**: Back buttons for menu traversal

## External Dependencies

### Telegram Bot API
- **Purpose**: Core bot functionality and user interaction
- **Integration**: python-telegram-bot library
- **Features**: Inline keyboards, callback queries, message handling

### Channel Integration
- **Purpose**: Membership verification and user engagement
- **Channel**: @daalstore (https://t.me/daalstore)
- **Verification**: Real-time membership status checking

### Payment System
- **Method**: Manual bank transfer verification
- **Bank**: Mellat Bank (Iran)
- **Process**: User sends payment receipt to channel direct messages

## Deployment Strategy

### Current Setup
- **Environment**: Single Python application
- **Dependencies**: python-telegram-bot library
- **Configuration**: Environment variables for sensitive data
- **State Storage**: In-memory (volatile)

### Production Considerations
- **State Persistence**: Recommend Redis or database for user states
- **Scaling**: Currently single-instance, would need session management for scaling
- **Monitoring**: Basic logging implemented, could be enhanced
- **Security**: Environment variables for sensitive configuration

### Service Architecture
- **VPN Services**: OpenVPN and WireGuard with multiple pricing tiers
- **Apple ID Services**: Two service types with user information collection
- **Payment Integration**: Manual verification through channel communication
- **User Experience**: Persian language with emoji-rich interface

The bot follows a straightforward request-response pattern with state management for complex user flows, making it suitable for the target Persian-speaking audience with clear navigation and payment processes.