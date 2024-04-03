# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel


class DescribeMetricDatumRequest(TeaModel):
    def __init__(self, dimensions=None, end_time=None, group_name=None, length=None, metric_name=None,
                 namespace=None, next_token=None, period=None, start_time=None, statistics=None):
        self.dimensions = dimensions  # type: str
        self.end_time = end_time  # type: str
        self.group_name = group_name  # type: str
        self.length = length  # type: int
        self.metric_name = metric_name  # type: str
        self.namespace = namespace  # type: str
        self.next_token = next_token  # type: str
        self.period = period  # type: str
        self.start_time = start_time  # type: str
        self.statistics = statistics  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeMetricDatumRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dimensions is not None:
            result['Dimensions'] = self.dimensions
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.length is not None:
            result['Length'] = self.length
        if self.metric_name is not None:
            result['MetricName'] = self.metric_name
        if self.namespace is not None:
            result['Namespace'] = self.namespace
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.period is not None:
            result['Period'] = self.period
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.statistics is not None:
            result['Statistics'] = self.statistics
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Dimensions') is not None:
            self.dimensions = m.get('Dimensions')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('Length') is not None:
            self.length = m.get('Length')
        if m.get('MetricName') is not None:
            self.metric_name = m.get('MetricName')
        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Statistics') is not None:
            self.statistics = m.get('Statistics')
        return self


class DescribeMetricDatumResponseBodyDatapoints(TeaModel):
    def __init__(self, datapoint=None):
        self.datapoint = datapoint  # type: list[str]

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeMetricDatumResponseBodyDatapoints, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.datapoint is not None:
            result['Datapoint'] = self.datapoint
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Datapoint') is not None:
            self.datapoint = m.get('Datapoint')
        return self


class DescribeMetricDatumResponseBody(TeaModel):
    def __init__(self, code=None, datapoints=None, message=None, next_token=None):
        self.code = code  # type: str
        self.datapoints = datapoints  # type: DescribeMetricDatumResponseBodyDatapoints
        self.message = message  # type: str
        self.next_token = next_token  # type: str

    def validate(self):
        if self.datapoints:
            self.datapoints.validate()

    def to_map(self):
        _map = super(DescribeMetricDatumResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.datapoints is not None:
            result['Datapoints'] = self.datapoints.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Datapoints') is not None:
            temp_model = DescribeMetricDatumResponseBodyDatapoints()
            self.datapoints = temp_model.from_map(m['Datapoints'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        return self


class DescribeMetricDatumResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeMetricDatumResponseBody

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeMetricDatumResponse, self).to_map()
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

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeMetricDatumResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


