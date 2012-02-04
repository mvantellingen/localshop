from localshop.services.base import Service


class LocalShopWorker(Service):
    name = 'worker'

    def run(self):
        from celery.bin import celeryd
        from djcelery.app import app

        worker = celeryd.WorkerCommand(app=app)
        worker.run()
