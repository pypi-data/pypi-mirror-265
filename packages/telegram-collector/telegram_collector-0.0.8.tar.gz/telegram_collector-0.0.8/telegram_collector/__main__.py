from .__init__ import TelegramCollector


def send_current_message_src_to_dest():
    collector = TelegramCollector()
    collector.do_init()
    collector.send_current_message_src_to_dest()


def send_history_message_src_to_dest():
    collector = TelegramCollector()
    collector.do_init()
    collector.send_history_message_src_to_dest()



