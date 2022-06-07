# Image Resizer

## Description:
Web service providing API for resizing images. The user via endpoint can create a task to resize the picture. 
After that one can get the task status and download the picture in the desired resolution (32x32, 64x64 or original size).

## Makefile commands

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Run service:
    make up

You can then access the service at 
```
http://localhost:80/
```

## API Endpoints

| HTTP Method | Endpoint              | Action                                            | Response                        |
|-------------|-----------------------|---------------------------------------------------|---------------------------------|
| POST        | /tasks/               | To create a task to resize an image               | Task information (UUID, status) | 
| GET         | /tasks/{job_id}       | To get information about job with UUID = `job_id` | Task information (UUID, status) | 
| GET         | /tasks/{job_id}/image | To get information about your account             | Resized image**                 |

** Make sure that you specify the desired resolution in the `size` query parameter ('32', '64', 'original'), otherwise
the service will return you an image with 32x32 resolution.

To get full details about endpoints go to  
```
http://localhost:80/docs
```