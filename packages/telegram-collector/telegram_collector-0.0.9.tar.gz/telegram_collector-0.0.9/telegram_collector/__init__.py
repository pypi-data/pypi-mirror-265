import asyncio
import configparser
import math
import python_socks
from telethon import *
from .util import *


class TelegramCollector:
    def __init__(self):
        self.dest_dialogs = None
        self.src_dialogs = None
        self.my_dialogs = None
        self.client = None
        self.proxy_type = None
        self.api_id = None
        self.api_hash = None
        self.proxy_ip = None
        self.proxy_port = None
        self.session_name = None
        self.src_dialog_ids = None
        self.dest_dialog_ids = None
        self.iter_val = None
        self.use_proxy = None

        self.parser = configparser.ConfigParser()
        self.parser.read('tg.ini')

    async def __do_init(self):
        # 参数
        self.proxy_type = python_socks.ProxyType.SOCKS5
        self.api_id = get_config(self.parser, 'api_id', 0)
        self.api_hash = get_config(self.parser, 'api_hash', '0')
        self.proxy_ip = get_config(self.parser, 'proxy_ip', '127.0.0.1')
        self.proxy_port = get_config(self.parser, 'proxy_port', 7890)
        self.session_name = get_config(self.parser, 'session_name', 'tg_session')
        self.src_dialog_ids = get_config(self.parser, 'src_dialog_ids', [])
        self.dest_dialog_ids = get_config(self.parser, 'dest_dialog_ids', [])
        self.iter_val = get_config(self.parser, 'iter_val', 1000)
        self.use_proxy = get_config(self.parser, 'use_proxy', True)

        proxy = (self.proxy_type, self.proxy_ip, self.proxy_port) if self.use_proxy else None
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                     proxy=proxy)
        await self.client.start()

        self.my_dialogs = await self.__get_my_dialogs()
        self.src_dialogs = await self.__get_src_dialogs()
        self.dest_dialogs = await self.__get_dest_dialogs()

    async def __get_my_dialogs(self):
        dialogs = await self.client.get_dialogs()
        await print_dialogs(dialogs)
        return dialogs

    async def __get_src_dialogs(self):
        src_dialog = []
        for dialog in self.my_dialogs:
            if dialog.id in self.src_dialog_ids:
                src_dialog.append(dialog)
        return src_dialog

    async def __get_dest_dialogs(self):
        dest_dialogs = []
        for dialog in self.my_dialogs:
            if dialog.id in self.dest_dialog_ids:
                dest_dialogs.append(dialog)
        return dest_dialogs

    async def __get_history_messages(self):
        all_messages = []
        for dialog in self.src_dialogs:
            messages = await self.client.get_messages(dialog, None)
            all_messages += messages
        return all_messages

    async def __refresh_history_messages(self):
        messages = await self.__get_history_messages()
        messages = await filter_messages(messages)
        return messages

    async def __send_messages(self, messages):
        count = 0
        delay = 2.5
        for message in messages:
            count += 1
            print(count, end='.')
            for dest_dialog in self.dest_dialogs:
                try:
                    await self.client.send_message(entity=dest_dialog, message=message)
                except Exception as e:
                    print(e, message)
                finally:
                    await asyncio.sleep(delay)

    async def __terminate_client(self):
        await self.client.disconnect()

    # 批量汇总全量消息
    async def __send_history_message_src_to_dest(self):
        try:
            messages = await self.__refresh_history_messages()
            part_amount = math.ceil(len(messages) / self.iter_val)
            part_num = 1
            while part_num <= part_amount:
                messages = await split_message(part_num, self.iter_val, messages)
                await self.__send_messages(messages)
                if part_num != part_amount:  # not last one
                    messages = await self.__refresh_history_messages()
                part_num += 1
        finally:
            await self.__terminate_client()

    async def callback(self, event):
        message = event.message
        src_dialog_id = event.message.chat_id
        print('get: ', message)
        if message_is_video_or_photo(message) and src_dialog_id in self.src_dialog_ids:
            await self.__send_messages([message])

    # 流式汇总增量消息
    async def __send_current_message_src_to_dest(self):
        self.client.add_event_handler(self.callback, events.NewMessage(incoming=True))

        try:
            while True:
                await asyncio.sleep(1)
        finally:
            await self.__terminate_client()

    def send_current_message_src_to_dest(self):
        asyncio.run(self.__send_current_message_src_to_dest())

    def send_history_message_src_to_dest(self):
        asyncio.run(self.__send_history_message_src_to_dest())

    def do_init(self):
        asyncio.run(self.__do_init())


def console():
    print("hello world!")
