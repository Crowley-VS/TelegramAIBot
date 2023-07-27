import telebot
from bot import TelegramBot, WebhookManager, load_environment_variables
import os

if __name__ == '__main__':
    load_environment_variables()
    webhook_url = os.environ.get('WEBHOOK_URL')  # Get the webhook URL from the environment variables

    if webhook_url is None:
        raise ValueError("Webhook URL not set. Please provide your Render-provided webhook URL in the environment variables.")
    
    bot = TelegramBot()
    webhook_manager = WebhookManager(bot, webhook_url)
    webhook_manager.run()
    