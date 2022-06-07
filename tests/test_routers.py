from io import BytesIO

import pytest
from fastapi import status
from PIL import Image, ImageChops

from app.schemas import Status


def construct_different_uuid(uuid):
    last_symbol = uuid[-1]
    if last_symbol == '0':
        return uuid[:-1:] + '1'
    return uuid[:-1:] + '0'


def test_create_job(client, image_file):
    files = {'file': ('test_image.jpg', image_file, 'image/jpeg')}
    response = client.post('/tasks/', files=files)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in data
    assert data['status'] == Status.DONE.value


def test_create_job_not_image(client, not_image_file):
    files = {'file': ('test_image.jpg', not_image_file, 'image/jpeg')}
    response = client.post('/tasks/', files=files)

    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    data = response.json()
    assert data['detail'] == 'Unsupported content type, image is expected'


def test_create_job_not_square_image(client, not_square_image_file):
    files = {'file': ('test_image.jpg', not_square_image_file, 'image/jpeg')}
    response = client.post('/tasks/', files=files)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data['detail'] == 'Only square images are accepted'


def test_get_job_info(client, job_id):
    response = client.get(f'/tasks/{job_id}')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == job_id
    assert data['status'] == Status.DONE.value


def test_get_job_info_invali_id(client, job_id):
    # here we need make sure that we are testing endpoint
    # with uuid different from generated in the fixture
    invalid_id = construct_different_uuid(job_id)
    response = client.get(f'/tasks/{invalid_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data['detail'] == 'Invalid job id'


def test_get_original_image(client, job_id, image):
    response = client.get(f'/tasks/{job_id}/image', params={'size': 'original'})
    assert response.status_code == 200

    data = response.content
    received_image = Image.open(BytesIO(data))

    assert not ImageChops.difference(image, received_image).getbbox()


@pytest.mark.parametrize('size', ['32', '64'])
def test_get_resized_image(client, job_id, size):
    response = client.get(f'/tasks/{job_id}/image', params={'size': size})
    assert response.status_code == 200

    data = response.content
    received_image = Image.open(BytesIO(data))
    assert received_image.size == (int(size), int(size))


def test_get_image_invali_id(client, job_id):
    # here we need make sure that we are testing endpoint
    # with uuid different from generated in the fixture
    invalid_id = construct_different_uuid(job_id)
    response = client.get(f'/tasks/{invalid_id}/image', params={'size': 'original'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data['detail'] == 'Invalid job id'
