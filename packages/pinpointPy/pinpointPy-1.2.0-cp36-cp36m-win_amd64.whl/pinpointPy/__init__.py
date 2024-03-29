# ******************************************************************************
#   Copyright  2020. NAVER Corp.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ******************************************************************************

# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by eeliu at 2/4/21

from pinpointPy.libs import monkey_patch_for_pinpoint
from pinpointPy.pinpoint import set_agent, app_id, app_name, gen_tid, get_logger
from pinpointPy.TraceContext import set_trace_context, thread_local_context
from pinpointPy.Common import PinTransaction, GenPinHeader, PinHeader


def use_thread_local_context():
    get_logger().debug("use_thread_local_context")
    set_trace_context(thread_local_context())


__all__ = ['monkey_patch_for_pinpoint', 'use_thread_local_context'
           'set_agent', 'app_id', 'app_name', 'gen_tid', 'get_logger', 'PinTransaction', 'GenPinHeader', 'PinHeader']
__version__ = "1.1.0"
__author__ = 'liu.mingyi@navercorp.com'
