# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_cms20150420 import models as cms_20150420_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('cms', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def describe_metric_datum_with_options(
        self,
        request: cms_20150420_models.DescribeMetricDatumRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cms_20150420_models.DescribeMetricDatumResponse:
        """
        @deprecated
        
        @param request: DescribeMetricDatumRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeMetricDatumResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dimensions):
            query['Dimensions'] = request.dimensions
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.metric_name):
            query['MetricName'] = request.metric_name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.statistics):
            query['Statistics'] = request.statistics
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeMetricDatum',
            version='2015-04-20',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20150420_models.DescribeMetricDatumResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_metric_datum_with_options_async(
        self,
        request: cms_20150420_models.DescribeMetricDatumRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cms_20150420_models.DescribeMetricDatumResponse:
        """
        @deprecated
        
        @param request: DescribeMetricDatumRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeMetricDatumResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dimensions):
            query['Dimensions'] = request.dimensions
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.metric_name):
            query['MetricName'] = request.metric_name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.statistics):
            query['Statistics'] = request.statistics
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeMetricDatum',
            version='2015-04-20',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20150420_models.DescribeMetricDatumResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_metric_datum(
        self,
        request: cms_20150420_models.DescribeMetricDatumRequest,
    ) -> cms_20150420_models.DescribeMetricDatumResponse:
        """
        @deprecated
        
        @param request: DescribeMetricDatumRequest
        @return: DescribeMetricDatumResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_metric_datum_with_options(request, runtime)

    async def describe_metric_datum_async(
        self,
        request: cms_20150420_models.DescribeMetricDatumRequest,
    ) -> cms_20150420_models.DescribeMetricDatumResponse:
        """
        @deprecated
        
        @param request: DescribeMetricDatumRequest
        @return: DescribeMetricDatumResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_metric_datum_with_options_async(request, runtime)
