import consumer.consumer_manager as cm


def main():

    consumer_manager = cm.ConsumeManager()
    consumer_manager.start_consumption_all_consumers()


if __name__ == '__main__':
    main()
