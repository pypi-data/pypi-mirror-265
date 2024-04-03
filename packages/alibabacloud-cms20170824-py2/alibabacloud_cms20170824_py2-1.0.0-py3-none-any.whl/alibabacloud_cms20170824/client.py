# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import unicode_literals

from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_cms20170824 import models as cms_20170824_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(self, config):
        super(Client, self).__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('cms', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(self, product_id, region_id, endpoint_rule, network, suffix, endpoint_map, endpoint):
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def batch_create_once_task_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: BatchCreateOnceTaskRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: BatchCreateOnceTaskResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.task_list):
            body['taskList'] = request.task_list
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BatchCreateOnceTask',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.BatchCreateOnceTaskResponse(),
            self.call_api(params, req, runtime)
        )

    def batch_create_once_task(self, request):
        """
        @deprecated
        

        @param request: BatchCreateOnceTaskRequest

        @return: BatchCreateOnceTaskResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_create_once_task_with_options(request, runtime)

    def batch_delete_task_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: BatchDeleteTaskRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: BatchDeleteTaskResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.task_ids):
            query['taskIds'] = request.task_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BatchDeleteTask',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.BatchDeleteTaskResponse(),
            self.call_api(params, req, runtime)
        )

    def batch_delete_task(self, request):
        """
        @deprecated
        

        @param request: BatchDeleteTaskRequest

        @return: BatchDeleteTaskResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.batch_delete_task_with_options(request, runtime)

    def get_agent_all_city_avail_rate_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: GetAgentAllCityAvailRateRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: GetAgentAllCityAvailRateResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetAgentAllCityAvailRate',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.GetAgentAllCityAvailRateResponse(),
            self.call_api(params, req, runtime)
        )

    def get_agent_all_city_avail_rate(self, request):
        """
        @deprecated
        

        @param request: GetAgentAllCityAvailRateRequest

        @return: GetAgentAllCityAvailRateResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.get_agent_all_city_avail_rate_with_options(request, runtime)

    def get_agent_all_city_trend_with_options(self, request, runtime):
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetAgentAllCityTrend',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.GetAgentAllCityTrendResponse(),
            self.call_api(params, req, runtime)
        )

    def get_agent_all_city_trend(self, request):
        runtime = util_models.RuntimeOptions()
        return self.get_agent_all_city_trend_with_options(request, runtime)

    def get_isparea_city_with_options(self, runtime):
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='GetISPAreaCity',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.GetISPAreaCityResponse(),
            self.call_api(params, req, runtime)
        )

    def get_isparea_city(self):
        runtime = util_models.RuntimeOptions()
        return self.get_isparea_city_with_options(runtime)

    def list_metric_meta_with_options(self, request, runtime):
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListMetricMeta',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.ListMetricMetaResponse(),
            self.call_api(params, req, runtime)
        )

    def list_metric_meta(self, request):
        runtime = util_models.RuntimeOptions()
        return self.list_metric_meta_with_options(request, runtime)

    def pause_tasks_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: PauseTasksRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: PauseTasksResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.task_ids):
            query['taskIds'] = request.task_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PauseTasks',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.PauseTasksResponse(),
            self.call_api(params, req, runtime)
        )

    def pause_tasks(self, request):
        """
        @deprecated
        

        @param request: PauseTasksRequest

        @return: PauseTasksResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.pause_tasks_with_options(request, runtime)

    def query_task_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: QueryTaskRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: QueryTaskResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = OpenApiUtilClient.query(UtilClient.to_map(request))
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTask',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='GET',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.QueryTaskResponse(),
            self.call_api(params, req, runtime)
        )

    def query_task(self, request):
        """
        @deprecated
        

        @param request: QueryTaskRequest

        @return: QueryTaskResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.query_task_with_options(request, runtime)

    def start_tasks_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: StartTasksRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: StartTasksResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.task_ids):
            query['taskIds'] = request.task_ids
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartTasks',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.StartTasksResponse(),
            self.call_api(params, req, runtime)
        )

    def start_tasks(self, request):
        """
        @deprecated
        

        @param request: StartTasksRequest

        @return: StartTasksResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.start_tasks_with_options(request, runtime)

    def update_task_with_options(self, request, runtime):
        """
        @deprecated
        

        @param request: UpdateTaskRequest

        @param runtime: runtime options for this request RuntimeOptions

        @return: UpdateTaskResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.address):
            query['address'] = request.address
        if not UtilClient.is_unset(request.agent_group):
            query['agentGroup'] = request.agent_group
        if not UtilClient.is_unset(request.agent_type):
            query['agentType'] = request.agent_type
        if not UtilClient.is_unset(request.alert_info):
            query['alertInfo'] = request.alert_info
        if not UtilClient.is_unset(request.alert_name):
            query['alertName'] = request.alert_name
        if not UtilClient.is_unset(request.client_ids):
            query['clientIds'] = request.client_ids
        if not UtilClient.is_unset(request.end_time):
            query['endTime'] = request.end_time
        if not UtilClient.is_unset(request.interval):
            query['interval'] = request.interval
        if not UtilClient.is_unset(request.interval_unit):
            query['intervalUnit'] = request.interval_unit
        if not UtilClient.is_unset(request.ip):
            query['ip'] = request.ip
        if not UtilClient.is_unset(request.isp_city):
            query['ispCity'] = request.isp_city
        if not UtilClient.is_unset(request.options):
            query['options'] = request.options
        if not UtilClient.is_unset(request.report_project):
            query['reportProject'] = request.report_project
        if not UtilClient.is_unset(request.task_id):
            query['taskId'] = request.task_id
        if not UtilClient.is_unset(request.task_name):
            query['taskName'] = request.task_name
        if not UtilClient.is_unset(request.task_state):
            query['taskState'] = request.task_state
        if not UtilClient.is_unset(request.task_type):
            query['taskType'] = request.task_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateTask',
            version='2017-08-24',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            cms_20170824_models.UpdateTaskResponse(),
            self.call_api(params, req, runtime)
        )

    def update_task(self, request):
        """
        @deprecated
        

        @param request: UpdateTaskRequest

        @return: UpdateTaskResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.update_task_with_options(request, runtime)
