# coding: utf-8

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # load local .env file

# For slackbot
API_TOKEN = os.environ["TOKEN"]
DEFAULT_REPLY = "わかんないよ〜ん"
PLUGINS = ['plugins']


CHANNEL_ID = os.environ["CHANNEL_ID"]
USER1 = os.environ["USER1"]
USER2 = os.environ["USER2"]
