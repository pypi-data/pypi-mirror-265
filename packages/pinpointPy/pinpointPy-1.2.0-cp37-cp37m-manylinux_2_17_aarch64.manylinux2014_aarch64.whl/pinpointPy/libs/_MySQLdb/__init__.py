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
from pinpointPy.Interceptor import Interceptor, intercept_once
from pinpointPy import get_logger


@intercept_once
def monkey_patch():
    try:
        from MySQLdb.connections import Connection
        from MySQLdb.cursors import BaseCursor
        from .MySQLdbPlugin import MySQLdbPlugin
        from .BaseCursorPlugins import BaseCursorPlugins

        Interceptors = [
            Interceptor(Connection, 'query', MySQLdbPlugin),
            Interceptor(BaseCursor, 'execute', BaseCursorPlugins)
        ]
        for interceptor in Interceptors:
            interceptor.enable()

    except ImportError as e:
        get_logger().debug(f'exception at {e}')


__all__ = ['monkey_patch']
__version__ = '0.0.3'
__author__ = 'liu.mingyi@navercorp.com'
