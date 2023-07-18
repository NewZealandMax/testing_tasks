from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

import aiohttp
import asyncio


async def logs(cont, name):
    conn = aiohttp.UnixConnector(path='/var/run/docker.sock')
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f'http://xx/containers/{cont}/logs?follow=1&stdout=1') as resp:
            async for line in resp.content:
                print(name, line)


class LogsMock(AsyncMock):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, url='http://xx/containers/container/logs?follow=1&stdout=1'):
        return LogsMock()


class LogsTestCase(TestCase):

    @patch('aiohttp.ClientSession')
    @patch('aiohttp.UnixConnector')
    def test_logs(self, mock_connector, mock_session):
        cont = 'container'
        name = 'name'
        mock_session.return_value.__aenter__.return_value = LogsMock()

        asyncio.run(logs(cont, name))

        mock_connector.assert_called_once_with(path='/var/run/docker.sock')
        mock_session.assert_called_once_with(connector=mock_connector.return_value)


if __name__ == '__main__':
    main()
