from .__init__ import TelegramCollector


def main():
    collector = TelegramCollector()
    collector.do_init()
    collector.send_current_message_src_to_dest()


if __name__ == '__main__':
    main()