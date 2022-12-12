# -*- coding: utf-8 -*-
import requests
import aiohttp
import asyncio


class AsyncRequest:
    def __init__(self):
        pass

    async def __fetch(self, client: aiohttp.ClientSession, url: str, bin: bool) -> list:
        async with client.get(url) as resp:
            if resp.status == 200:
                if bin:
                    return await resp.read()
                return await resp.json()
            else:
                print(f'[ERR] {resp.status} in {url}')
                return []

    async def __fetch_task(self, urls, bin: bool):
        async with aiohttp.ClientSession() as client:
            tasks = [asyncio.create_task(
                self.__fetch(client, url, bin)) for url in urls]
            return await asyncio.wait(tasks)

    async def request(self, urls=[], bin: bool = False) -> list:
        print('requesting urls: ', urls)
        done, _ = await self.__fetch_task(urls, bin)
        return [fut.result() for fut in done]

    def request_sync(self, url: str) -> bytes:
        resp = requests.get(url)
        if resp.status_code != 200:
            resp = requests.get(url)
        return resp.content


req_inst = AsyncRequest()


__all__ = [req_inst]
