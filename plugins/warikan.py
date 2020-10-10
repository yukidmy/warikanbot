# coding: utf-8

import json
import psycopg2
from psycopg2.extras import DictCursor

from slackbot import settings
from slackbot.bot import listen_to
from slackbot.bot import respond_to


@respond_to(r'^(?:りせっと|リセット|reset|Reset|RESET)$')
def reset(message):
    if reset_func():
        message.reply('おっけ〜リセットしたよ')
    else:
        message.reply('リセット失敗！　また今度試してね')


@respond_to(r'^([-+]?\d*)[ 　]')
@listen_to(r'^([-+]?\d*)[ 　]')
def warikan(message, price):
    if message.body['channel'] != settings.CHANNEL_ID:
        return
    if message.user['name'] not in [settings.USER1, settings.USER2]:
        return {'error': '誰だかわかんなかった！！　つらい〜！！'}
    result = warikan_func(message.user['name'], int(price))
    if 'error' in result:
        message.reply(result['error'])
    elif result['price'] == 0:
        message.reply('記録したよ！　ぴったり割り勘できたね！')
    else:
        formatted_price = '{:,}'.format(result["price"])
        attachments = [{
            'fallback': f'{result["from"]} → {result["to"]}: {result["price"]}',
            'color': 'good',
            'title': f'{result["from"]} → {result["to"]}',
            'text': f'{formatted_price} 円'
        }]
        message.send_webapi('', json.dumps(attachments))


def reset_func():
    print('Reset')
    try:
        with psycopg2.connect(settings.DATABASE_URL, sslmode='require') as db:
            with db.cursor(cursor_factory=DictCursor) as cur:
                df = {settings.USER1: 0, settings.USER2: 0}
                print({'new': df})
                query = """UPDATE warikan SET price = %s where name = %s"""
                for k, v in df.items():
                    cur.execute(query, (v, k))
                db.commit()
        print('Resetted')
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)
        return False


def warikan_func(name, price):
    print('Warikan', name, price)
    try:
        with psycopg2.connect(settings.DATABASE_URL, sslmode='require') as db:
            with db.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM warikan')
                data = cur.fetchall()
                df = {}
                if not data:
                    df = {settings.USER1: 0, settings.USER2: 0}
                else:
                    for d in data:
                        df[d[0]] = d[1]
                print({'prev': df})
                df[name] += price
                result = {}
                if df[settings.USER1] > df[settings.USER2]:
                    df[settings.USER1] -= df[settings.USER2]
                    df[settings.USER2] = 0
                    diff = df[settings.USER1] // 2
                    result = {'from': settings.USERNAME2,
                              'to': settings.USERNAME1, 'price': diff}
                else:
                    df[settings.USER2] -= df[settings.USER1]
                    df[settings.USER1] = 0
                    diff = df[settings.USER2] // 2
                    result = {'from': settings.USERNAME1,
                              'to': settings.USERNAME2, 'price': diff}
                print({'new': df})
                query = """UPDATE warikan SET price = %s where name = %s"""
                for k, v in df.items():
                    cur.execute(query, (v, k))
                db.commit()
        return result
    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)
        return {'error': error}
