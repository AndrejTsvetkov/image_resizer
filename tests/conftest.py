# pylint: disable=W0621
import pytest
from fakeredis import FakeStrictRedis
from fastapi.testclient import TestClient
from PIL import Image
from rq import Queue

from app.dependencies import get_queue
from app.image_process import resize_image
from app.main import app

queue = Queue(is_async=False, connection=FakeStrictRedis())


def fake_queue():
    return queue


@pytest.fixture(scope='session')
def client():
    app.dependency_overrides[get_queue] = fake_queue
    return TestClient(app)


@pytest.fixture(scope='session')
def client_no_deps():
    return TestClient(app)


@pytest.fixture(scope='session')
def image():
    return Image.open('tests/files/test_image.jpg')


@pytest.fixture(scope='session')
def image_32_base64():
    with open('tests/files/test_image_32_base64.txt', 'rb') as file:
        return file.read()


@pytest.fixture(scope='session')
def image_64_base64():
    with open('tests/files/test_image_64_base64.txt', 'rb') as file:
        return file.read()


@pytest.fixture(scope='session')
def image_base64():
    with open('tests/files/test_image_base64.txt', 'rb') as file:
        return file.read()


@pytest.fixture(scope='session')
def image_file():
    with open('tests/files/test_image.jpg', 'rb') as file:
        yield file


@pytest.fixture(scope='session')
def not_image_file():
    with open('tests/files/not_image.txt', 'rb') as file:
        yield file


@pytest.fixture(scope='session')
def not_square_image_file():
    with open('tests/files/not_square_image.jpg', 'rb') as file:
        yield file


@pytest.fixture(scope='session')
def job_id(image):
    job = queue.enqueue(resize_image, image)
    return job.id
