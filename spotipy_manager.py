import logging
import os
import spotipy
import time
from typing import List
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__file__)
logging.basicConfig(level='DEBUG')


class SpotipyManager():
    
    def __init__(self):
        self.sp = spotipy.Spotify(auth=self.get_oauth_token())
        self.playlist = os.environ['SPOTIFY_PLAYLIST_ID']
        
    def add_tracks_to_playlist(self, track_list: List[str]):
        self.sp.playlist_add_items(self.playlist, track_list)

    def get_oauth_token(self):
        s = SpotifyOAuth()
        # TODO: Esto es una guarrada
        endpoint = s.get_authorize_url().replace("response_type=code", "response_type=token")
        # TODO: Esto es una guarrada
        endpoint = endpoint + "&scope=playlist-modify-private"
        driver = webdriver.Chrome(chrome_options=self.get_chrome_options(), executable_path=os.environ['CHROMEDRIVER_PATH'])
        driver.get(endpoint)
        username_field = driver.find_element_by_id('login-username')
        username_field.send_keys(os.environ['SPOTIFY_USERNAME'])
        password_field = driver.find_element_by_id('login-password')
        password_field.send_keys(os.environ['SPOTIFY_PASSWORD'])
        login_button = driver.find_element_by_id('login-button')
        login_button.send_keys(Keys.ENTER)
        # TODO: Esto es una guarrada
        time.sleep(2)
        driver.implicitly_wait(5)
        url = urlparse(driver.current_url)
        logger.info(f"Access URL: {driver.current_url}")
        token = parse_qs(url.fragment)['access_token'][0]
        driver.quit()
        return token

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ['GOOGLE_CHROME_PATH']
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        return options