from localshop.services.base import Service


class LocalShopWorker(Service):
    name = 'worker'

    def run(self):
        from localshop.queue.client import broker
        from localshop.queue.worker import Worker

        from kombu.utils.debug import setup_logging
        setup_logging(loglevel="INFO")

        try:
            Worker(broker.connection).run()
        except KeyboardInterrupt:
            print("bye bye")
