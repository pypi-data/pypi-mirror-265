# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_hitsdb20200615 import models as hitsdb_20200615_models
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
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('hitsdb', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

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

    def create_ldps_compute_group_with_options(
        self,
        request: hitsdb_20200615_models.CreateLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLdpsComputeGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_ldps_compute_group_with_options_async(
        self,
        request: hitsdb_20200615_models.CreateLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLdpsComputeGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_ldps_compute_group(
        self,
        request: hitsdb_20200615_models.CreateLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.CreateLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_ldps_compute_group_with_options(request, runtime)

    async def create_ldps_compute_group_async(
        self,
        request: hitsdb_20200615_models.CreateLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.CreateLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_ldps_compute_group_with_options_async(request, runtime)

    def create_ldps_namespace_with_options(
        self,
        request: hitsdb_20200615_models.CreateLdpsNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLdpsNamespaceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLdpsNamespace',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLdpsNamespaceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_ldps_namespace_with_options_async(
        self,
        request: hitsdb_20200615_models.CreateLdpsNamespaceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLdpsNamespaceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLdpsNamespace',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLdpsNamespaceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_ldps_namespace(
        self,
        request: hitsdb_20200615_models.CreateLdpsNamespaceRequest,
    ) -> hitsdb_20200615_models.CreateLdpsNamespaceResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_ldps_namespace_with_options(request, runtime)

    async def create_ldps_namespace_async(
        self,
        request: hitsdb_20200615_models.CreateLdpsNamespaceRequest,
    ) -> hitsdb_20200615_models.CreateLdpsNamespaceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_ldps_namespace_with_options_async(request, runtime)

    def create_lindorm_instance_with_options(
        self,
        request: hitsdb_20200615_models.CreateLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLindormInstanceResponse:
        """
        You must select at least one engine when you create a Lindorm instance. For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine types](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: CreateLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arbiter_vswitch_id):
            query['ArbiterVSwitchId'] = request.arbiter_vswitch_id
        if not UtilClient.is_unset(request.arbiter_zone_id):
            query['ArbiterZoneId'] = request.arbiter_zone_id
        if not UtilClient.is_unset(request.arch_version):
            query['ArchVersion'] = request.arch_version
        if not UtilClient.is_unset(request.auto_renew_duration):
            query['AutoRenewDuration'] = request.auto_renew_duration
        if not UtilClient.is_unset(request.auto_renewal):
            query['AutoRenewal'] = request.auto_renewal
        if not UtilClient.is_unset(request.cold_storage):
            query['ColdStorage'] = request.cold_storage
        if not UtilClient.is_unset(request.core_single_storage):
            query['CoreSingleStorage'] = request.core_single_storage
        if not UtilClient.is_unset(request.core_spec):
            query['CoreSpec'] = request.core_spec
        if not UtilClient.is_unset(request.disk_category):
            query['DiskCategory'] = request.disk_category
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.filestore_num):
            query['FilestoreNum'] = request.filestore_num
        if not UtilClient.is_unset(request.filestore_spec):
            query['FilestoreSpec'] = request.filestore_spec
        if not UtilClient.is_unset(request.instance_alias):
            query['InstanceAlias'] = request.instance_alias
        if not UtilClient.is_unset(request.instance_storage):
            query['InstanceStorage'] = request.instance_storage
        if not UtilClient.is_unset(request.lindorm_num):
            query['LindormNum'] = request.lindorm_num
        if not UtilClient.is_unset(request.lindorm_spec):
            query['LindormSpec'] = request.lindorm_spec
        if not UtilClient.is_unset(request.log_disk_category):
            query['LogDiskCategory'] = request.log_disk_category
        if not UtilClient.is_unset(request.log_num):
            query['LogNum'] = request.log_num
        if not UtilClient.is_unset(request.log_single_storage):
            query['LogSingleStorage'] = request.log_single_storage
        if not UtilClient.is_unset(request.log_spec):
            query['LogSpec'] = request.log_spec
        if not UtilClient.is_unset(request.multi_zone_combination):
            query['MultiZoneCombination'] = request.multi_zone_combination
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.primary_vswitch_id):
            query['PrimaryVSwitchId'] = request.primary_vswitch_id
        if not UtilClient.is_unset(request.primary_zone_id):
            query['PrimaryZoneId'] = request.primary_zone_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.solr_num):
            query['SolrNum'] = request.solr_num
        if not UtilClient.is_unset(request.solr_spec):
            query['SolrSpec'] = request.solr_spec
        if not UtilClient.is_unset(request.standby_vswitch_id):
            query['StandbyVSwitchId'] = request.standby_vswitch_id
        if not UtilClient.is_unset(request.standby_zone_id):
            query['StandbyZoneId'] = request.standby_zone_id
        if not UtilClient.is_unset(request.stream_num):
            query['StreamNum'] = request.stream_num
        if not UtilClient.is_unset(request.stream_spec):
            query['StreamSpec'] = request.stream_spec
        if not UtilClient.is_unset(request.tsdb_num):
            query['TsdbNum'] = request.tsdb_num
        if not UtilClient.is_unset(request.tsdb_spec):
            query['TsdbSpec'] = request.tsdb_spec
        if not UtilClient.is_unset(request.vpcid):
            query['VPCId'] = request.vpcid
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLindormInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_lindorm_instance_with_options_async(
        self,
        request: hitsdb_20200615_models.CreateLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.CreateLindormInstanceResponse:
        """
        You must select at least one engine when you create a Lindorm instance. For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine types](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: CreateLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arbiter_vswitch_id):
            query['ArbiterVSwitchId'] = request.arbiter_vswitch_id
        if not UtilClient.is_unset(request.arbiter_zone_id):
            query['ArbiterZoneId'] = request.arbiter_zone_id
        if not UtilClient.is_unset(request.arch_version):
            query['ArchVersion'] = request.arch_version
        if not UtilClient.is_unset(request.auto_renew_duration):
            query['AutoRenewDuration'] = request.auto_renew_duration
        if not UtilClient.is_unset(request.auto_renewal):
            query['AutoRenewal'] = request.auto_renewal
        if not UtilClient.is_unset(request.cold_storage):
            query['ColdStorage'] = request.cold_storage
        if not UtilClient.is_unset(request.core_single_storage):
            query['CoreSingleStorage'] = request.core_single_storage
        if not UtilClient.is_unset(request.core_spec):
            query['CoreSpec'] = request.core_spec
        if not UtilClient.is_unset(request.disk_category):
            query['DiskCategory'] = request.disk_category
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.filestore_num):
            query['FilestoreNum'] = request.filestore_num
        if not UtilClient.is_unset(request.filestore_spec):
            query['FilestoreSpec'] = request.filestore_spec
        if not UtilClient.is_unset(request.instance_alias):
            query['InstanceAlias'] = request.instance_alias
        if not UtilClient.is_unset(request.instance_storage):
            query['InstanceStorage'] = request.instance_storage
        if not UtilClient.is_unset(request.lindorm_num):
            query['LindormNum'] = request.lindorm_num
        if not UtilClient.is_unset(request.lindorm_spec):
            query['LindormSpec'] = request.lindorm_spec
        if not UtilClient.is_unset(request.log_disk_category):
            query['LogDiskCategory'] = request.log_disk_category
        if not UtilClient.is_unset(request.log_num):
            query['LogNum'] = request.log_num
        if not UtilClient.is_unset(request.log_single_storage):
            query['LogSingleStorage'] = request.log_single_storage
        if not UtilClient.is_unset(request.log_spec):
            query['LogSpec'] = request.log_spec
        if not UtilClient.is_unset(request.multi_zone_combination):
            query['MultiZoneCombination'] = request.multi_zone_combination
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.primary_vswitch_id):
            query['PrimaryVSwitchId'] = request.primary_vswitch_id
        if not UtilClient.is_unset(request.primary_zone_id):
            query['PrimaryZoneId'] = request.primary_zone_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.solr_num):
            query['SolrNum'] = request.solr_num
        if not UtilClient.is_unset(request.solr_spec):
            query['SolrSpec'] = request.solr_spec
        if not UtilClient.is_unset(request.standby_vswitch_id):
            query['StandbyVSwitchId'] = request.standby_vswitch_id
        if not UtilClient.is_unset(request.standby_zone_id):
            query['StandbyZoneId'] = request.standby_zone_id
        if not UtilClient.is_unset(request.stream_num):
            query['StreamNum'] = request.stream_num
        if not UtilClient.is_unset(request.stream_spec):
            query['StreamSpec'] = request.stream_spec
        if not UtilClient.is_unset(request.tsdb_num):
            query['TsdbNum'] = request.tsdb_num
        if not UtilClient.is_unset(request.tsdb_spec):
            query['TsdbSpec'] = request.tsdb_spec
        if not UtilClient.is_unset(request.vpcid):
            query['VPCId'] = request.vpcid
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.CreateLindormInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_lindorm_instance(
        self,
        request: hitsdb_20200615_models.CreateLindormInstanceRequest,
    ) -> hitsdb_20200615_models.CreateLindormInstanceResponse:
        """
        You must select at least one engine when you create a Lindorm instance. For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine types](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: CreateLindormInstanceRequest
        @return: CreateLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_lindorm_instance_with_options(request, runtime)

    async def create_lindorm_instance_async(
        self,
        request: hitsdb_20200615_models.CreateLindormInstanceRequest,
    ) -> hitsdb_20200615_models.CreateLindormInstanceResponse:
        """
        You must select at least one engine when you create a Lindorm instance. For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine types](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: CreateLindormInstanceRequest
        @return: CreateLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_lindorm_instance_with_options_async(request, runtime)

    def delete_ldps_compute_group_with_options(
        self,
        request: hitsdb_20200615_models.DeleteLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.DeleteLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.DeleteLdpsComputeGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_ldps_compute_group_with_options_async(
        self,
        request: hitsdb_20200615_models.DeleteLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.DeleteLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.DeleteLdpsComputeGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_ldps_compute_group(
        self,
        request: hitsdb_20200615_models.DeleteLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.DeleteLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_ldps_compute_group_with_options(request, runtime)

    async def delete_ldps_compute_group_async(
        self,
        request: hitsdb_20200615_models.DeleteLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.DeleteLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_ldps_compute_group_with_options_async(request, runtime)

    def describe_regions_with_options(
        self,
        request: hitsdb_20200615_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accept_language):
            query['AcceptLanguage'] = request.accept_language
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeRegions',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.DescribeRegionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_regions_with_options_async(
        self,
        request: hitsdb_20200615_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.accept_language):
            query['AcceptLanguage'] = request.accept_language
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeRegions',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.DescribeRegionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_regions(
        self,
        request: hitsdb_20200615_models.DescribeRegionsRequest,
    ) -> hitsdb_20200615_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_regions_with_options(request, runtime)

    async def describe_regions_async(
        self,
        request: hitsdb_20200615_models.DescribeRegionsRequest,
    ) -> hitsdb_20200615_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_regions_with_options_async(request, runtime)

    def get_client_source_ip_with_options(
        self,
        request: hitsdb_20200615_models.GetClientSourceIpRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetClientSourceIpResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientSourceIp',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetClientSourceIpResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_client_source_ip_with_options_async(
        self,
        request: hitsdb_20200615_models.GetClientSourceIpRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetClientSourceIpResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetClientSourceIp',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetClientSourceIpResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_client_source_ip(
        self,
        request: hitsdb_20200615_models.GetClientSourceIpRequest,
    ) -> hitsdb_20200615_models.GetClientSourceIpResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_client_source_ip_with_options(request, runtime)

    async def get_client_source_ip_async(
        self,
        request: hitsdb_20200615_models.GetClientSourceIpRequest,
    ) -> hitsdb_20200615_models.GetClientSourceIpResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_client_source_ip_with_options_async(request, runtime)

    def get_engine_default_auth_with_options(
        self,
        request: hitsdb_20200615_models.GetEngineDefaultAuthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetEngineDefaultAuthResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEngineDefaultAuth',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetEngineDefaultAuthResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_engine_default_auth_with_options_async(
        self,
        request: hitsdb_20200615_models.GetEngineDefaultAuthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetEngineDefaultAuthResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetEngineDefaultAuth',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetEngineDefaultAuthResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_engine_default_auth(
        self,
        request: hitsdb_20200615_models.GetEngineDefaultAuthRequest,
    ) -> hitsdb_20200615_models.GetEngineDefaultAuthResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_engine_default_auth_with_options(request, runtime)

    async def get_engine_default_auth_async(
        self,
        request: hitsdb_20200615_models.GetEngineDefaultAuthRequest,
    ) -> hitsdb_20200615_models.GetEngineDefaultAuthResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_engine_default_auth_with_options_async(request, runtime)

    def get_instance_ip_white_list_with_options(
        self,
        request: hitsdb_20200615_models.GetInstanceIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetInstanceIpWhiteListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceIpWhiteList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetInstanceIpWhiteListResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_ip_white_list_with_options_async(
        self,
        request: hitsdb_20200615_models.GetInstanceIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetInstanceIpWhiteListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceIpWhiteList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetInstanceIpWhiteListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance_ip_white_list(
        self,
        request: hitsdb_20200615_models.GetInstanceIpWhiteListRequest,
    ) -> hitsdb_20200615_models.GetInstanceIpWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_instance_ip_white_list_with_options(request, runtime)

    async def get_instance_ip_white_list_async(
        self,
        request: hitsdb_20200615_models.GetInstanceIpWhiteListRequest,
    ) -> hitsdb_20200615_models.GetInstanceIpWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_instance_ip_white_list_with_options_async(request, runtime)

    def get_instance_security_groups_with_options(
        self,
        request: hitsdb_20200615_models.GetInstanceSecurityGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetInstanceSecurityGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceSecurityGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetInstanceSecurityGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_instance_security_groups_with_options_async(
        self,
        request: hitsdb_20200615_models.GetInstanceSecurityGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetInstanceSecurityGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetInstanceSecurityGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetInstanceSecurityGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_instance_security_groups(
        self,
        request: hitsdb_20200615_models.GetInstanceSecurityGroupsRequest,
    ) -> hitsdb_20200615_models.GetInstanceSecurityGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_instance_security_groups_with_options(request, runtime)

    async def get_instance_security_groups_async(
        self,
        request: hitsdb_20200615_models.GetInstanceSecurityGroupsRequest,
    ) -> hitsdb_20200615_models.GetInstanceSecurityGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_instance_security_groups_with_options_async(request, runtime)

    def get_ldps_compute_group_with_options(
        self,
        request: hitsdb_20200615_models.GetLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsComputeGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_ldps_compute_group_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsComputeGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_ldps_compute_group(
        self,
        request: hitsdb_20200615_models.GetLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.GetLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_ldps_compute_group_with_options(request, runtime)

    async def get_ldps_compute_group_async(
        self,
        request: hitsdb_20200615_models.GetLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.GetLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_ldps_compute_group_with_options_async(request, runtime)

    def get_ldps_namespaced_quota_with_options(
        self,
        request: hitsdb_20200615_models.GetLdpsNamespacedQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsNamespacedQuota',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_ldps_namespaced_quota_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLdpsNamespacedQuotaRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsNamespacedQuota',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_ldps_namespaced_quota(
        self,
        request: hitsdb_20200615_models.GetLdpsNamespacedQuotaRequest,
    ) -> hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_ldps_namespaced_quota_with_options(request, runtime)

    async def get_ldps_namespaced_quota_async(
        self,
        request: hitsdb_20200615_models.GetLdpsNamespacedQuotaRequest,
    ) -> hitsdb_20200615_models.GetLdpsNamespacedQuotaResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_ldps_namespaced_quota_with_options_async(request, runtime)

    def get_ldps_resource_cost_with_options(
        self,
        request: hitsdb_20200615_models.GetLdpsResourceCostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsResourceCostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsResourceCost',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsResourceCostResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_ldps_resource_cost_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLdpsResourceCostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLdpsResourceCostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLdpsResourceCost',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLdpsResourceCostResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_ldps_resource_cost(
        self,
        request: hitsdb_20200615_models.GetLdpsResourceCostRequest,
    ) -> hitsdb_20200615_models.GetLdpsResourceCostResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_ldps_resource_cost_with_options(request, runtime)

    async def get_ldps_resource_cost_async(
        self,
        request: hitsdb_20200615_models.GetLdpsResourceCostRequest,
    ) -> hitsdb_20200615_models.GetLdpsResourceCostResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_ldps_resource_cost_with_options_async(request, runtime)

    def get_lindorm_instance_with_options(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_lindorm_instance_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_lindorm_instance(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_lindorm_instance_with_options(request, runtime)

    async def get_lindorm_instance_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_lindorm_instance_with_options_async(request, runtime)

    def get_lindorm_instance_engine_list_with_options(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceEngineListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceEngineListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstanceEngineList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceEngineListResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_lindorm_instance_engine_list_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceEngineListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceEngineListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstanceEngineList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceEngineListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_lindorm_instance_engine_list(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceEngineListRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceEngineListResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_lindorm_instance_engine_list_with_options(request, runtime)

    async def get_lindorm_instance_engine_list_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceEngineListRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceEngineListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_lindorm_instance_engine_list_with_options_async(request, runtime)

    def get_lindorm_instance_list_with_options(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.query_str):
            query['QueryStr'] = request.query_str
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.service_type):
            query['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.support_engine):
            query['SupportEngine'] = request.support_engine
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstanceList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceListResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_lindorm_instance_list_with_options_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.GetLindormInstanceListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.query_str):
            query['QueryStr'] = request.query_str
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.service_type):
            query['ServiceType'] = request.service_type
        if not UtilClient.is_unset(request.support_engine):
            query['SupportEngine'] = request.support_engine
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetLindormInstanceList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.GetLindormInstanceListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_lindorm_instance_list(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceListRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceListResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_lindorm_instance_list_with_options(request, runtime)

    async def get_lindorm_instance_list_async(
        self,
        request: hitsdb_20200615_models.GetLindormInstanceListRequest,
    ) -> hitsdb_20200615_models.GetLindormInstanceListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_lindorm_instance_list_with_options_async(request, runtime)

    def list_ldps_compute_groups_with_options(
        self,
        request: hitsdb_20200615_models.ListLdpsComputeGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ListLdpsComputeGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLdpsComputeGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ListLdpsComputeGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_ldps_compute_groups_with_options_async(
        self,
        request: hitsdb_20200615_models.ListLdpsComputeGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ListLdpsComputeGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListLdpsComputeGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ListLdpsComputeGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_ldps_compute_groups(
        self,
        request: hitsdb_20200615_models.ListLdpsComputeGroupsRequest,
    ) -> hitsdb_20200615_models.ListLdpsComputeGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_ldps_compute_groups_with_options(request, runtime)

    async def list_ldps_compute_groups_async(
        self,
        request: hitsdb_20200615_models.ListLdpsComputeGroupsRequest,
    ) -> hitsdb_20200615_models.ListLdpsComputeGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_ldps_compute_groups_with_options_async(request, runtime)

    def list_tag_resources_with_options(
        self,
        request: hitsdb_20200615_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ListTagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_tag_resources_with_options_async(
        self,
        request: hitsdb_20200615_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ListTagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_tag_resources(
        self,
        request: hitsdb_20200615_models.ListTagResourcesRequest,
    ) -> hitsdb_20200615_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_tag_resources_with_options(request, runtime)

    async def list_tag_resources_async(
        self,
        request: hitsdb_20200615_models.ListTagResourcesRequest,
    ) -> hitsdb_20200615_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_tag_resources_with_options_async(request, runtime)

    def modify_instance_pay_type_with_options(
        self,
        request: hitsdb_20200615_models.ModifyInstancePayTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ModifyInstancePayTypeResponse:
        """
        You can call this operation to change the billing method of an instance to subscription or pay-as-you-go.
        Before you call this operation, make sure that you fully understand the billing methods and [pricing](https://www.aliyun.com/price/product?spm=openapi-amp.newDocPublishment.0.0.6345281fu63xJ3#/hitsdb/detail/hitsdb_lindormpre_public_cn) of Lindorm.
        
        @param request: ModifyInstancePayTypeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyInstancePayTypeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyInstancePayType',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ModifyInstancePayTypeResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_instance_pay_type_with_options_async(
        self,
        request: hitsdb_20200615_models.ModifyInstancePayTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ModifyInstancePayTypeResponse:
        """
        You can call this operation to change the billing method of an instance to subscription or pay-as-you-go.
        Before you call this operation, make sure that you fully understand the billing methods and [pricing](https://www.aliyun.com/price/product?spm=openapi-amp.newDocPublishment.0.0.6345281fu63xJ3#/hitsdb/detail/hitsdb_lindormpre_public_cn) of Lindorm.
        
        @param request: ModifyInstancePayTypeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyInstancePayTypeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyInstancePayType',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ModifyInstancePayTypeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_instance_pay_type(
        self,
        request: hitsdb_20200615_models.ModifyInstancePayTypeRequest,
    ) -> hitsdb_20200615_models.ModifyInstancePayTypeResponse:
        """
        You can call this operation to change the billing method of an instance to subscription or pay-as-you-go.
        Before you call this operation, make sure that you fully understand the billing methods and [pricing](https://www.aliyun.com/price/product?spm=openapi-amp.newDocPublishment.0.0.6345281fu63xJ3#/hitsdb/detail/hitsdb_lindormpre_public_cn) of Lindorm.
        
        @param request: ModifyInstancePayTypeRequest
        @return: ModifyInstancePayTypeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.modify_instance_pay_type_with_options(request, runtime)

    async def modify_instance_pay_type_async(
        self,
        request: hitsdb_20200615_models.ModifyInstancePayTypeRequest,
    ) -> hitsdb_20200615_models.ModifyInstancePayTypeResponse:
        """
        You can call this operation to change the billing method of an instance to subscription or pay-as-you-go.
        Before you call this operation, make sure that you fully understand the billing methods and [pricing](https://www.aliyun.com/price/product?spm=openapi-amp.newDocPublishment.0.0.6345281fu63xJ3#/hitsdb/detail/hitsdb_lindormpre_public_cn) of Lindorm.
        
        @param request: ModifyInstancePayTypeRequest
        @return: ModifyInstancePayTypeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.modify_instance_pay_type_with_options_async(request, runtime)

    def open_compute_engine_with_options(
        self,
        request: hitsdb_20200615_models.OpenComputeEngineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.OpenComputeEngineResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cpu_limit):
            query['CpuLimit'] = request.cpu_limit
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.memory_limit):
            query['MemoryLimit'] = request.memory_limit
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='OpenComputeEngine',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.OpenComputeEngineResponse(),
            self.call_api(params, req, runtime)
        )

    async def open_compute_engine_with_options_async(
        self,
        request: hitsdb_20200615_models.OpenComputeEngineRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.OpenComputeEngineResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cpu_limit):
            query['CpuLimit'] = request.cpu_limit
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.memory_limit):
            query['MemoryLimit'] = request.memory_limit
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='OpenComputeEngine',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.OpenComputeEngineResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def open_compute_engine(
        self,
        request: hitsdb_20200615_models.OpenComputeEngineRequest,
    ) -> hitsdb_20200615_models.OpenComputeEngineResponse:
        runtime = util_models.RuntimeOptions()
        return self.open_compute_engine_with_options(request, runtime)

    async def open_compute_engine_async(
        self,
        request: hitsdb_20200615_models.OpenComputeEngineRequest,
    ) -> hitsdb_20200615_models.OpenComputeEngineResponse:
        runtime = util_models.RuntimeOptions()
        return await self.open_compute_engine_with_options_async(request, runtime)

    def open_compute_pre_check_with_options(
        self,
        request: hitsdb_20200615_models.OpenComputePreCheckRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.OpenComputePreCheckResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cpu_limit):
            query['CpuLimit'] = request.cpu_limit
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.memory_limit):
            query['MemoryLimit'] = request.memory_limit
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='OpenComputePreCheck',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.OpenComputePreCheckResponse(),
            self.call_api(params, req, runtime)
        )

    async def open_compute_pre_check_with_options_async(
        self,
        request: hitsdb_20200615_models.OpenComputePreCheckRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.OpenComputePreCheckResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cpu_limit):
            query['CpuLimit'] = request.cpu_limit
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.memory_limit):
            query['MemoryLimit'] = request.memory_limit
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='OpenComputePreCheck',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.OpenComputePreCheckResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def open_compute_pre_check(
        self,
        request: hitsdb_20200615_models.OpenComputePreCheckRequest,
    ) -> hitsdb_20200615_models.OpenComputePreCheckResponse:
        runtime = util_models.RuntimeOptions()
        return self.open_compute_pre_check_with_options(request, runtime)

    async def open_compute_pre_check_async(
        self,
        request: hitsdb_20200615_models.OpenComputePreCheckRequest,
    ) -> hitsdb_20200615_models.OpenComputePreCheckResponse:
        runtime = util_models.RuntimeOptions()
        return await self.open_compute_pre_check_with_options_async(request, runtime)

    def release_lindorm_instance_with_options(
        self,
        request: hitsdb_20200615_models.ReleaseLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ReleaseLindormInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.immediately):
            query['Immediately'] = request.immediately
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ReleaseLindormInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def release_lindorm_instance_with_options_async(
        self,
        request: hitsdb_20200615_models.ReleaseLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.ReleaseLindormInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.immediately):
            query['Immediately'] = request.immediately
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.ReleaseLindormInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def release_lindorm_instance(
        self,
        request: hitsdb_20200615_models.ReleaseLindormInstanceRequest,
    ) -> hitsdb_20200615_models.ReleaseLindormInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.release_lindorm_instance_with_options(request, runtime)

    async def release_lindorm_instance_async(
        self,
        request: hitsdb_20200615_models.ReleaseLindormInstanceRequest,
    ) -> hitsdb_20200615_models.ReleaseLindormInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.release_lindorm_instance_with_options_async(request, runtime)

    def renew_lindorm_instance_with_options(
        self,
        request: hitsdb_20200615_models.RenewLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.RenewLindormInstanceResponse:
        """
        You can call this operation to renew a subscription Lindorm instance for 1 to 9 months or 1 to 3 years.
        Before you call this operation, make sure that you fully understand the billing methods and pricing of Lindorm.
        
        @param request: RenewLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RenewLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RenewLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.RenewLindormInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def renew_lindorm_instance_with_options_async(
        self,
        request: hitsdb_20200615_models.RenewLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.RenewLindormInstanceResponse:
        """
        You can call this operation to renew a subscription Lindorm instance for 1 to 9 months or 1 to 3 years.
        Before you call this operation, make sure that you fully understand the billing methods and pricing of Lindorm.
        
        @param request: RenewLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RenewLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.duration):
            query['Duration'] = request.duration
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.pricing_cycle):
            query['PricingCycle'] = request.pricing_cycle
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RenewLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.RenewLindormInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def renew_lindorm_instance(
        self,
        request: hitsdb_20200615_models.RenewLindormInstanceRequest,
    ) -> hitsdb_20200615_models.RenewLindormInstanceResponse:
        """
        You can call this operation to renew a subscription Lindorm instance for 1 to 9 months or 1 to 3 years.
        Before you call this operation, make sure that you fully understand the billing methods and pricing of Lindorm.
        
        @param request: RenewLindormInstanceRequest
        @return: RenewLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.renew_lindorm_instance_with_options(request, runtime)

    async def renew_lindorm_instance_async(
        self,
        request: hitsdb_20200615_models.RenewLindormInstanceRequest,
    ) -> hitsdb_20200615_models.RenewLindormInstanceResponse:
        """
        You can call this operation to renew a subscription Lindorm instance for 1 to 9 months or 1 to 3 years.
        Before you call this operation, make sure that you fully understand the billing methods and pricing of Lindorm.
        
        @param request: RenewLindormInstanceRequest
        @return: RenewLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.renew_lindorm_instance_with_options_async(request, runtime)

    def restart_ldps_compute_group_with_options(
        self,
        request: hitsdb_20200615_models.RestartLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.RestartLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RestartLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.RestartLdpsComputeGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def restart_ldps_compute_group_with_options_async(
        self,
        request: hitsdb_20200615_models.RestartLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.RestartLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RestartLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.RestartLdpsComputeGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def restart_ldps_compute_group(
        self,
        request: hitsdb_20200615_models.RestartLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.RestartLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.restart_ldps_compute_group_with_options(request, runtime)

    async def restart_ldps_compute_group_async(
        self,
        request: hitsdb_20200615_models.RestartLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.RestartLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.restart_ldps_compute_group_with_options_async(request, runtime)

    def switch_lsqlv3my_sqlservice_with_options(
        self,
        request: hitsdb_20200615_models.SwitchLSQLV3MySQLServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse:
        """
        Prerequisites
        *   The LindormTable version of your instance is 2.6.0 or later.
        *   The LindormTable of your instance supports LindormSQL V3. The value of the EnableLsqlVersionV3 parameter in the response of the GetLindormInstance operation is true for Lindorm instances purchased after Oct 24, 2023, which indicates that LindormSQL is supported by these instances by default. If you want to enable LindormSQL for instances purchased before Oct 24, 2023, contact the on-duty technical support.
        You can enable the MySQL compatibility feature for a Lindorm instance only when the instance meets the preceding requirements.
        
        @param request: SwitchLSQLV3MySQLServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SwitchLSQLV3MySQLServiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_type):
            query['ActionType'] = request.action_type
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SwitchLSQLV3MySQLService',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def switch_lsqlv3my_sqlservice_with_options_async(
        self,
        request: hitsdb_20200615_models.SwitchLSQLV3MySQLServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse:
        """
        Prerequisites
        *   The LindormTable version of your instance is 2.6.0 or later.
        *   The LindormTable of your instance supports LindormSQL V3. The value of the EnableLsqlVersionV3 parameter in the response of the GetLindormInstance operation is true for Lindorm instances purchased after Oct 24, 2023, which indicates that LindormSQL is supported by these instances by default. If you want to enable LindormSQL for instances purchased before Oct 24, 2023, contact the on-duty technical support.
        You can enable the MySQL compatibility feature for a Lindorm instance only when the instance meets the preceding requirements.
        
        @param request: SwitchLSQLV3MySQLServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SwitchLSQLV3MySQLServiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_type):
            query['ActionType'] = request.action_type
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SwitchLSQLV3MySQLService',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def switch_lsqlv3my_sqlservice(
        self,
        request: hitsdb_20200615_models.SwitchLSQLV3MySQLServiceRequest,
    ) -> hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse:
        """
        Prerequisites
        *   The LindormTable version of your instance is 2.6.0 or later.
        *   The LindormTable of your instance supports LindormSQL V3. The value of the EnableLsqlVersionV3 parameter in the response of the GetLindormInstance operation is true for Lindorm instances purchased after Oct 24, 2023, which indicates that LindormSQL is supported by these instances by default. If you want to enable LindormSQL for instances purchased before Oct 24, 2023, contact the on-duty technical support.
        You can enable the MySQL compatibility feature for a Lindorm instance only when the instance meets the preceding requirements.
        
        @param request: SwitchLSQLV3MySQLServiceRequest
        @return: SwitchLSQLV3MySQLServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.switch_lsqlv3my_sqlservice_with_options(request, runtime)

    async def switch_lsqlv3my_sqlservice_async(
        self,
        request: hitsdb_20200615_models.SwitchLSQLV3MySQLServiceRequest,
    ) -> hitsdb_20200615_models.SwitchLSQLV3MySQLServiceResponse:
        """
        Prerequisites
        *   The LindormTable version of your instance is 2.6.0 or later.
        *   The LindormTable of your instance supports LindormSQL V3. The value of the EnableLsqlVersionV3 parameter in the response of the GetLindormInstance operation is true for Lindorm instances purchased after Oct 24, 2023, which indicates that LindormSQL is supported by these instances by default. If you want to enable LindormSQL for instances purchased before Oct 24, 2023, contact the on-duty technical support.
        You can enable the MySQL compatibility feature for a Lindorm instance only when the instance meets the preceding requirements.
        
        @param request: SwitchLSQLV3MySQLServiceRequest
        @return: SwitchLSQLV3MySQLServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.switch_lsqlv3my_sqlservice_with_options_async(request, runtime)

    def tag_resources_with_options(
        self,
        request: hitsdb_20200615_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.TagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def tag_resources_with_options_async(
        self,
        request: hitsdb_20200615_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.TagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def tag_resources(
        self,
        request: hitsdb_20200615_models.TagResourcesRequest,
    ) -> hitsdb_20200615_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.tag_resources_with_options(request, runtime)

    async def tag_resources_async(
        self,
        request: hitsdb_20200615_models.TagResourcesRequest,
    ) -> hitsdb_20200615_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.tag_resources_with_options_async(request, runtime)

    def untag_resources_with_options(
        self,
        request: hitsdb_20200615_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UntagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def untag_resources_with_options_async(
        self,
        request: hitsdb_20200615_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UntagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def untag_resources(
        self,
        request: hitsdb_20200615_models.UntagResourcesRequest,
    ) -> hitsdb_20200615_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.untag_resources_with_options(request, runtime)

    async def untag_resources_async(
        self,
        request: hitsdb_20200615_models.UntagResourcesRequest,
    ) -> hitsdb_20200615_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.untag_resources_with_options_async(request, runtime)

    def update_instance_ip_white_list_with_options(
        self,
        request: hitsdb_20200615_models.UpdateInstanceIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.delete):
            query['Delete'] = request.delete
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_ip_list):
            query['SecurityIpList'] = request.security_ip_list
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateInstanceIpWhiteList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_instance_ip_white_list_with_options_async(
        self,
        request: hitsdb_20200615_models.UpdateInstanceIpWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.delete):
            query['Delete'] = request.delete
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_ip_list):
            query['SecurityIpList'] = request.security_ip_list
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateInstanceIpWhiteList',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_instance_ip_white_list(
        self,
        request: hitsdb_20200615_models.UpdateInstanceIpWhiteListRequest,
    ) -> hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_instance_ip_white_list_with_options(request, runtime)

    async def update_instance_ip_white_list_async(
        self,
        request: hitsdb_20200615_models.UpdateInstanceIpWhiteListRequest,
    ) -> hitsdb_20200615_models.UpdateInstanceIpWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_instance_ip_white_list_with_options_async(request, runtime)

    def update_instance_security_groups_with_options(
        self,
        request: hitsdb_20200615_models.UpdateInstanceSecurityGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_groups):
            query['SecurityGroups'] = request.security_groups
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateInstanceSecurityGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_instance_security_groups_with_options_async(
        self,
        request: hitsdb_20200615_models.UpdateInstanceSecurityGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_groups):
            query['SecurityGroups'] = request.security_groups
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateInstanceSecurityGroups',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_instance_security_groups(
        self,
        request: hitsdb_20200615_models.UpdateInstanceSecurityGroupsRequest,
    ) -> hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_instance_security_groups_with_options(request, runtime)

    async def update_instance_security_groups_async(
        self,
        request: hitsdb_20200615_models.UpdateInstanceSecurityGroupsRequest,
    ) -> hitsdb_20200615_models.UpdateInstanceSecurityGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_instance_security_groups_with_options_async(request, runtime)

    def update_ldps_compute_group_with_options(
        self,
        request: hitsdb_20200615_models.UpdateLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateLdpsComputeGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def update_ldps_compute_group_with_options_async(
        self,
        request: hitsdb_20200615_models.UpdateLdpsComputeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpdateLdpsComputeGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.group_name):
            query['GroupName'] = request.group_name
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.properties):
            query['Properties'] = request.properties
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpdateLdpsComputeGroup',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpdateLdpsComputeGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def update_ldps_compute_group(
        self,
        request: hitsdb_20200615_models.UpdateLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.UpdateLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_ldps_compute_group_with_options(request, runtime)

    async def update_ldps_compute_group_async(
        self,
        request: hitsdb_20200615_models.UpdateLdpsComputeGroupRequest,
    ) -> hitsdb_20200615_models.UpdateLdpsComputeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_ldps_compute_group_with_options_async(request, runtime)

    def upgrade_lindorm_instance_with_options(
        self,
        request: hitsdb_20200615_models.UpgradeLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpgradeLindormInstanceResponse:
        """
        For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine typpes](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: UpgradeLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpgradeLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_storage):
            query['ClusterStorage'] = request.cluster_storage
        if not UtilClient.is_unset(request.cold_storage):
            query['ColdStorage'] = request.cold_storage
        if not UtilClient.is_unset(request.core_single_storage):
            query['CoreSingleStorage'] = request.core_single_storage
        if not UtilClient.is_unset(request.filestore_num):
            query['FilestoreNum'] = request.filestore_num
        if not UtilClient.is_unset(request.filestore_spec):
            query['FilestoreSpec'] = request.filestore_spec
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.lindorm_num):
            query['LindormNum'] = request.lindorm_num
        if not UtilClient.is_unset(request.lindorm_spec):
            query['LindormSpec'] = request.lindorm_spec
        if not UtilClient.is_unset(request.log_num):
            query['LogNum'] = request.log_num
        if not UtilClient.is_unset(request.log_single_storage):
            query['LogSingleStorage'] = request.log_single_storage
        if not UtilClient.is_unset(request.log_spec):
            query['LogSpec'] = request.log_spec
        if not UtilClient.is_unset(request.lts_core_num):
            query['LtsCoreNum'] = request.lts_core_num
        if not UtilClient.is_unset(request.lts_core_spec):
            query['LtsCoreSpec'] = request.lts_core_spec
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.solr_num):
            query['SolrNum'] = request.solr_num
        if not UtilClient.is_unset(request.solr_spec):
            query['SolrSpec'] = request.solr_spec
        if not UtilClient.is_unset(request.stream_num):
            query['StreamNum'] = request.stream_num
        if not UtilClient.is_unset(request.stream_spec):
            query['StreamSpec'] = request.stream_spec
        if not UtilClient.is_unset(request.tsdb_num):
            query['TsdbNum'] = request.tsdb_num
        if not UtilClient.is_unset(request.tsdb_spec):
            query['TsdbSpec'] = request.tsdb_spec
        if not UtilClient.is_unset(request.upgrade_type):
            query['UpgradeType'] = request.upgrade_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpgradeLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpgradeLindormInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def upgrade_lindorm_instance_with_options_async(
        self,
        request: hitsdb_20200615_models.UpgradeLindormInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> hitsdb_20200615_models.UpgradeLindormInstanceResponse:
        """
        For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine typpes](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: UpgradeLindormInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UpgradeLindormInstanceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_storage):
            query['ClusterStorage'] = request.cluster_storage
        if not UtilClient.is_unset(request.cold_storage):
            query['ColdStorage'] = request.cold_storage
        if not UtilClient.is_unset(request.core_single_storage):
            query['CoreSingleStorage'] = request.core_single_storage
        if not UtilClient.is_unset(request.filestore_num):
            query['FilestoreNum'] = request.filestore_num
        if not UtilClient.is_unset(request.filestore_spec):
            query['FilestoreSpec'] = request.filestore_spec
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.lindorm_num):
            query['LindormNum'] = request.lindorm_num
        if not UtilClient.is_unset(request.lindorm_spec):
            query['LindormSpec'] = request.lindorm_spec
        if not UtilClient.is_unset(request.log_num):
            query['LogNum'] = request.log_num
        if not UtilClient.is_unset(request.log_single_storage):
            query['LogSingleStorage'] = request.log_single_storage
        if not UtilClient.is_unset(request.log_spec):
            query['LogSpec'] = request.log_spec
        if not UtilClient.is_unset(request.lts_core_num):
            query['LtsCoreNum'] = request.lts_core_num
        if not UtilClient.is_unset(request.lts_core_spec):
            query['LtsCoreSpec'] = request.lts_core_spec
        if not UtilClient.is_unset(request.owner_account):
            query['OwnerAccount'] = request.owner_account
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_token):
            query['SecurityToken'] = request.security_token
        if not UtilClient.is_unset(request.solr_num):
            query['SolrNum'] = request.solr_num
        if not UtilClient.is_unset(request.solr_spec):
            query['SolrSpec'] = request.solr_spec
        if not UtilClient.is_unset(request.stream_num):
            query['StreamNum'] = request.stream_num
        if not UtilClient.is_unset(request.stream_spec):
            query['StreamSpec'] = request.stream_spec
        if not UtilClient.is_unset(request.tsdb_num):
            query['TsdbNum'] = request.tsdb_num
        if not UtilClient.is_unset(request.tsdb_spec):
            query['TsdbSpec'] = request.tsdb_spec
        if not UtilClient.is_unset(request.upgrade_type):
            query['UpgradeType'] = request.upgrade_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UpgradeLindormInstance',
            version='2020-06-15',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            hitsdb_20200615_models.UpgradeLindormInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def upgrade_lindorm_instance(
        self,
        request: hitsdb_20200615_models.UpgradeLindormInstanceRequest,
    ) -> hitsdb_20200615_models.UpgradeLindormInstanceResponse:
        """
        For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine typpes](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: UpgradeLindormInstanceRequest
        @return: UpgradeLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.upgrade_lindorm_instance_with_options(request, runtime)

    async def upgrade_lindorm_instance_async(
        self,
        request: hitsdb_20200615_models.UpgradeLindormInstanceRequest,
    ) -> hitsdb_20200615_models.UpgradeLindormInstanceResponse:
        """
        For more information about how to select the storage type and engine type when you create a Lindorm instance, see [Select engine typpes](~~181971~~) and [Select storage types](~~174643~~).
        
        @param request: UpgradeLindormInstanceRequest
        @return: UpgradeLindormInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.upgrade_lindorm_instance_with_options_async(request, runtime)
