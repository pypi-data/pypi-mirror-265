import asyncio
import os

import aiohttp
from dotenv import load_dotenv

from methods import GetAnalyticsReport, GetUser, FindUsers

type ApiMethods = FindUsers | GetUser | GetAnalyticsReport

load_dotenv()


class NutshellCalls:
    """Class to handle multiple API calls to the Nutshell API"""
    URL = "https://app.nutshell.com/api/v1/json"

    def __init__(self, calls: list[ApiMethods] = None):
        self.auth = aiohttp.BasicAuth(os.getenv('USERNAME'), password=os.getenv('NUTSHELL_KEY'))
        self.calls = calls

    async def call_api(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for call in self.calls:
                tasks.append(self._fetch_report(session, call))
            return await asyncio.gather(*tasks)

    async def _fetch_report(self, session: aiohttp.ClientSession, call: ApiMethods) -> dict:
        payload = {"id": "apeye",
                   "jsonrpc": "2.0",
                   "method": call.api_method,
                   "params": call.params}
        async with session.post(self.URL, auth=self.auth, json=payload, ) as resp:
            info = await resp.json()
            return info
