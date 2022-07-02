import configparser
import json
import logging
from telethon.sync import TelegramClient, events
from telethon.tl.types import InputMessagesFilterVideo
from moviepy.editor import *

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
phone_number = '+79269295455'
channel_username = 'PapaIVanya'
discounts_channels_list = [
    -1001422930650,
    -1001122357347,
    -1001129241203,
    # 80387796,
]


# Printing download progress
def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))


async def check_video(chatid, local_video_in_file_path, local_video_out_file_path, sec_end):
    result = {}
    result['status'] = False
    result['duration'] = 0
    try:
        video = VideoFileClip(local_video_in_file_path)
        result['duration'] = float(video.duration)
        sec_end = float(sec_end)
        if result['duration'] > sec_end:
            video = video.subclip(0, sec_end)
        else:
            video = video.subclip(0, result['duration'])
        result_video = CompositeVideoClip([video])
        result_video.write_videofile(local_video_out_file_path)
        result['status'] = True
    except Exception as e:
        result['error'] = f'{chatid} \n{local_video_in_file_path}\n\n{str(e)}'
    return result


with TelegramClient('name', api_id, api_hash) as client:
    # client.send_message('me', 'Hello, myself!')
    # print(client.download_profile_photo('me'))

    for dialog in client.iter_dialogs():
        print(dialog.id, dialog.title)


    @client.on(events.NewMessage(pattern='(?i).*Привет'))
    async def handler(event):
        await event.reply(f'И тебе привет {event.id}')


    @client.on(events.NewMessage(discounts_channels_list))
    async def main(event):
        print(event.message)
        await client.forward_messages(-1001573630357, event.message)


    # @client.on(events.NewMessage())
    # async def handler(event):
    #     message = event.message
    #     print(event)
    #     print(message)
    #     print(message.media)
    #     media_file_datetime_str = str(message.date).replace('+00:00', '').replace(':', '_').replace(' ', '_')
    #     file_path = f"video/{message.message}_{media_file_datetime_str}"
    #     try:
    #         if message.media != 'None' and message.peer_id.user_id == 5246541938:
    #             local_video_in_file_path = await client.download_media(message, file=file_path, progress_callback=callback)
    #             print(local_video_in_file_path)
    #             local_video_out_file_path = local_video_in_file_path.replace('.mp4','_out.mp4')
    #             video_info = await check_video(message.message, local_video_in_file_path, local_video_out_file_path,60)
    #     except Exception as e:
    #         pass
            # if video_info['status']:
            #     await log_db_add(message.from_user.id,
            #                      f'Принято видео от пользователя продолжительностью {video_info["duration"]} сек.')
            #     await message.answer(f"Видео на {video_info['duration']} сек")
            #     await bot.send_video(message.from_user.id, open(local_video_out_file_path, 'rb'))
            # else:
            #     await bot.send_message(service_chatid, video_info['error'])
            #     await log_db_add(log_db_addmessage.from_user.id, f'Ошибка анализа видео от пользователя {video_info["error"]}')


    # Message(id=786, peer_id=PeerUser(user_id=80387796), date=datetime.datetime(2022, 7, 1, 14, 17, 40, tzinfo=datetime.timezone.utc), message='Тест', out=False, mentioned=False, media_unread=False, silent=False, post=None, from_scheduled=None, legacy=None, edit_hide=None, pinned=None, from_id=PeerUser(user_id=80387796), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[], ttl_period=None)

    # @client.on(events.NewMessage())
    # async def handler_video(event):
    #     for message in client.iter_messages(event.user_id, filter=):
    #         if message.video:
    #             path = await message.download_media()
    #             print('File saved to', path)  # printed after download is done
    #         await client.send_message(event.user_id, 'Ответ'+str(event))

    client.run_until_disconnected()
