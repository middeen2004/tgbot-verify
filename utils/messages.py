"""Message templates."""
from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Return the welcome message."""
    msg = (
        f"🎉 Welcome, {full_name}!\n"
        "You have successfully registered and received 1 point.\n"
    )
    if invited_by:
        msg += "Thanks for joining via an invite link—the inviter received 2 points.\n"

    msg += (
        "\nThis bot can automatically complete SheerID verification.\n"
        "Quick start:\n"
        "/about - Learn what the bot can do\n"
        "/balance - Check your balance\n"
        "/help - View all commands\n\n"
        "Earn more points:\n"
        "/qd - Daily check-in\n"
        "/invite - Invite friends\n"
        f"Join the channel: {CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """Return the about message."""
    return (
        "🤖 SheerID Auto-Verification Bot\n"
        "\n"
        "Features:\n"
        "- Automatically completes SheerID student/teacher verification\n"
        "- Supports Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher, Perplexity Pro Student\n"
        "- /service shows all services with quick buttons\n"
        "\n"
        "Points:\n"
        "- Registration bonus: 1 point\n"
        "- Daily check-in: +1 point\n"
        "- Invite friends: +2 points per person\n"
        "- Use card keys (per card rules)\n"
        f"- Join the channel: {CHANNEL_URL}\n"
        "\n"
        "How to use:\n"
        "1. Start verification on the web page and copy the full verification link\n"
        "2. Send /verify, /verify2, /verify3, /verify4, or /verify5 with that link\n"
        "3. Wait for processing and review the results\n"
        "4. Bolt.new verification automatically retrieves a code; use /getV4Code <verification_id> for manual lookup\n"
        "\n"
        "Send /help for more commands"
    )


def get_help_message(is_admin: bool = False) -> str:
    """Return the help message."""
    msg = (
        "📖 SheerID Auto-Verification Bot - Help\n"
        "\n"
        "User commands:\n"
        "/start - Begin (register)\n"
        "/about - Learn what the bot can do\n"
        "/balance - View your balance\n"
        "/service - List services with quick buttons\n"
        "/qd - Daily check-in (+1 point)\n"
        "/invite - Generate an invite link (+2 points per person)\n"
        "/use <code> - Redeem a card key for points\n"
        f"/verify <link> - Gemini One Pro verification (-{VERIFY_COST} points)\n"
        f"/verify2 <link> - ChatGPT Teacher K12 verification (-{VERIFY_COST} points)\n"
        f"/verify3 <link> - Spotify Student verification (-{VERIFY_COST} points)\n"
        f"/verify4 <link> - Bolt.new Teacher verification (-{VERIFY_COST} points)\n"
        f"/verify5 <link> - YouTube Student Premium verification (-{VERIFY_COST} points)\n"
        f"/verify6 <link> - Perplexity Pro student verification (-{VERIFY_COST} points)\n"
        "/getV4Code <verification_id> - Retrieve Bolt.new verification code\n"
        "/help - View this help message\n"
        f"For failed verifications, see: {HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\nAdmin commands:\n"
            "/addbalance <user_id> <points> - Add user points\n"
            "/block <user_id> - Block a user\n"
            "/white <user_id> - Unblock a user\n"
            "/blacklist - View the blacklist\n"
            "/genkey <code> <points> [uses] [days] - Generate a card key\n"
            "/listkeys - List card keys\n"
            "/broadcast <text> - Broadcast a message to all users\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Return the insufficient balance message."""
    return (
        f"Not enough points! {VERIFY_COST} points required, you currently have {current_balance}.\n\n"
        "How to earn points:\n"
        "- Daily check-in /qd\n"
        "- Invite friends /invite\n"
        "- Use a card key /use <code>"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Return usage guidance for verification commands."""
    return (
        f"Usage: {command} <SheerID link>\n\n"
        "Example:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "How to get the verification link:\n"
        f"1. Visit the {service_name} verification page\n"
        "2. Start the verification flow\n"
        "3. Copy the full URL from the browser address bar\n"
        f"4. Submit it with {command}"
    )
