'''
# paloaltonetworks-cloudngfw-ngfw

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `PaloAltoNetworks::CloudNGFW::NGFW` v2.0.0.

## Description

A Firewall resource offers Palo Alto Networks next-generation firewall capabilities with built-in resiliency, scalability, and life-cycle management.

## References

* [Source](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name PaloAltoNetworks::CloudNGFW::NGFW \
  --publisher-id 4e4cf7d0eb3aa7334767bc17a1dbec7e8279d078 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/4e4cf7d0eb3aa7334767bc17a1dbec7e8279d078/PaloAltoNetworks-CloudNGFW-NGFW \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `PaloAltoNetworks::CloudNGFW::NGFW`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fpaloaltonetworks-cloudngfw-ngfw+v2.0.0).
* Issues related to `PaloAltoNetworks::CloudNGFW::NGFW` should be reported to the [publisher](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git).

## License

Distributed under the Apache-2.0 License.
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.Attachment",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "endpoint_id": "endpointId",
        "rejected_reason": "rejectedReason",
        "status": "status",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
    },
)
class Attachment:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        rejected_reason: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: 
        :param endpoint_id: 
        :param rejected_reason: 
        :param status: 
        :param subnet_id: 
        :param vpc_id: 

        :schema: Attachment
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aca4af208c41c9d8df7e894754d8890bfe54f292782fb9ceef8fa21b942475)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument rejected_reason", value=rejected_reason, expected_type=type_hints["rejected_reason"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if endpoint_id is not None:
            self._values["endpoint_id"] = endpoint_id
        if rejected_reason is not None:
            self._values["rejected_reason"] = rejected_reason
        if status is not None:
            self._values["status"] = status
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#AccountId
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#EndpointId
        '''
        result = self._values.get("endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rejected_reason(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#RejectedReason
        '''
        result = self._values.get("rejected_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#Status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#SubnetId
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attachment#VpcId
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Attachment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnNgfw(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.CfnNgfw",
):
    '''A CloudFormation ``PaloAltoNetworks::CloudNGFW::NGFW``.

    :cloudformationResource: PaloAltoNetworks::CloudNGFW::NGFW
    :link: https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        firewall_name: builtins.str,
        app_id_version: typing.Optional[builtins.str] = None,
        associate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
        cloud_watch_metric_namespace: typing.Optional[builtins.str] = None,
        describe: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disassociate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_mode: typing.Optional["EndpointMode"] = None,
        global_rule_stack_name: typing.Optional[builtins.str] = None,
        link_id: typing.Optional[builtins.str] = None,
        log_destination_configs: typing.Optional[typing.Sequence[typing.Union["LogProfileConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        multi_vpc_enable: typing.Optional[builtins.bool] = None,
        read_firewall: typing.Optional[typing.Union["CfnNgfwPropsReadFirewall", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_name: typing.Optional[builtins.str] = None,
        subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``PaloAltoNetworks::CloudNGFW::NGFW``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_id: 
        :param firewall_name: 
        :param app_id_version: 
        :param associate_subnet_mappings: 
        :param automatic_upgrade_app_id_version: 
        :param cloud_watch_metric_namespace: 
        :param describe: 
        :param description: 
        :param disassociate_subnet_mappings: 
        :param endpoint_mode: 
        :param global_rule_stack_name: 
        :param link_id: 
        :param log_destination_configs: 
        :param multi_vpc_enable: 
        :param read_firewall: 
        :param rule_stack_name: 
        :param subnet_mappings: 
        :param tags: 
        :param vpc_id: 
        :param vpc_ids: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44e34122d63b2e649e1a0cf59f5d48094ce3838d16dfa68e3cc9200b395326e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNgfwProps(
            account_id=account_id,
            firewall_name=firewall_name,
            app_id_version=app_id_version,
            associate_subnet_mappings=associate_subnet_mappings,
            automatic_upgrade_app_id_version=automatic_upgrade_app_id_version,
            cloud_watch_metric_namespace=cloud_watch_metric_namespace,
            describe=describe,
            description=description,
            disassociate_subnet_mappings=disassociate_subnet_mappings,
            endpoint_mode=endpoint_mode,
            global_rule_stack_name=global_rule_stack_name,
            link_id=link_id,
            log_destination_configs=log_destination_configs,
            multi_vpc_enable=multi_vpc_enable,
            read_firewall=read_firewall,
            rule_stack_name=rule_stack_name,
            subnet_mappings=subnet_mappings,
            tags=tags,
            vpc_id=vpc_id,
            vpc_ids=vpc_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnNgfwProps":
        '''Resource props.'''
        return typing.cast("CfnNgfwProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.CfnNgfwProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "firewall_name": "firewallName",
        "app_id_version": "appIdVersion",
        "associate_subnet_mappings": "associateSubnetMappings",
        "automatic_upgrade_app_id_version": "automaticUpgradeAppIdVersion",
        "cloud_watch_metric_namespace": "cloudWatchMetricNamespace",
        "describe": "describe",
        "description": "description",
        "disassociate_subnet_mappings": "disassociateSubnetMappings",
        "endpoint_mode": "endpointMode",
        "global_rule_stack_name": "globalRuleStackName",
        "link_id": "linkId",
        "log_destination_configs": "logDestinationConfigs",
        "multi_vpc_enable": "multiVpcEnable",
        "read_firewall": "readFirewall",
        "rule_stack_name": "ruleStackName",
        "subnet_mappings": "subnetMappings",
        "tags": "tags",
        "vpc_id": "vpcId",
        "vpc_ids": "vpcIds",
    },
)
class CfnNgfwProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        firewall_name: builtins.str,
        app_id_version: typing.Optional[builtins.str] = None,
        associate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
        cloud_watch_metric_namespace: typing.Optional[builtins.str] = None,
        describe: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disassociate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_mode: typing.Optional["EndpointMode"] = None,
        global_rule_stack_name: typing.Optional[builtins.str] = None,
        link_id: typing.Optional[builtins.str] = None,
        log_destination_configs: typing.Optional[typing.Sequence[typing.Union["LogProfileConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        multi_vpc_enable: typing.Optional[builtins.bool] = None,
        read_firewall: typing.Optional[typing.Union["CfnNgfwPropsReadFirewall", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_name: typing.Optional[builtins.str] = None,
        subnet_mappings: typing.Optional[typing.Sequence[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''A Firewall resource offers Palo Alto Networks next-generation firewall capabilities with built-in resiliency, scalability, and life-cycle management.

        :param account_id: 
        :param firewall_name: 
        :param app_id_version: 
        :param associate_subnet_mappings: 
        :param automatic_upgrade_app_id_version: 
        :param cloud_watch_metric_namespace: 
        :param describe: 
        :param description: 
        :param disassociate_subnet_mappings: 
        :param endpoint_mode: 
        :param global_rule_stack_name: 
        :param link_id: 
        :param log_destination_configs: 
        :param multi_vpc_enable: 
        :param read_firewall: 
        :param rule_stack_name: 
        :param subnet_mappings: 
        :param tags: 
        :param vpc_id: 
        :param vpc_ids: 

        :schema: CfnNgfwProps
        '''
        if isinstance(read_firewall, dict):
            read_firewall = CfnNgfwPropsReadFirewall(**read_firewall)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babd383745f46351db16da77dd426a0238262cf070da922071ca55f3a80af00b)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument app_id_version", value=app_id_version, expected_type=type_hints["app_id_version"])
            check_type(argname="argument associate_subnet_mappings", value=associate_subnet_mappings, expected_type=type_hints["associate_subnet_mappings"])
            check_type(argname="argument automatic_upgrade_app_id_version", value=automatic_upgrade_app_id_version, expected_type=type_hints["automatic_upgrade_app_id_version"])
            check_type(argname="argument cloud_watch_metric_namespace", value=cloud_watch_metric_namespace, expected_type=type_hints["cloud_watch_metric_namespace"])
            check_type(argname="argument describe", value=describe, expected_type=type_hints["describe"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disassociate_subnet_mappings", value=disassociate_subnet_mappings, expected_type=type_hints["disassociate_subnet_mappings"])
            check_type(argname="argument endpoint_mode", value=endpoint_mode, expected_type=type_hints["endpoint_mode"])
            check_type(argname="argument global_rule_stack_name", value=global_rule_stack_name, expected_type=type_hints["global_rule_stack_name"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
            check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            check_type(argname="argument multi_vpc_enable", value=multi_vpc_enable, expected_type=type_hints["multi_vpc_enable"])
            check_type(argname="argument read_firewall", value=read_firewall, expected_type=type_hints["read_firewall"])
            check_type(argname="argument rule_stack_name", value=rule_stack_name, expected_type=type_hints["rule_stack_name"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument vpc_ids", value=vpc_ids, expected_type=type_hints["vpc_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "firewall_name": firewall_name,
        }
        if app_id_version is not None:
            self._values["app_id_version"] = app_id_version
        if associate_subnet_mappings is not None:
            self._values["associate_subnet_mappings"] = associate_subnet_mappings
        if automatic_upgrade_app_id_version is not None:
            self._values["automatic_upgrade_app_id_version"] = automatic_upgrade_app_id_version
        if cloud_watch_metric_namespace is not None:
            self._values["cloud_watch_metric_namespace"] = cloud_watch_metric_namespace
        if describe is not None:
            self._values["describe"] = describe
        if description is not None:
            self._values["description"] = description
        if disassociate_subnet_mappings is not None:
            self._values["disassociate_subnet_mappings"] = disassociate_subnet_mappings
        if endpoint_mode is not None:
            self._values["endpoint_mode"] = endpoint_mode
        if global_rule_stack_name is not None:
            self._values["global_rule_stack_name"] = global_rule_stack_name
        if link_id is not None:
            self._values["link_id"] = link_id
        if log_destination_configs is not None:
            self._values["log_destination_configs"] = log_destination_configs
        if multi_vpc_enable is not None:
            self._values["multi_vpc_enable"] = multi_vpc_enable
        if read_firewall is not None:
            self._values["read_firewall"] = read_firewall
        if rule_stack_name is not None:
            self._values["rule_stack_name"] = rule_stack_name
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if vpc_ids is not None:
            self._values["vpc_ids"] = vpc_ids

    @builtins.property
    def account_id(self) -> builtins.str:
        '''
        :schema: CfnNgfwProps#AccountId
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_name(self) -> builtins.str:
        '''
        :schema: CfnNgfwProps#FirewallName
        '''
        result = self._values.get("firewall_name")
        assert result is not None, "Required property 'firewall_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#AppIdVersion
        '''
        result = self._values.get("app_id_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def associate_subnet_mappings(
        self,
    ) -> typing.Optional[typing.List["SubnetMappings"]]:
        '''
        :schema: CfnNgfwProps#AssociateSubnetMappings
        '''
        result = self._values.get("associate_subnet_mappings")
        return typing.cast(typing.Optional[typing.List["SubnetMappings"]], result)

    @builtins.property
    def automatic_upgrade_app_id_version(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnNgfwProps#AutomaticUpgradeAppIdVersion
        '''
        result = self._values.get("automatic_upgrade_app_id_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cloud_watch_metric_namespace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#CloudWatchMetricNamespace
        '''
        result = self._values.get("cloud_watch_metric_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def describe(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnNgfwProps#Describe
        '''
        result = self._values.get("describe")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disassociate_subnet_mappings(
        self,
    ) -> typing.Optional[typing.List["SubnetMappings"]]:
        '''
        :schema: CfnNgfwProps#DisassociateSubnetMappings
        '''
        result = self._values.get("disassociate_subnet_mappings")
        return typing.cast(typing.Optional[typing.List["SubnetMappings"]], result)

    @builtins.property
    def endpoint_mode(self) -> typing.Optional["EndpointMode"]:
        '''
        :schema: CfnNgfwProps#EndpointMode
        '''
        result = self._values.get("endpoint_mode")
        return typing.cast(typing.Optional["EndpointMode"], result)

    @builtins.property
    def global_rule_stack_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#GlobalRuleStackName
        '''
        result = self._values.get("global_rule_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#LinkId
        '''
        result = self._values.get("link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_destination_configs(
        self,
    ) -> typing.Optional[typing.List["LogProfileConfig"]]:
        '''
        :schema: CfnNgfwProps#LogDestinationConfigs
        '''
        result = self._values.get("log_destination_configs")
        return typing.cast(typing.Optional[typing.List["LogProfileConfig"]], result)

    @builtins.property
    def multi_vpc_enable(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnNgfwProps#MultiVpcEnable
        '''
        result = self._values.get("multi_vpc_enable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_firewall(self) -> typing.Optional["CfnNgfwPropsReadFirewall"]:
        '''
        :schema: CfnNgfwProps#ReadFirewall
        '''
        result = self._values.get("read_firewall")
        return typing.cast(typing.Optional["CfnNgfwPropsReadFirewall"], result)

    @builtins.property
    def rule_stack_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#RuleStackName
        '''
        result = self._values.get("rule_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_mappings(self) -> typing.Optional[typing.List["SubnetMappings"]]:
        '''
        :schema: CfnNgfwProps#SubnetMappings
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional[typing.List["SubnetMappings"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnNgfwProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwProps#VpcId
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnNgfwProps#VPCIds
        '''
        result = self._values.get("vpc_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNgfwProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.CfnNgfwPropsReadFirewall",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "app_id_version": "appIdVersion",
        "attachments": "attachments",
        "automatic_upgrade_app_id_version": "automaticUpgradeAppIdVersion",
        "description": "description",
        "endpoint_mode": "endpointMode",
        "endpoint_service_name": "endpointServiceName",
        "failure_reason": "failureReason",
        "firewall_name": "firewallName",
        "firewall_status": "firewallStatus",
        "global_rule_stack_name": "globalRuleStackName",
        "link_id": "linkId",
        "link_status": "linkStatus",
        "multi_vpc_enable": "multiVpcEnable",
        "rule_stack_name": "ruleStackName",
        "rule_stack_status": "ruleStackStatus",
        "subnet_mappings": "subnetMappings",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnNgfwPropsReadFirewall:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        app_id_version: typing.Optional[builtins.str] = None,
        attachments: typing.Optional[typing.Sequence[typing.Union[Attachment, typing.Dict[builtins.str, typing.Any]]]] = None,
        automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        endpoint_mode: typing.Optional["EndpointMode"] = None,
        endpoint_service_name: typing.Optional[builtins.str] = None,
        failure_reason: typing.Optional[builtins.str] = None,
        firewall_name: typing.Optional[builtins.str] = None,
        firewall_status: typing.Optional[builtins.str] = None,
        global_rule_stack_name: typing.Optional[builtins.str] = None,
        link_id: typing.Optional[builtins.str] = None,
        link_status: typing.Optional[builtins.str] = None,
        multi_vpc_enable: typing.Optional[builtins.bool] = None,
        rule_stack_name: typing.Optional[builtins.str] = None,
        rule_stack_status: typing.Optional[builtins.str] = None,
        subnet_mappings: typing.Optional[typing.Union["SubnetMappings", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: 
        :param app_id_version: 
        :param attachments: 
        :param automatic_upgrade_app_id_version: 
        :param description: 
        :param endpoint_mode: 
        :param endpoint_service_name: 
        :param failure_reason: 
        :param firewall_name: 
        :param firewall_status: 
        :param global_rule_stack_name: 
        :param link_id: 
        :param link_status: 
        :param multi_vpc_enable: 
        :param rule_stack_name: 
        :param rule_stack_status: 
        :param subnet_mappings: 
        :param tags: 
        :param vpc_id: 

        :schema: CfnNgfwPropsReadFirewall
        '''
        if isinstance(subnet_mappings, dict):
            subnet_mappings = SubnetMappings(**subnet_mappings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce095556ca83beeaecfe83beae6caeda3c0798f9340949d37a095b246fc300a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument app_id_version", value=app_id_version, expected_type=type_hints["app_id_version"])
            check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
            check_type(argname="argument automatic_upgrade_app_id_version", value=automatic_upgrade_app_id_version, expected_type=type_hints["automatic_upgrade_app_id_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint_mode", value=endpoint_mode, expected_type=type_hints["endpoint_mode"])
            check_type(argname="argument endpoint_service_name", value=endpoint_service_name, expected_type=type_hints["endpoint_service_name"])
            check_type(argname="argument failure_reason", value=failure_reason, expected_type=type_hints["failure_reason"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_status", value=firewall_status, expected_type=type_hints["firewall_status"])
            check_type(argname="argument global_rule_stack_name", value=global_rule_stack_name, expected_type=type_hints["global_rule_stack_name"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
            check_type(argname="argument link_status", value=link_status, expected_type=type_hints["link_status"])
            check_type(argname="argument multi_vpc_enable", value=multi_vpc_enable, expected_type=type_hints["multi_vpc_enable"])
            check_type(argname="argument rule_stack_name", value=rule_stack_name, expected_type=type_hints["rule_stack_name"])
            check_type(argname="argument rule_stack_status", value=rule_stack_status, expected_type=type_hints["rule_stack_status"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if app_id_version is not None:
            self._values["app_id_version"] = app_id_version
        if attachments is not None:
            self._values["attachments"] = attachments
        if automatic_upgrade_app_id_version is not None:
            self._values["automatic_upgrade_app_id_version"] = automatic_upgrade_app_id_version
        if description is not None:
            self._values["description"] = description
        if endpoint_mode is not None:
            self._values["endpoint_mode"] = endpoint_mode
        if endpoint_service_name is not None:
            self._values["endpoint_service_name"] = endpoint_service_name
        if failure_reason is not None:
            self._values["failure_reason"] = failure_reason
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name
        if firewall_status is not None:
            self._values["firewall_status"] = firewall_status
        if global_rule_stack_name is not None:
            self._values["global_rule_stack_name"] = global_rule_stack_name
        if link_id is not None:
            self._values["link_id"] = link_id
        if link_status is not None:
            self._values["link_status"] = link_status
        if multi_vpc_enable is not None:
            self._values["multi_vpc_enable"] = multi_vpc_enable
        if rule_stack_name is not None:
            self._values["rule_stack_name"] = rule_stack_name
        if rule_stack_status is not None:
            self._values["rule_stack_status"] = rule_stack_status
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#AccountId
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_id_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#AppIdVersion
        '''
        result = self._values.get("app_id_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attachments(self) -> typing.Optional[typing.List[Attachment]]:
        '''
        :schema: CfnNgfwPropsReadFirewall#Attachments
        '''
        result = self._values.get("attachments")
        return typing.cast(typing.Optional[typing.List[Attachment]], result)

    @builtins.property
    def automatic_upgrade_app_id_version(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnNgfwPropsReadFirewall#AutomaticUpgradeAppIdVersion
        '''
        result = self._values.get("automatic_upgrade_app_id_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_mode(self) -> typing.Optional["EndpointMode"]:
        '''
        :schema: CfnNgfwPropsReadFirewall#EndpointMode
        '''
        result = self._values.get("endpoint_mode")
        return typing.cast(typing.Optional["EndpointMode"], result)

    @builtins.property
    def endpoint_service_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#EndpointServiceName
        '''
        result = self._values.get("endpoint_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_reason(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#FailureReason
        '''
        result = self._values.get("failure_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#FirewallName
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_status(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#FirewallStatus
        '''
        result = self._values.get("firewall_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_rule_stack_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#GlobalRuleStackName
        '''
        result = self._values.get("global_rule_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#LinkId
        '''
        result = self._values.get("link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_status(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#LinkStatus
        '''
        result = self._values.get("link_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_vpc_enable(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnNgfwPropsReadFirewall#MultiVpcEnable
        '''
        result = self._values.get("multi_vpc_enable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_stack_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#RuleStackName
        '''
        result = self._values.get("rule_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_stack_status(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#RuleStackStatus
        '''
        result = self._values.get("rule_stack_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_mappings(self) -> typing.Optional["SubnetMappings"]:
        '''
        :schema: CfnNgfwPropsReadFirewall#SubnetMappings
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional["SubnetMappings"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnNgfwPropsReadFirewall#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnNgfwPropsReadFirewall#VpcId
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNgfwPropsReadFirewall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.EndpointMode"
)
class EndpointMode(enum.Enum):
    '''
    :schema: EndpointMode
    '''

    SERVICE_MANAGED = "SERVICE_MANAGED"
    '''ServiceManaged.'''
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    '''CustomerManaged.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.LogProfileConfig",
    jsii_struct_bases=[],
    name_mapping={
        "log_destination": "logDestination",
        "log_destination_type": "logDestinationType",
        "log_type": "logType",
    },
)
class LogProfileConfig:
    def __init__(
        self,
        *,
        log_destination: builtins.str,
        log_destination_type: "LogProfileConfigLogDestinationType",
        log_type: "LogProfileConfigLogType",
    ) -> None:
        '''Add Log profile config.

        :param log_destination: 
        :param log_destination_type: 
        :param log_type: 

        :schema: LogProfileConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbd3e688630265a99392f1db06e9897764a78868a0e014666ab1b1ec9468311)
            check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
            check_type(argname="argument log_destination_type", value=log_destination_type, expected_type=type_hints["log_destination_type"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_destination": log_destination,
            "log_destination_type": log_destination_type,
            "log_type": log_type,
        }

    @builtins.property
    def log_destination(self) -> builtins.str:
        '''
        :schema: LogProfileConfig#LogDestination
        '''
        result = self._values.get("log_destination")
        assert result is not None, "Required property 'log_destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_destination_type(self) -> "LogProfileConfigLogDestinationType":
        '''
        :schema: LogProfileConfig#LogDestinationType
        '''
        result = self._values.get("log_destination_type")
        assert result is not None, "Required property 'log_destination_type' is missing"
        return typing.cast("LogProfileConfigLogDestinationType", result)

    @builtins.property
    def log_type(self) -> "LogProfileConfigLogType":
        '''
        :schema: LogProfileConfig#LogType
        '''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast("LogProfileConfigLogType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.LogProfileConfigLogDestinationType"
)
class LogProfileConfigLogDestinationType(enum.Enum):
    '''
    :schema: LogProfileConfigLogDestinationType
    '''

    S3 = "S3"
    '''S3.'''
    CLOUD_WATCH_LOGS = "CLOUD_WATCH_LOGS"
    '''CloudWatchLogs.'''
    KINESIS_DATA_FIREHOSE = "KINESIS_DATA_FIREHOSE"
    '''KinesisDataFirehose.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.LogProfileConfigLogType"
)
class LogProfileConfigLogType(enum.Enum):
    '''
    :schema: LogProfileConfigLogType
    '''

    TRAFFIC = "TRAFFIC"
    '''TRAFFIC.'''
    DECRYPTION = "DECRYPTION"
    '''DECRYPTION.'''
    THREAT = "THREAT"
    '''THREAT.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.SubnetMappings",
    jsii_struct_bases=[],
    name_mapping={"availability_zone": "availabilityZone", "subnet_id": "subnetId"},
)
class SubnetMappings:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_zone: 
        :param subnet_id: 

        :schema: SubnetMappings
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa9b9acae3f077e4ecc1fd05621b515e4b1822665b8498c1d579a448a5b8578)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''
        :schema: SubnetMappings#AvailabilityZone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: SubnetMappings#SubnetId
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetMappings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-ngfw.Tag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Tag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 

        :schema: Tag
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf568c9dc0219d71b4b6c76cf031581e711e5dbe1f5fa5650ce6900c5f124d05)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''
        :schema: Tag#Key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''
        :schema: Tag#Value
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Attachment",
    "CfnNgfw",
    "CfnNgfwProps",
    "CfnNgfwPropsReadFirewall",
    "EndpointMode",
    "LogProfileConfig",
    "LogProfileConfigLogDestinationType",
    "LogProfileConfigLogType",
    "SubnetMappings",
    "Tag",
]

publication.publish()

def _typecheckingstub__71aca4af208c41c9d8df7e894754d8890bfe54f292782fb9ceef8fa21b942475(
    *,
    account_id: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    rejected_reason: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44e34122d63b2e649e1a0cf59f5d48094ce3838d16dfa68e3cc9200b395326e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    firewall_name: builtins.str,
    app_id_version: typing.Optional[builtins.str] = None,
    associate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
    cloud_watch_metric_namespace: typing.Optional[builtins.str] = None,
    describe: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disassociate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_mode: typing.Optional[EndpointMode] = None,
    global_rule_stack_name: typing.Optional[builtins.str] = None,
    link_id: typing.Optional[builtins.str] = None,
    log_destination_configs: typing.Optional[typing.Sequence[typing.Union[LogProfileConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_vpc_enable: typing.Optional[builtins.bool] = None,
    read_firewall: typing.Optional[typing.Union[CfnNgfwPropsReadFirewall, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_name: typing.Optional[builtins.str] = None,
    subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babd383745f46351db16da77dd426a0238262cf070da922071ca55f3a80af00b(
    *,
    account_id: builtins.str,
    firewall_name: builtins.str,
    app_id_version: typing.Optional[builtins.str] = None,
    associate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
    cloud_watch_metric_namespace: typing.Optional[builtins.str] = None,
    describe: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disassociate_subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_mode: typing.Optional[EndpointMode] = None,
    global_rule_stack_name: typing.Optional[builtins.str] = None,
    link_id: typing.Optional[builtins.str] = None,
    log_destination_configs: typing.Optional[typing.Sequence[typing.Union[LogProfileConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_vpc_enable: typing.Optional[builtins.bool] = None,
    read_firewall: typing.Optional[typing.Union[CfnNgfwPropsReadFirewall, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_name: typing.Optional[builtins.str] = None,
    subnet_mappings: typing.Optional[typing.Sequence[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce095556ca83beeaecfe83beae6caeda3c0798f9340949d37a095b246fc300a(
    *,
    account_id: typing.Optional[builtins.str] = None,
    app_id_version: typing.Optional[builtins.str] = None,
    attachments: typing.Optional[typing.Sequence[typing.Union[Attachment, typing.Dict[builtins.str, typing.Any]]]] = None,
    automatic_upgrade_app_id_version: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    endpoint_mode: typing.Optional[EndpointMode] = None,
    endpoint_service_name: typing.Optional[builtins.str] = None,
    failure_reason: typing.Optional[builtins.str] = None,
    firewall_name: typing.Optional[builtins.str] = None,
    firewall_status: typing.Optional[builtins.str] = None,
    global_rule_stack_name: typing.Optional[builtins.str] = None,
    link_id: typing.Optional[builtins.str] = None,
    link_status: typing.Optional[builtins.str] = None,
    multi_vpc_enable: typing.Optional[builtins.bool] = None,
    rule_stack_name: typing.Optional[builtins.str] = None,
    rule_stack_status: typing.Optional[builtins.str] = None,
    subnet_mappings: typing.Optional[typing.Union[SubnetMappings, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbd3e688630265a99392f1db06e9897764a78868a0e014666ab1b1ec9468311(
    *,
    log_destination: builtins.str,
    log_destination_type: LogProfileConfigLogDestinationType,
    log_type: LogProfileConfigLogType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa9b9acae3f077e4ecc1fd05621b515e4b1822665b8498c1d579a448a5b8578(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf568c9dc0219d71b4b6c76cf031581e711e5dbe1f5fa5650ce6900c5f124d05(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
