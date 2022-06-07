from fastapi import HTTPException, status

InvalidJobId = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail='Invalid job id'
)

JobNotFinished = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail='The job is not finished yet'
)

ServiceUnavailable = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail='The service is not available at the moment, try again later',
)

IncorrectImageFormat = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Only square images are accepted',
)

NotImage = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail='Unsupported content type, image is expected',
)
