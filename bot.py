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
            response = send_unique_tracks(api, tracks)
            update.message.reply_text(response)
        except Exception:
            update.message.reply_text("❌ Algo falló :(")

def send_unique_tracks(api: SpotipyManager, tracks: list):
    current_tracks = api.get_playlist_tracks()
    unique_tracks = list(set(tracks) - set(current_tracks))
    duplicate_tracks = len(tracks) - len(unique_tracks)
    api.add_tracks_to_playlist(unique_tracks)
    number_uniques, number_duplicates = (len(unique_tracks), len(duplicate_tracks))
    if number_uniques > 0:
        if number_duplicates > 0:
            return f'✔️ Allright! {len(duplicate_tracks)} ya estaban, el resto se añadieron'
        return '✔️ Allright! Gracias :)'
    return 'Este temardo ya estaba en la playlist'

def main(local: bool):
    """Start the bot."""
    token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, find_and_send_tracks))

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
        logger.info("Starting bot locally")
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        load_dotenv(env_file)
        main(local=True)
    else:
        logger.info("Starting bot prod")
        main(local=False)