#!/usr/bin/env python
# coding: utf-8

import asyncio
import aiohttp
from lxml import html
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor


index_urls = 'http://pic.netbian.com'


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
        text = await response.text(errors='ignore')
        tree = html.fromstring(text)
        for each in tree.xpath('//ul[@class="clearfix"]/li'):
            img_url = 'http://pic.netbian.com' + each.xpath('.//a//img/@src')[0]
            img_url_list.append(img_url)
    return img_url_list


async def main(index_url):
    async with aiohttp.ClientSession() as session:
        img_url_list = await get_img_url(session, index_url)
        tasks = [asyncio.create_task(fetch(session, url)) for url in img_url_list]
        done, pending = await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = time.time()
    index_url_list = ['http://pic.netbian.com'] + ['http://pic.netbian.com/index_{}.html'.format(i) for i in range(2,6)]
    for index_url in index_url_list:
        asyncio.run(main(index_url))
    print(time.time()-start_time)