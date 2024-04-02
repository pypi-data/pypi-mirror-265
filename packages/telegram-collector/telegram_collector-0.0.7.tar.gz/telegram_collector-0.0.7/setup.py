#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='telegram_collector',
    version='0.0.7',
    author='fengleicn',
    author_email='fengleisemail@gmail.com',
    url='https://github.com/fengleicn/telegram_collector',
    description=u'收集电报群组的视频图片消息',
    packages=['telegram_collector'],
    install_requires=['telethon', 'python_socks'],
    entry_points={
        'console_scripts': [
            'telegram_collector_send_current_message_src_to_dest=telegram_collector.__main__:send_current_message_src_to_dest',
            'telegram_collector_send_history_message_src_to_dest=telegram_collector.__main__:send_history_message_src_to_dest']
    }
)
