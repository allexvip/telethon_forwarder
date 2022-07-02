import configparser
import json
import logging
from telethon.sync import TelegramClient, events
from telethon.tl.types import InputMessagesFilterVideo

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
channels_list_from = config['Telegram']['channels_list_from'].split(',')
channels_list_from = list(map(int, channels_list_from))
channel_to = config['Telegram']['channel_to']

with TelegramClient('name', api_id, api_hash) as client:

    for dialog in client.iter_dialogs():
        print(dialog.id, dialog.title)


    @client.on(events.NewMessage(pattern='(?i).*Привет'))
    async def handler(event):
        await event.reply(f'И тебе привет {event.id}')


    @client.on(events.NewMessage(channels_list_from))
    async def main(event):
        print(event.message)
        await client.forward_messages(channel_to, event.message)

    client.run_until_disconnected()
