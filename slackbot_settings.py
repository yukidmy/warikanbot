# coding: utf-8

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # Load local .env file

# Slackbot settings
API_TOKEN = os.environ["TOKEN"]
DEFAULT_REPLY = "わかんないよ〜ん"
PLUGINS = ['plugins']

# Personal settings
CHANNEL_ID = os.environ["CHANNEL_ID"]
USER1 = os.environ["USER1"]
USER2 = os.environ["USER2"]
USERNAME1 = os.environ["USERNAME1"]
USERNAME2 = os.environ["USERNAME2"]
DATABASE_URL = os.environ["DATABASE_URL"]
