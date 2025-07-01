# Just-A-Bot

A feature-rich Discord bot with customizable prefix, message management, and interactive commands.

## Features

- 🔧 **Customizable Prefix**: Set different prefixes per server
- 🗑️ **Message Management**: Delete messages in bulk (Admin only)
- 💬 **Message Echo**: Echo messages using `%` prefix
- 👋 **Slash Commands**: Modern Discord slash command support
- 🔒 **Permission System**: Admin-only access for sensitive operations

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/just-a-bot.git
   cd just-a-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the project root
   - Add your Discord bot token and optional guild ID:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   GUILD_ID=your_guild_id_here  # Optional: for faster command syncing
   ```

4. **Run the bot**:
   ```bash
   python bot.py
   ```

## Commands

### Prefix Commands (Dynamic Prefix)

#### `[prefix]setprefix <new_prefix>`
- **Permission**: Administrator only
- **Description**: Change the bot's prefix for the current server
- **Example**: `$setprefix !` or `!setprefix ?`

#### `[prefix]delete <number|all>`
- **Permission**: Administrator only
- **Description**: Delete messages in the current channel
- **Options**:
  - `[prefix]delete all` - Delete all messages in the channel
  - `[prefix]delete 10` - Delete the last 10 messages
- **Example**: `$delete 5` or `!delete all`

### Echo Feature

#### `%<message>`
- **Permission**: All users
- **Description**: Make the bot echo your message
- **Example**: `%Hello, world!`

### Slash Commands

#### `/greet`
- **Description**: Bot sends a greeting message
- **Response**: "hey how are you doing"

#### `/sendthis <message>`
- **Description**: Bot sends your specified message
- **Example**: `/sendthis Hello everyone!`

## Configuration

### Default Prefix
- The bot starts with `$` as the default prefix
- Each server can set its own custom prefix
- Prefixes are stored in `prefix.json`

### Permissions Required
- **Bot Permissions**:
  - Send Messages
  - Manage Messages (for delete command)
  - Use Slash Commands
  - Read Message History

- **User Permissions**:
  - Administrator: Required for `setprefix` and `delete` commands
  - Regular users: Can use echo feature and slash commands

## Security Features

- ✅ Admin-only access for sensitive operations
- ✅ Permission checks for all destructive commands
- ✅ Per-server prefix isolation
- ✅ Environment variable protection

## File Structure

```
just-a-bot/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not tracked)
├── prefix.json        # Prefix storage (auto-generated)
└── README.md          # This file
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Your Discord bot token |
| `GUILD_ID` | No | Guild ID for faster command syncing |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**⚠️ Important**: Never share your `.env` file or bot token publicly!