import pytest
from wsgiref.simple_server import make_server
from tests.utils import pypi_app
import threading


@pytest.yield_fixture(scope='module')
def pypi_stub():
    server = make_server('', 12946, pypi_app)  # Same port as LOCALSHOP_PYPI_URL

    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()
