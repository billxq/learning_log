#!/usr/bin/env python
# coding: utf-8

import asyncio
import aiohttp
from lxml import html
import time


index_url = 'http://pic.netbian.com'


async def fetch(session, url):
    async with session.get(url, verify_ssl=False) as response:
        pic_name = url.split('/')[-1]
        print('开始下载%s' % pic_name)
        content = await response.read()
        with open(pic_name, 'wb') as f:
            f.write(content)


async def get_img_url(session, index_url):
    img_url_list = []
    async with session.get(index_url, verify_ssl=False) as response:
        text = await response.text()
        tree = html.fromstring(text)
        for each in tree.xpath('//ul[@class="clearfix"]/li'):
            img_url = 'http://pic.netbian.com' + each.xpath('.//a/span/img/@src')[0]
            img_url_list.append(img_url)
    return img_url_list


async def main():
    async with aiohttp.ClientSession() as session:
        img_url_list = await get_img_url(session, index_url)
        tasks = [asyncio.create_task(fetch(session, url)) for url in img_url_list]
        done, pending = await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(time.time()-start_time)