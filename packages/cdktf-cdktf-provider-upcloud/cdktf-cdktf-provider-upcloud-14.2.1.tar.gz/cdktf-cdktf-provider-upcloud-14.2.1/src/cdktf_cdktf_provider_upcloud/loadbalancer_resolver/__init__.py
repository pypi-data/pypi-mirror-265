'''
# `upcloud_loadbalancer_resolver`

Refer to the Terraform Registry for docs: [`upcloud_loadbalancer_resolver`](https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class LoadbalancerResolver(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.loadbalancerResolver.LoadbalancerResolver",
):
    '''Represents a {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver upcloud_loadbalancer_resolver}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cache_invalid: jsii.Number,
        cache_valid: jsii.Number,
        loadbalancer: builtins.str,
        name: builtins.str,
        nameservers: typing.Sequence[builtins.str],
        retries: jsii.Number,
        timeout: jsii.Number,
        timeout_retry: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver upcloud_loadbalancer_resolver} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cache_invalid: Time in seconds to cache invalid results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_invalid LoadbalancerResolver#cache_invalid}
        :param cache_valid: Time in seconds to cache valid results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_valid LoadbalancerResolver#cache_valid}
        :param loadbalancer: ID of the load balancer to which the resolver is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#loadbalancer LoadbalancerResolver#loadbalancer}
        :param name: The name of the resolver must be unique within the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#name LoadbalancerResolver#name}
        :param nameservers: List of nameserver IP addresses. Nameserver can reside in public internet or in customer private network. Port is optional, if missing then default 53 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#nameservers LoadbalancerResolver#nameservers}
        :param retries: Number of retries on failure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#retries LoadbalancerResolver#retries}
        :param timeout: Timeout for the query in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout LoadbalancerResolver#timeout}
        :param timeout_retry: Timeout for the query retries in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout_retry LoadbalancerResolver#timeout_retry}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#id LoadbalancerResolver#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a811cc75f16b5c9b55d7f8145f9615fb0e5168fb449c714ebefb32a8826e5cc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoadbalancerResolverConfig(
            cache_invalid=cache_invalid,
            cache_valid=cache_valid,
            loadbalancer=loadbalancer,
            name=name,
            nameservers=nameservers,
            retries=retries,
            timeout=timeout,
            timeout_retry=timeout_retry,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a LoadbalancerResolver resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LoadbalancerResolver to import.
        :param import_from_id: The id of the existing LoadbalancerResolver that should be imported. Refer to the {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LoadbalancerResolver to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b648b7a934f38b595d3bde5d234db47a840cbb5704b0368a8448b5394af74a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="cacheInvalidInput")
    def cache_invalid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cacheInvalidInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheValidInput")
    def cache_valid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cacheValidInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerInput")
    def loadbalancer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameserversInput")
    def nameservers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameserversInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutRetryInput")
    def timeout_retry_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutRetryInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheInvalid")
    def cache_invalid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cacheInvalid"))

    @cache_invalid.setter
    def cache_invalid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b041650f2ad1cea86ce9a6170c9ffdb4b90a9e40e1a2f5e6b34991e3a0dea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheInvalid", value)

    @builtins.property
    @jsii.member(jsii_name="cacheValid")
    def cache_valid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cacheValid"))

    @cache_valid.setter
    def cache_valid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7476731dff9995e1f459ada9be6af4a2c38d305f075c617f307b5fc225a25aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheValid", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81314ff44b3e740103c6facadca5b715e01299f28863f63e370fda1febffbd61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancer"))

    @loadbalancer.setter
    def loadbalancer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b254bca963e2c51cffb7da0def772a8e94968fac0d74f1331cf15afe90d75421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancer", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d76818e9c87fbe9837fc279948c11d638c58d11cae0f655f8953445addf9a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nameservers")
    def nameservers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nameservers"))

    @nameservers.setter
    def nameservers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28777585256e4cb148737602cf55dbf8205409b1b1724e2ce9d07a5662231e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameservers", value)

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8ed424a15e3003baafec3fac82b95f2f803890af7571a66f3efb622ae6d375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8918ee1ad2aa74e9e13e0da2225a6894392e47d0c7cc77282bb85ec47fb58fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutRetry")
    def timeout_retry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutRetry"))

    @timeout_retry.setter
    def timeout_retry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f760e66b87d709f8d20b3b8629736cac46f0942155d2f47aee824000a3e10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutRetry", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.loadbalancerResolver.LoadbalancerResolverConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cache_invalid": "cacheInvalid",
        "cache_valid": "cacheValid",
        "loadbalancer": "loadbalancer",
        "name": "name",
        "nameservers": "nameservers",
        "retries": "retries",
        "timeout": "timeout",
        "timeout_retry": "timeoutRetry",
        "id": "id",
    },
)
class LoadbalancerResolverConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_invalid: jsii.Number,
        cache_valid: jsii.Number,
        loadbalancer: builtins.str,
        name: builtins.str,
        nameservers: typing.Sequence[builtins.str],
        retries: jsii.Number,
        timeout: jsii.Number,
        timeout_retry: jsii.Number,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cache_invalid: Time in seconds to cache invalid results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_invalid LoadbalancerResolver#cache_invalid}
        :param cache_valid: Time in seconds to cache valid results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_valid LoadbalancerResolver#cache_valid}
        :param loadbalancer: ID of the load balancer to which the resolver is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#loadbalancer LoadbalancerResolver#loadbalancer}
        :param name: The name of the resolver must be unique within the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#name LoadbalancerResolver#name}
        :param nameservers: List of nameserver IP addresses. Nameserver can reside in public internet or in customer private network. Port is optional, if missing then default 53 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#nameservers LoadbalancerResolver#nameservers}
        :param retries: Number of retries on failure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#retries LoadbalancerResolver#retries}
        :param timeout: Timeout for the query in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout LoadbalancerResolver#timeout}
        :param timeout_retry: Timeout for the query retries in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout_retry LoadbalancerResolver#timeout_retry}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#id LoadbalancerResolver#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1ce39c3bb47be078508ac4c8b9127bc9a888ba10274c8c4519b23b6acf5058)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cache_invalid", value=cache_invalid, expected_type=type_hints["cache_invalid"])
            check_type(argname="argument cache_valid", value=cache_valid, expected_type=type_hints["cache_valid"])
            check_type(argname="argument loadbalancer", value=loadbalancer, expected_type=type_hints["loadbalancer"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nameservers", value=nameservers, expected_type=type_hints["nameservers"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeout_retry", value=timeout_retry, expected_type=type_hints["timeout_retry"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_invalid": cache_invalid,
            "cache_valid": cache_valid,
            "loadbalancer": loadbalancer,
            "name": name,
            "nameservers": nameservers,
            "retries": retries,
            "timeout": timeout,
            "timeout_retry": timeout_retry,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cache_invalid(self) -> jsii.Number:
        '''Time in seconds to cache invalid results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_invalid LoadbalancerResolver#cache_invalid}
        '''
        result = self._values.get("cache_invalid")
        assert result is not None, "Required property 'cache_invalid' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cache_valid(self) -> jsii.Number:
        '''Time in seconds to cache valid results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#cache_valid LoadbalancerResolver#cache_valid}
        '''
        result = self._values.get("cache_valid")
        assert result is not None, "Required property 'cache_valid' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def loadbalancer(self) -> builtins.str:
        '''ID of the load balancer to which the resolver is connected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#loadbalancer LoadbalancerResolver#loadbalancer}
        '''
        result = self._values.get("loadbalancer")
        assert result is not None, "Required property 'loadbalancer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the resolver must be unique within the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#name LoadbalancerResolver#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nameservers(self) -> typing.List[builtins.str]:
        '''List of nameserver IP addresses.

        Nameserver can reside in public internet or in customer private network.
        Port is optional, if missing then default 53 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#nameservers LoadbalancerResolver#nameservers}
        '''
        result = self._values.get("nameservers")
        assert result is not None, "Required property 'nameservers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def retries(self) -> jsii.Number:
        '''Number of retries on failure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#retries LoadbalancerResolver#retries}
        '''
        result = self._values.get("retries")
        assert result is not None, "Required property 'retries' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timeout(self) -> jsii.Number:
        '''Timeout for the query in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout LoadbalancerResolver#timeout}
        '''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timeout_retry(self) -> jsii.Number:
        '''Timeout for the query retries in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#timeout_retry LoadbalancerResolver#timeout_retry}
        '''
        result = self._values.get("timeout_retry")
        assert result is not None, "Required property 'timeout_retry' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/5.2.1/docs/resources/loadbalancer_resolver#id LoadbalancerResolver#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadbalancerResolverConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LoadbalancerResolver",
    "LoadbalancerResolverConfig",
]

publication.publish()

def _typecheckingstub__a811cc75f16b5c9b55d7f8145f9615fb0e5168fb449c714ebefb32a8826e5cc8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cache_invalid: jsii.Number,
    cache_valid: jsii.Number,
    loadbalancer: builtins.str,
    name: builtins.str,
    nameservers: typing.Sequence[builtins.str],
    retries: jsii.Number,
    timeout: jsii.Number,
    timeout_retry: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b648b7a934f38b595d3bde5d234db47a840cbb5704b0368a8448b5394af74a1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b041650f2ad1cea86ce9a6170c9ffdb4b90a9e40e1a2f5e6b34991e3a0dea9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7476731dff9995e1f459ada9be6af4a2c38d305f075c617f307b5fc225a25aa4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81314ff44b3e740103c6facadca5b715e01299f28863f63e370fda1febffbd61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b254bca963e2c51cffb7da0def772a8e94968fac0d74f1331cf15afe90d75421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d76818e9c87fbe9837fc279948c11d638c58d11cae0f655f8953445addf9a7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28777585256e4cb148737602cf55dbf8205409b1b1724e2ce9d07a5662231e38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8ed424a15e3003baafec3fac82b95f2f803890af7571a66f3efb622ae6d375(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8918ee1ad2aa74e9e13e0da2225a6894392e47d0c7cc77282bb85ec47fb58fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f760e66b87d709f8d20b3b8629736cac46f0942155d2f47aee824000a3e10c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1ce39c3bb47be078508ac4c8b9127bc9a888ba10274c8c4519b23b6acf5058(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_invalid: jsii.Number,
    cache_valid: jsii.Number,
    loadbalancer: builtins.str,
    name: builtins.str,
    nameservers: typing.Sequence[builtins.str],
    retries: jsii.Number,
    timeout: jsii.Number,
    timeout_retry: jsii.Number,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
