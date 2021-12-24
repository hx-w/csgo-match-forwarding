# -*- coding: utf-8 -*-
import aiohttp
import asyncio

class AsyncRequest:
    def __init__(self, urls=[]):
        self.urls = urls

    async def __fetch(self, client: aiohttp.ClientSession, url: str):
        async with client.get(url) as resp:
            assert resp.status == 200
            return await resp.json()


    async def __fetch_task(self):
        async with aiohttp.ClientSession() as client:
            tasks = [asyncio.create_task(
                self.__fetch(client, url)) for url in self.urls]
            return await asyncio.wait(tasks)


    def request(self) -> list:
        # exception check TODO
        loop = asyncio.get_event_loop()
        done, _ = loop.run_until_complete(self.__fetch_task())
        loop.close()
        return [fut.result() for fut in done]


def main():
    req_inst = AsyncRequest([
        'https://hltv-api.netlify.app/.netlify/functions/news',
        'https://hltv-api.netlify.app/.netlify/functions/results'
    ])
    res = req_inst.request()
    print(len(res))


if __name__ == '__main__':
    main()
