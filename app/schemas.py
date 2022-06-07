from __future__ import annotations

from enum import Enum

from pydantic import UUID4, BaseModel


class Status(Enum):
    WAITING = 'WAITING'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    FAILED = 'FAILED'

    @staticmethod
    def from_job_status(status: str) -> Status:
        mapping = {
            'queued': Status.WAITING,
            'finished': Status.DONE,
            'failed': Status.FAILED,
            'started': Status.IN_PROGRESS,
            'deferred': Status.WAITING,
            'scheduled': Status.WAITING,
            'stopped': Status.FAILED,
            'canceled': Status.FAILED,
        }
        return mapping[status]


class JobInfo(BaseModel):
    id: UUID4
    status: Status


class ImageSize(Enum):
    IMAGE_32 = '32'
    IMAGE_64 = '64'
    IMAGE_ORIGINAL = 'original'


class ImageResult(BaseModel):
    IMAGE_32: bytes
    IMAGE_64: bytes
    IMAGE_ORIGINAL: bytes


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'HTTP Exception'},
        }
