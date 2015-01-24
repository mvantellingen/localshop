import pytest
from SimpleXMLRPCServer import SimpleXMLRPCServer

from tests.utils import PyPiXMLRPCStub
import threading


@pytest.yield_fixture(scope='module')
def pypi_stub():
    server = SimpleXMLRPCServer(('localhost', 12946), allow_none=True)
    server.register_instance(PyPiXMLRPCStub())

    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()
