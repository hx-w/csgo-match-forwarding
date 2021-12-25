# -*- coding: utf-8 -*-
import aiohttp
import asyncio

class AsyncRequest:
    def __init__(self, urls=[]):
        self.urls = urls

    async def __fetch(self, client: aiohttp.ClientSession, url: str) -> list:
        async with client.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f'[ERR] {resp.status} in {url}')
                return []


    async def __fetch_task(self, urls):
        async with aiohttp.ClientSession() as client:
            tasks = [asyncio.create_task(
                self.__fetch(client, url)) for url in urls]
            return await asyncio.wait(tasks)


    async def request(self, urls = []) -> list:
        if urls == []:
            urls = self.urls
        done, _ = await self.__fetch_task(urls)
        return [fut.result() for fut in done]