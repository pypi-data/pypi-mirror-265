import asyncio
import configparser
import math
import python_socks
from telethon import *


def get_config(option, fallback, section='default'):
    if parser.has_section(section):
        if parser.has_option(section, option):
            if fallback == None:
                return parser.get(section, option)
            elif type(fallback) == bool:
                return parser.getboolean(section, option)
            elif type(fallback) == str:
                return parser.get(section, option)
            elif type(fallback) == int:
                return parser.getint(section, option)
            elif type(fallback) == list:
                return list(map(lambda x: int(x), parser.get(section, option).split(',')))
    return fallback


def get_size(message):
    if is_video_or_photo(message):
        if message.video is not None:
            return message.video.size
        elif message.photo is not None:
            return message.photo.sizes[1].size
    else:
        raise Exception(message)


def get_file_reference(message):
    if is_video_or_photo(message):
        if message.video is not None:
            return str(message.video.file_reference)
        elif message.photo is not None:
            return str(message.photo.file_reference)
    else:
        raise Exception(message)


def is_video_or_photo(message) -> bool:
    return message.video is not None or message.photo is not None


def unique(messages):
    check_set = set()

    def check_unique(elem):
        def key_func(e):
            return get_size(e)

        key = key_func(elem)
        if key in check_set:
            return False

        else:
            check_set.add(key)
            return True

    unique_list = []
    for message in messages:
        if check_unique(message):
            unique_list.append(message)
    return unique_list


def sort(messages):
    ret = messages.copy()
    ret.sort(key=lambda m: get_size(m), reverse=True)
    return ret


async def refresh_history_messages(client, src_dialog):
    messages = await get_history_messages(client, src_dialog)
    messages = await filter_messages(messages)
    return messages


async def refresh_current_messages(client, src_dialog):
    messages = await get_current_messages(client, src_dialog)
    # messages = await filter_messages(messages)
    return messages


async def get_current_messages(client, dialogs):
    all_messages = []
    client.add_event_handler()
    for dialog in dialogs:
        messages = await client.get_messages(dialog)
        all_messages += messages
    return all_messages


async def print_dialogs(dialogs):
    for dialog in dialogs:
        print(dialog.id, dialog.title)


async def get_src_dialogs(dialogs):
    src_dialog = []
    for dialog in dialogs:
        if dialog.id in src_dialog_ids:
            src_dialog.append(dialog)
    return src_dialog


async def send_messages(client, dest_dialogs, messages):
    count = 0
    delay = 2.5
    for message in messages:
        count += 1
        print(count, end='.')
        for dest_dialog in dest_dialogs:
            try:
                await client.send_message(entity=dest_dialog, message=message)
            except Exception as e:
                print(e, message)
            finally:
                await asyncio.sleep(delay)


def get_video_or_photo(messages):
    ret = []
    for message in messages:
        if is_video_or_photo(message):
            ret.append(message)
    return ret


async def filter_messages(messages):
    start = len(messages)
    messages = get_video_or_photo(messages)
    messages = unique(messages)
    messages = sort(messages)
    end = len(messages)
    print('\nbefore filter: ', start, 'after filter: ', end)
    return messages


async def get_dialogs(client):
    dialogs = await client.get_dialogs()
    await print_dialogs(dialogs)
    return dialogs


async def get_dest_dialogs(dialogs):
    dest_dialogs = []
    for dialog in dialogs:
        if dialog.id in dest_dialog_ids:
            dest_dialogs.append(dialog)
    return dest_dialogs


async def get_history_messages(client, dialogs):
    all_messages = []
    for dialog in dialogs:
        messages = await client.get_messages(dialog, None)
        all_messages += messages
    return all_messages


async def new_client():
    client = TelegramClient(session_name, api_id, api_hash,
                            proxy=(proxy_type, proxy_ip, proxy_port) if use_proxy else None)
    await client.start()
    return client


async def terminate_client(client):
    await client.disconnect()


async def get_meta_info():
    client = await new_client()
    dialogs = await get_dialogs(client)
    src_dialogs = await get_src_dialogs(dialogs)
    dest_dialogs = await get_dest_dialogs(dialogs)
    return client, dest_dialogs, src_dialogs


async def do_send_history_message(client, dest_dialogs, src_dialogs):
    messages = await refresh_history_messages(client, src_dialogs)
    part_amount = math.ceil(len(messages) / iter_val)
    part_num = 1
    while part_num <= part_amount:
        messages = await split_message(part_num, iter_val, messages)
        await send_messages(client, dest_dialogs, messages)
        if part_num != part_amount:  # not last one
            messages = await refresh_history_messages(client, src_dialogs)
        part_num += 1


async def split_message(part, _iter_val, messages):
    end = part * _iter_val
    start = end - _iter_val
    messages = messages[start: end]
    return messages


async def send_history_message_src_to_dest():
    client, dest_dialogs, src_dialogs = await get_meta_info()
    await do_send_history_message(client, dest_dialogs, src_dialogs)
    await terminate_client(client)


async def send_current_message_src_to_dest():
    client, dest_dialogs, src_dialogs = await get_meta_info()

    async def callback(event):
        message = event.message
        src_dialog_id = event.message.chat_id
        if is_video_or_photo(message) and src_dialog_id in src_dialog_ids:
            await send_messages(client, dest_dialogs, [message])

    client.add_event_handler(callback, events.NewMessage(incoming=True))
    await asyncio.sleep(3600 * 24 * 30 * 12)


parser = configparser.ConfigParser()
read = parser.read('tg.ini')

# 参数
proxy_type = python_socks.ProxyType.SOCKS5
api_id = get_config('api_id', 0)
api_hash = get_config('api_hash', '0')
proxy_ip = get_config('proxy_ip', '127.0.0.1')
proxy_port = get_config('proxy_port', 7890)
session_name = get_config('session_name', 'tg_session')
src_dialog_ids = get_config('src_dialog_ids', [])
dest_dialog_ids = get_config('dest_dialog_ids', [])
iter_val = get_config('iter_val', 1000)
use_proxy = get_config('use_proxy', True)


def console():
    print("hello world!")
