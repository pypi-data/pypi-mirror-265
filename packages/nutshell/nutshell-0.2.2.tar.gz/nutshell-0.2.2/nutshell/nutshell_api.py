import asyncio
import os
from typing import Sequence

import aiohttp
from dotenv import load_dotenv

from methods import GetAnalyticsReport, GetUser, FindUsers, APIMethod
from responses import FindUsersResult, GetUserResult, GetAnalyticsReportResult, FindTeamsResult, FindActivityTypesResult

type ApiMethods = FindUsers | GetUser | GetAnalyticsReport
type ApiResults = FindUsersResult | GetUserResult | GetAnalyticsReportResult

load_dotenv()


class NutshellAPI:
    """Class to handle multiple API calls to the Nutshell API"""
    URL = "https://app.nutshell.com/api/v1/json"

    def __init__(self, calls: APIMethod | Sequence[APIMethod]):
        self.auth = aiohttp.BasicAuth(os.getenv('NUTSHELL_USERNAME'), password=os.getenv('NUTSHELL_KEY'))
        if isinstance(calls, APIMethod):
            self.calls = (calls,)
        else:
            self.calls = calls

    async def call_api(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for call in self.calls:
                tasks.append(self._fetch_report(session, call))
            responses = await asyncio.gather(*tasks)

            return self._map_results(responses)

    async def _fetch_report(self, session: aiohttp.ClientSession, call: APIMethod) -> dict:
        payload = {"id": "apeye",
                   "jsonrpc": "2.0",
                   "method": call.api_method,
                   "params": call.params}
        async with session.post(self.URL, auth=self.auth, json=payload, ) as resp:
            info = await resp.json()
            return info

    def _map_results(self, results: list[dict]) -> list[tuple[APIMethod, ApiResults]]:
        call_response = []
        for idx, call in enumerate(self.calls):
            match call.api_method:
                case "findUsers":
                    call_response.append((call, FindUsersResult(**results[idx])))
                case "getUser":
                    call_response.append((call, GetUserResult(**results[idx])))
                case "findTeams":
                    call_response.append((call, FindTeamsResult(**results[idx])))
                case "findActivityTypes":
                    call_response.append((call, FindActivityTypesResult(**results[idx])))
                case "getAnalyticsReport":
                    call_response.append((call, GetAnalyticsReportResult(**results[idx])))

        return call_response
