import logging
import argparse
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from spotify_parser import SpotifyParser
from spotipy_manager import SpotipyManager
import os

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def find_and_send_tracks(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    parser = SpotifyParser()
    tracks = parser.parse_songs(update.message.text)
    if len(tracks) > 0:
        update.message.reply_text("🎶 Añadiendo a playlist...")
        api = SpotipyManager()
        try:
            api.add_tracks_to_playlist(tracks)
            update.message.reply_text("✔️ Allright!")
        except Exception:
            update.message.reply_text("❌ Algo falló :(")

def debug_in_prod(update: Update, context: CallbackContext) -> None:
    if "ping" in update.message.text:
        update.message.reply("pong")

def main(local: bool):
    """Start the bot."""
    token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, find_and_send_tracks))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, debug_in_prod))

    if local:
        updater.start_polling()
        updater.idle()

    if not local:
        updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=token)
        updater.bot.setWebhook('https://musikilla-bot.herokuapp.com/' + token)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--local", action='store_true', help="run locally")
    parser.add_argument("-p", "--prod", action='store_true', help="run prod mode")
    args = parser.parse_args()
    if args.local:
        from dotenv import load_dotenv
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        load_dotenv(env_file)
        main(local=True)
    else:
        main(local=False)