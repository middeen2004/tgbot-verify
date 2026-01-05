# SheerID Auto-Verification Bot - Deployment Guide

## Overview

This guide explains how to deploy the SheerID auto-verification Telegram bot using Docker or manual setup.

## Prerequisites

- Linux, macOS, or Windows with Python 3.11+
- MySQL 5.7+ (or compatible)
- At least 512MB RAM (1GB+ recommended)
- Reliable internet connection

## Quick Start with Docker Compose

1. Clone the repository.
2. Copy `env.example` to `.env` and fill in your values.
3. Run `docker compose up -d`.
4. View logs with `docker compose logs -f`.

## Manual Deployment

1. Install Python 3.11+ and MySQL.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`.
3. Configure environment variables in a `.env` file (see `env.example`).
4. Run the bot: `python bot.py`.

## Configuration Notes

- **Telegram**: `BOT_TOKEN`, `CHANNEL_USERNAME`, `CHANNEL_URL`, `ADMIN_USER_ID`
- **Database**: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- **Points**: Adjust `VERIFY_COST`, `CHECKIN_REWARD`, `INVITE_REWARD`, and `REGISTER_REWARD` in `config.py`.

## Troubleshooting

- Invalid bot token: verify `BOT_TOKEN` with @BotFather.
- Database connection errors: confirm MySQL is running and credentials are correct.
- Playwright issues: ensure `playwright install chromium` has been executed.

## Maintenance

- Rotate credentials regularly and back up the database.
- Monitor logs (`./logs` when using Docker).
- Update the codebase and rebuild Docker images as needed.

## Support

- Telegram channel: https://t.me/pk_oa
- Issues: https://github.com/PastKing/tgbot-verify/issues
