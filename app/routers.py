from typing import IO

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from pydantic import UUID4
from rq import Queue
from rq.job import Job

from app.dependencies import get_queue
from app.exceptions import (
    IncorrectImageFormat,
    InvalidJobId,
    JobNotFinished,
    NotImage,
    ServiceUnavailable,
)
from app.image_process import b64decode, resize_image
from app.schemas import HTTPError, ImageSize, JobInfo, Status

router = APIRouter(
    prefix='/tasks',
    responses={
        ServiceUnavailable.status_code: {
            'model': HTTPError,
            'description': ServiceUnavailable.detail,
        },
    },
)


def add_redis_job(image_data: IO[bytes], image_resizer_queue: Queue) -> Job:
    try:
        image = Image.open(image_data)
    except UnidentifiedImageError as err:
        raise NotImage from err

    if image.height != image.width:
        raise IncorrectImageFormat

    job = image_resizer_queue.enqueue(resize_image, image, result_ttl='1d')
    return job


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=JobInfo,
    responses={
        NotImage.status_code: {
            'model': HTTPError,
            'description': NotImage.detail,
        },
        IncorrectImageFormat.status_code: {
            'model': HTTPError,
            'description': IncorrectImageFormat.detail,
        },
    },
)
def create_job(
    file: UploadFile, image_resizer_queue: Queue = Depends(get_queue)
) -> JobInfo:
    job = add_redis_job(file.file, image_resizer_queue)
    job_status = job.get_status()
    return JobInfo(id=job.id, status=Status.from_job_status(job_status))


@router.get(
    '/{job_id}',
    status_code=status.HTTP_200_OK,
    response_model=JobInfo,
    responses={
        InvalidJobId.status_code: {
            'model': HTTPError,
            'description': InvalidJobId.detail,
        },
    },
)
def get_job_info(
    job_id: UUID4, image_resizer_queue: Queue = Depends(get_queue)
) -> JobInfo:
    job = image_resizer_queue.fetch_job(str(job_id))
    if job is None:
        raise InvalidJobId
    job_status = job.get_status()
    return JobInfo(id=job.id, status=Status.from_job_status(job_status))


@router.get(
    '/{job_id}/image',
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={
        InvalidJobId.status_code: {
            'model': HTTPError,
            'description': InvalidJobId.detail,
        },
        JobNotFinished.status_code: {
            'model': HTTPError,
            'description': JobNotFinished.detail,
        },
    },
)
def get_image(
    job_id: UUID4,
    size: ImageSize = ImageSize.IMAGE_32,
    image_resizer_queue: Queue = Depends(get_queue),
) -> Response:
    job = image_resizer_queue.fetch_job(str(job_id))
    if job is None:
        raise InvalidJobId

    job_status = job.get_status()
    if Status.from_job_status(job_status) != Status.DONE:
        raise JobNotFinished

    if size == ImageSize.IMAGE_32:
        image_data = job.result.IMAGE_32
    elif size == ImageSize.IMAGE_64:
        image_data = job.result.IMAGE_64
    else:
        image_data = job.result.IMAGE_ORIGINAL

    # here we don't need to get image object (only getting decoded from base64 bytes)
    img_byte_arr = b64decode(image_data)

    return Response(content=img_byte_arr, media_type='image/png')
