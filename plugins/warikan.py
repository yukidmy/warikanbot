# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to

error_message = 'よくわかんなかった！'


@respond_to('リセット')  # メンションにお返事
def reset_func(message):
    if reset():
        message.reply('おっけ〜リセットしたよ')
    else:
        message.reply(error_message)


@respond_to(r'^(?:割り勘|わりかん|warikan) (\d*)')  # メンションにお返事
def mention_func(message, price):
    warikan(price)
    message.reply(price)


@listen_to(r'^(?:割り勘|わりかん|warikan) (\d*)')  # チャンネル内発言にお返事
def listen_func(message, price):
    warikan(price)
    message.reply(price)


def warikan(price):
    return {'name': price}


def reset():
    return True
