__all__ = ["AiohttpSession"]

import asyncio
from json import JSONDecodeError

from aiohttp import ClientSession, MultipartWriter
from aiohttp.client_exceptions import ContentTypeError
import aiofiles
from aiofiles import os as async_os
import async_timeout

from ..models import Response
from .abc import AbstractSession


async def _get_file_size(full_file_path):
    stat = await async_os.stat(full_file_path)
    return stat.st_size


async def _aiter_file(file_name, chunk_size):
    """ Async file generator """
    async with aiofiles.open(file_name, "rb") as f:
        chunk = await f.read(chunk_size)
        while chunk:
            yield chunk
            chunk = await f.read(chunk_size)


async def _read_file(file_name):
    async with aiofiles.open(file_name, "rb") as file:
        return await file.read()


class AiohttpSession(ClientSession, AbstractSession):
    async def send(
        self,
        *requests,
        timeout=None,
        full_res=False,
        raise_for_status=True,
        session_factory=None,
        auth_manager=None
    ):
        async def resolve_response(request, response):
            data = None
            json = None
            download_file = None
            upload_file = None
            pipe_from = None
            pipe_to = None

            # If downloading file:
            if request.media_download:
                chunk_size = request.media_download.chunk_size
                download_file = request.media_download.file_path
                pipe_to = request.media_download.pipe_to

                if pipe_to:
                    async for line in response.content.iter_chunked(chunk_size):
                        await pipe_to.write(line)

                if download_file:
                    async with aiofiles.open(download_file, "wb+") as f:
                        async for line in response.content.iter_chunked(chunk_size):
                            await f.write(line)
            else:
                if response.status != 204:  # If no (no content)
                    try:
                        json = await response.json()
                    except (JSONDecodeError, ContentTypeError):
                        try:
                            data = await response.text()
                        except ContentTypeError:
                            try:
                                data = await response.read()
                            except ContentTypeError:
                                data = None

            if request.media_upload:
                upload_file = request.media_upload.file_path

            return Response(
                url=str(response.url),
                headers=response.headers,
                status_code=response.status,
                json=json,
                data=data,
                reason=response.reason if getattr(response, "reason") else None,
                req=request,
                download_file=download_file,
                pipe_to=pipe_to,
                upload_file=upload_file,
                pipe_from=pipe_from,
                session_factory=session_factory,
                auth_manager=auth_manager
            )

        async def fire_request(request):
            request.headers["Accept-Encoding"] = "gzip"
            request.headers["User-Agent"] = "Aiogoogle Aiohttp (gzip)"
            if request.media_upload:
                # Validate
                await request.media_upload.run_validation(_get_file_size)

                # If multipart pass a file async generator
                if request.media_upload.multipart is True:
                    with MultipartWriter('mixed') as mpwriter:
                        mpwriter.append_json(request.json)

                        mpwriter.append(
                            request.media_upload.aiter_file(_aiter_file),
                            headers={"Content-Type": request.upload_file_content_type} if request.upload_file_content_type else None
                        )

                        req_content_type = 'multipart/related'

                        request.headers.update({"Content-Type": f"{req_content_type}; boundary={mpwriter.boundary}"})

                        return await self.request(
                            method=request.method,
                            url=request.media_upload.upload_path,
                            headers=request.headers,
                            data=mpwriter,
                            timeout=request.timeout,
                            verify_ssl=request._verify_ssl,
                        )
                # Else load file to memory and send
                else:
                    read_file = await request.media_upload.read_file(_read_file)
                    if request.upload_file_content_type:
                        request.headers.update({"Content-Type": request.upload_file_content_type})
                    return await self.request(
                        method=request.method,
                        url=request.media_upload.upload_path,
                        headers=request.headers,
                        data=read_file,
                        json=request.json,
                        timeout=request.timeout,
                        verify_ssl=request._verify_ssl,
                    )
            # Else, if no file upload
            else:
                return await self.request(
                    method=request.method,
                    url=request.url,
                    headers=request.headers,
                    data=request.data,
                    json=request.json,
                    timeout=request.timeout,
                    verify_ssl=request._verify_ssl,
                )

        # ----------------- send sequence ------------------#
        async def get_response(request):
            response = await fire_request(request)
            response = await resolve_response(request, response)
            if raise_for_status is True:
                response.raise_for_status()
            return response

        async def get_content(request):
            response = await get_response(request)
            return response.content

        # ----------------- /send sequence ------------------#

        async def schedule_tasks():
            if full_res is True:
                tasks = [
                    asyncio.ensure_future(get_response(request)) for request in requests
                ]
            else:
                tasks = [
                    asyncio.ensure_future(get_content(request)) for request in requests
                ]
            return await asyncio.gather(*tasks, return_exceptions=False)

        session_factory = self.__class__ if session_factory is None else session_factory

        if timeout is not None:
            async with async_timeout.timeout(timeout):
                results = await schedule_tasks()
        else:
            results = await schedule_tasks()

        return (
            results[0] if isinstance(results, list) and len(results) == 1 else results
        )
