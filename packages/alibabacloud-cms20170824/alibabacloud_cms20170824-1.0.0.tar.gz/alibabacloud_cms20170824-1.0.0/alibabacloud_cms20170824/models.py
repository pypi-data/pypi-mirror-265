# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict


class BatchCreateOnceTaskRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        task_list: str = None,
    ):
        self.region_id = region_id
        self.task_list = task_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.task_list is not None:
            result['taskList'] = self.task_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('taskList') is not None:
            self.task_list = m.get('taskList')
        return self


class BatchCreateOnceTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        message: str = None,
        request_id: str = None,
        success: str = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class BatchCreateOnceTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: BatchCreateOnceTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BatchCreateOnceTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BatchDeleteTaskRequest(TeaModel):
    def __init__(
        self,
        task_ids: str = None,
    ):
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_ids is not None:
            result['taskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('taskIds') is not None:
            self.task_ids = m.get('taskIds')
        return self


class BatchDeleteTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class BatchDeleteTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: BatchDeleteTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BatchDeleteTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAgentAllCityAvailRateRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
        task_ids: str = None,
        task_type: str = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.task_ids = task_ids
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.task_ids is not None:
            result['taskIds'] = self.task_ids
        if self.task_type is not None:
            result['taskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('taskIds') is not None:
            self.task_ids = m.get('taskIds')
        if m.get('taskType') is not None:
            self.task_type = m.get('taskType')
        return self


class GetAgentAllCityAvailRateResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        detail: str = None,
        msg: str = None,
    ):
        self.code = code
        self.data = data
        self.detail = detail
        self.msg = msg

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.data is not None:
            result['data'] = self.data
        if self.detail is not None:
            result['detail'] = self.detail
        if self.msg is not None:
            result['msg'] = self.msg
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('detail') is not None:
            self.detail = m.get('detail')
        if m.get('msg') is not None:
            self.msg = m.get('msg')
        return self


class GetAgentAllCityAvailRateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAgentAllCityAvailRateResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAgentAllCityAvailRateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAgentAllCityTrendRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
        task_ids: str = None,
        task_type: str = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.task_ids = task_ids
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.task_ids is not None:
            result['taskIds'] = self.task_ids
        if self.task_type is not None:
            result['taskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('taskIds') is not None:
            self.task_ids = m.get('taskIds')
        if m.get('taskType') is not None:
            self.task_type = m.get('taskType')
        return self


class GetAgentAllCityTrendResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        detail: str = None,
        msg: str = None,
    ):
        self.code = code
        self.data = data
        self.detail = detail
        self.msg = msg

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.data is not None:
            result['data'] = self.data
        if self.detail is not None:
            result['detail'] = self.detail
        if self.msg is not None:
            result['msg'] = self.msg
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('detail') is not None:
            self.detail = m.get('detail')
        if m.get('msg') is not None:
            self.msg = m.get('msg')
        return self


class GetAgentAllCityTrendResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAgentAllCityTrendResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAgentAllCityTrendResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetISPAreaCityResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class GetISPAreaCityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetISPAreaCityResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetISPAreaCityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListMetricMetaRequest(TeaModel):
    def __init__(
        self,
        metric: str = None,
        page: str = None,
        page_size: str = None,
        project: str = None,
    ):
        self.metric = metric
        self.page = page
        self.page_size = page_size
        self.project = project

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.metric is not None:
            result['Metric'] = self.metric
        if self.page is not None:
            result['Page'] = self.page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.project is not None:
            result['Project'] = self.project
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Metric') is not None:
            self.metric = m.get('Metric')
        if m.get('Page') is not None:
            self.page = m.get('Page')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Project') is not None:
            self.project = m.get('Project')
        return self


class ListMetricMetaResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        message: str = None,
        request_id: str = None,
        success: str = None,
        total: str = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class ListMetricMetaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListMetricMetaResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListMetricMetaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PauseTasksRequest(TeaModel):
    def __init__(
        self,
        task_ids: str = None,
    ):
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_ids is not None:
            result['taskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('taskIds') is not None:
            self.task_ids = m.get('taskIds')
        return self


class PauseTasksResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class PauseTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PauseTasksResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PauseTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class QueryTaskRequest(TeaModel):
    def __init__(
        self,
        page: int = None,
        page_size: int = None,
        keyword: str = None,
        task_id: str = None,
        task_type: str = None,
    ):
        self.page = page
        self.page_size = page_size
        self.keyword = keyword
        self.task_id = task_id
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page is not None:
            result['Page'] = self.page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.keyword is not None:
            result['keyword'] = self.keyword
        if self.task_id is not None:
            result['taskId'] = self.task_id
        if self.task_type is not None:
            result['taskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Page') is not None:
            self.page = m.get('Page')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('keyword') is not None:
            self.keyword = m.get('keyword')
        if m.get('taskId') is not None:
            self.task_id = m.get('taskId')
        if m.get('taskType') is not None:
            self.task_type = m.get('taskType')
        return self


class QueryTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        page_info: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.page_info = page_info
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.page_info is not None:
            result['PageInfo'] = self.page_info
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('PageInfo') is not None:
            self.page_info = m.get('PageInfo')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class QueryTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: QueryTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = QueryTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartTasksRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        task_ids: str = None,
    ):
        self.region_id = region_id
        self.task_ids = task_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.task_ids is not None:
            result['taskIds'] = self.task_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('taskIds') is not None:
            self.task_ids = m.get('taskIds')
        return self


class StartTasksResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class StartTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartTasksResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTaskRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        address: str = None,
        agent_group: str = None,
        agent_type: str = None,
        alert_info: str = None,
        alert_name: str = None,
        client_ids: str = None,
        end_time: str = None,
        interval: str = None,
        interval_unit: str = None,
        ip: str = None,
        isp_city: str = None,
        options: str = None,
        report_project: str = None,
        task_id: str = None,
        task_name: str = None,
        task_state: str = None,
        task_type: str = None,
    ):
        self.region_id = region_id
        self.address = address
        self.agent_group = agent_group
        self.agent_type = agent_type
        self.alert_info = alert_info
        self.alert_name = alert_name
        self.client_ids = client_ids
        self.end_time = end_time
        self.interval = interval
        self.interval_unit = interval_unit
        self.ip = ip
        self.isp_city = isp_city
        self.options = options
        self.report_project = report_project
        self.task_id = task_id
        self.task_name = task_name
        self.task_state = task_state
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.address is not None:
            result['address'] = self.address
        if self.agent_group is not None:
            result['agentGroup'] = self.agent_group
        if self.agent_type is not None:
            result['agentType'] = self.agent_type
        if self.alert_info is not None:
            result['alertInfo'] = self.alert_info
        if self.alert_name is not None:
            result['alertName'] = self.alert_name
        if self.client_ids is not None:
            result['clientIds'] = self.client_ids
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.interval is not None:
            result['interval'] = self.interval
        if self.interval_unit is not None:
            result['intervalUnit'] = self.interval_unit
        if self.ip is not None:
            result['ip'] = self.ip
        if self.isp_city is not None:
            result['ispCity'] = self.isp_city
        if self.options is not None:
            result['options'] = self.options
        if self.report_project is not None:
            result['reportProject'] = self.report_project
        if self.task_id is not None:
            result['taskId'] = self.task_id
        if self.task_name is not None:
            result['taskName'] = self.task_name
        if self.task_state is not None:
            result['taskState'] = self.task_state
        if self.task_type is not None:
            result['taskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('address') is not None:
            self.address = m.get('address')
        if m.get('agentGroup') is not None:
            self.agent_group = m.get('agentGroup')
        if m.get('agentType') is not None:
            self.agent_type = m.get('agentType')
        if m.get('alertInfo') is not None:
            self.alert_info = m.get('alertInfo')
        if m.get('alertName') is not None:
            self.alert_name = m.get('alertName')
        if m.get('clientIds') is not None:
            self.client_ids = m.get('clientIds')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('interval') is not None:
            self.interval = m.get('interval')
        if m.get('intervalUnit') is not None:
            self.interval_unit = m.get('intervalUnit')
        if m.get('ip') is not None:
            self.ip = m.get('ip')
        if m.get('ispCity') is not None:
            self.isp_city = m.get('ispCity')
        if m.get('options') is not None:
            self.options = m.get('options')
        if m.get('reportProject') is not None:
            self.report_project = m.get('reportProject')
        if m.get('taskId') is not None:
            self.task_id = m.get('taskId')
        if m.get('taskName') is not None:
            self.task_name = m.get('taskName')
        if m.get('taskState') is not None:
            self.task_state = m.get('taskState')
        if m.get('taskType') is not None:
            self.task_type = m.get('taskType')
        return self


class UpdateTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        data: str = None,
        request_id: str = None,
        success: str = None,
        message: str = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success
        self.message = message

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('message') is not None:
            self.message = m.get('message')
        return self


class UpdateTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


