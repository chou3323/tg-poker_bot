
# Telegram Poker Bot

This bot analyzes poker hands, calculates winning probabilities, and provides strategy advice based on the given input.

## Features
- Analyze poker hands using the `treys` library.
- Calculate winning probabilities, tie probabilities, and losing probabilities.
- Provide strategy recommendations based on probabilities.

## How to Use
1. Start the bot with `/start`.
2. Use `/calculate <hand> <board> <number_of_players>` to calculate probabilities.
   - Example: `/calculate Ah Kh Qh Jh Th 3`.

## Requirements
- Python 3.7+
- Libraries: `telegram`, `treys`

## Setup
1. Install dependencies:
   ```bash
   pip install python-telegram-bot treys
   ```
2. Replace `YOUR_TELEGRAM_BOT_TOKEN` in `telegram_poker_bot.py` with your bot token.
3. Run the bot:
   ```bash
   python telegram_poker_bot.py
   ```
