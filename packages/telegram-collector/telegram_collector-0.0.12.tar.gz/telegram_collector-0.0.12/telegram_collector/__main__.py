from .__init__ import TelegramCollector


def send_current_message_src_to_dest():
    TelegramCollector().send_current_message_src_to_dest()


def send_history_message_src_to_dest():
    TelegramCollector().send_history_message_src_to_dest()
