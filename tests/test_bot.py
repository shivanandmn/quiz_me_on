from telegram import Bot
import asyncio
from get_parms import bot_token

async def test_bot():
    # Create an instance of the Bot class with your bot token
    bot = Bot(token=bot_token())

    # Use the getMe method to retrieve information about the bot
    bot_info = await bot.get_me()

    # Print the bot's username and ID if the token is valid
    print("Bot username:", bot_info.username)
    print("Bot ID:", bot_info.id)

# Run the test_bot coroutine
asyncio.run(test_bot())
