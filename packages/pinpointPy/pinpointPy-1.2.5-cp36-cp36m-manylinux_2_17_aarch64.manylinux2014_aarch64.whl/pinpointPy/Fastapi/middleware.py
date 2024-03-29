#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------------------------
#  Copyright  2020. NAVER Corp.                                                -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#   http://www.apache.org/licenses/LICENSE-2.0                                 -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pinpointPy.Fastapi.FastAPIRequestPlugin import FastAPIRequestPlugin


class PinPointMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        plugin = FastAPIRequestPlugin("")
        traceId, _, _ = plugin.onBefore(0, request)
        response = await call_next(request)
        plugin.onEnd(traceId, response)
        return response
