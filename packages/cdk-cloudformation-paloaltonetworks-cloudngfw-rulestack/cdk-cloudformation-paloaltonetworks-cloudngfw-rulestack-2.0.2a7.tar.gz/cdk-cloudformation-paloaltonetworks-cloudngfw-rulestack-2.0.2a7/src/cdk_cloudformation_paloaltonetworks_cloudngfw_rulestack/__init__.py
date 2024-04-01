'''
# paloaltonetworks-cloudngfw-rulestack

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `PaloAltoNetworks::CloudNGFW::RuleStack` v2.0.2.

## Description

A rulestack defines the NGFW's advanced access control (APP-ID, URL Filtering) and threat prevention behavior.

## References

* [Source](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name PaloAltoNetworks::CloudNGFW::RuleStack \
  --publisher-id 4e4cf7d0eb3aa7334767bc17a1dbec7e8279d078 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/4e4cf7d0eb3aa7334767bc17a1dbec7e8279d078/PaloAltoNetworks-CloudNGFW-RuleStack \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `PaloAltoNetworks::CloudNGFW::RuleStack`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fpaloaltonetworks-cloudngfw-rulestack+v2.0.2).
* Issues related to `PaloAltoNetworks::CloudNGFW::RuleStack` should be reported to the [publisher](https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git).

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
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CertObject",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "audit_comment": "auditComment",
        "certificate_self_signed": "certificateSelfSigned",
        "certificate_signer_arn": "certificateSignerArn",
        "description": "description",
    },
)
class CertObject:
    def __init__(
        self,
        *,
        name: builtins.str,
        audit_comment: typing.Optional[builtins.str] = None,
        certificate_self_signed: typing.Optional[builtins.bool] = None,
        certificate_signer_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param audit_comment: 
        :param certificate_self_signed: 
        :param certificate_signer_arn: 
        :param description: 

        :schema: CertObject
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d6ac3c2386c5b531f8cee38336142892325fbd6142e5245726effb6f40e816)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument certificate_self_signed", value=certificate_self_signed, expected_type=type_hints["certificate_self_signed"])
            check_type(argname="argument certificate_signer_arn", value=certificate_signer_arn, expected_type=type_hints["certificate_signer_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if certificate_self_signed is not None:
            self._values["certificate_self_signed"] = certificate_self_signed
        if certificate_signer_arn is not None:
            self._values["certificate_signer_arn"] = certificate_signer_arn
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CertObject#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CertObject#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_self_signed(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CertObject#CertificateSelfSigned
        '''
        result = self._values.get("certificate_self_signed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def certificate_signer_arn(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CertObject#CertificateSignerArn
        '''
        result = self._values.get("certificate_signer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CertObject#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnRuleStack(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CfnRuleStack",
):
    '''A CloudFormation ``PaloAltoNetworks::CloudNGFW::RuleStack``.

    :cloudformationResource: PaloAltoNetworks::CloudNGFW::RuleStack
    :link: https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        rule_stack_name: builtins.str,
        custom_security_profiles: typing.Optional[typing.Union["CustomSecurityProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
        describe: typing.Optional[builtins.bool] = None,
        rule_list: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_stack: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_candidate: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_running: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_state: typing.Optional[builtins.str] = None,
        security_objects: typing.Optional[typing.Union["SecurityObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``PaloAltoNetworks::CloudNGFW::RuleStack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_stack_name: Rule stack name.
        :param custom_security_profiles: 
        :param describe: 
        :param rule_list: list of rules.
        :param rule_stack: 
        :param rule_stack_candidate: 
        :param rule_stack_running: 
        :param rule_stack_state: 
        :param security_objects: 
        :param tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c7cc33ff17b835ba43d025d41b528d4ae64649dcb7cdadf4e7691344839560)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleStackProps(
            rule_stack_name=rule_stack_name,
            custom_security_profiles=custom_security_profiles,
            describe=describe,
            rule_list=rule_list,
            rule_stack=rule_stack,
            rule_stack_candidate=rule_stack_candidate,
            rule_stack_running=rule_stack_running,
            rule_stack_state=rule_stack_state,
            security_objects=security_objects,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnRuleStackProps":
        '''Resource props.'''
        return typing.cast("CfnRuleStackProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CfnRuleStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_stack_name": "ruleStackName",
        "custom_security_profiles": "customSecurityProfiles",
        "describe": "describe",
        "rule_list": "ruleList",
        "rule_stack": "ruleStack",
        "rule_stack_candidate": "ruleStackCandidate",
        "rule_stack_running": "ruleStackRunning",
        "rule_stack_state": "ruleStackState",
        "security_objects": "securityObjects",
        "tags": "tags",
    },
)
class CfnRuleStackProps:
    def __init__(
        self,
        *,
        rule_stack_name: builtins.str,
        custom_security_profiles: typing.Optional[typing.Union["CustomSecurityProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
        describe: typing.Optional[builtins.bool] = None,
        rule_list: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_stack: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_candidate: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_running: typing.Optional[typing.Union["RuleStack", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_stack_state: typing.Optional[builtins.str] = None,
        security_objects: typing.Optional[typing.Union["SecurityObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''A rulestack defines the NGFW's advanced access control (APP-ID, URL Filtering) and threat prevention behavior.

        :param rule_stack_name: Rule stack name.
        :param custom_security_profiles: 
        :param describe: 
        :param rule_list: list of rules.
        :param rule_stack: 
        :param rule_stack_candidate: 
        :param rule_stack_running: 
        :param rule_stack_state: 
        :param security_objects: 
        :param tags: 

        :schema: CfnRuleStackProps
        '''
        if isinstance(custom_security_profiles, dict):
            custom_security_profiles = CustomSecurityProfiles(**custom_security_profiles)
        if isinstance(rule_stack, dict):
            rule_stack = RuleStack(**rule_stack)
        if isinstance(rule_stack_candidate, dict):
            rule_stack_candidate = RuleStack(**rule_stack_candidate)
        if isinstance(rule_stack_running, dict):
            rule_stack_running = RuleStack(**rule_stack_running)
        if isinstance(security_objects, dict):
            security_objects = SecurityObjects(**security_objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c8136c1919524d24a364aecded9e10f8416af6b8e850c6863af00bcc221923)
            check_type(argname="argument rule_stack_name", value=rule_stack_name, expected_type=type_hints["rule_stack_name"])
            check_type(argname="argument custom_security_profiles", value=custom_security_profiles, expected_type=type_hints["custom_security_profiles"])
            check_type(argname="argument describe", value=describe, expected_type=type_hints["describe"])
            check_type(argname="argument rule_list", value=rule_list, expected_type=type_hints["rule_list"])
            check_type(argname="argument rule_stack", value=rule_stack, expected_type=type_hints["rule_stack"])
            check_type(argname="argument rule_stack_candidate", value=rule_stack_candidate, expected_type=type_hints["rule_stack_candidate"])
            check_type(argname="argument rule_stack_running", value=rule_stack_running, expected_type=type_hints["rule_stack_running"])
            check_type(argname="argument rule_stack_state", value=rule_stack_state, expected_type=type_hints["rule_stack_state"])
            check_type(argname="argument security_objects", value=security_objects, expected_type=type_hints["security_objects"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_stack_name": rule_stack_name,
        }
        if custom_security_profiles is not None:
            self._values["custom_security_profiles"] = custom_security_profiles
        if describe is not None:
            self._values["describe"] = describe
        if rule_list is not None:
            self._values["rule_list"] = rule_list
        if rule_stack is not None:
            self._values["rule_stack"] = rule_stack
        if rule_stack_candidate is not None:
            self._values["rule_stack_candidate"] = rule_stack_candidate
        if rule_stack_running is not None:
            self._values["rule_stack_running"] = rule_stack_running
        if rule_stack_state is not None:
            self._values["rule_stack_state"] = rule_stack_state
        if security_objects is not None:
            self._values["security_objects"] = security_objects
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_stack_name(self) -> builtins.str:
        '''Rule stack name.

        :schema: CfnRuleStackProps#RuleStackName
        '''
        result = self._values.get("rule_stack_name")
        assert result is not None, "Required property 'rule_stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_security_profiles(self) -> typing.Optional["CustomSecurityProfiles"]:
        '''
        :schema: CfnRuleStackProps#CustomSecurityProfiles
        '''
        result = self._values.get("custom_security_profiles")
        return typing.cast(typing.Optional["CustomSecurityProfiles"], result)

    @builtins.property
    def describe(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnRuleStackProps#Describe
        '''
        result = self._values.get("describe")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_list(self) -> typing.Optional[typing.List["Rule"]]:
        '''list of rules.

        :schema: CfnRuleStackProps#RuleList
        '''
        result = self._values.get("rule_list")
        return typing.cast(typing.Optional[typing.List["Rule"]], result)

    @builtins.property
    def rule_stack(self) -> typing.Optional["RuleStack"]:
        '''
        :schema: CfnRuleStackProps#RuleStack
        '''
        result = self._values.get("rule_stack")
        return typing.cast(typing.Optional["RuleStack"], result)

    @builtins.property
    def rule_stack_candidate(self) -> typing.Optional["RuleStack"]:
        '''
        :schema: CfnRuleStackProps#RuleStackCandidate
        '''
        result = self._values.get("rule_stack_candidate")
        return typing.cast(typing.Optional["RuleStack"], result)

    @builtins.property
    def rule_stack_running(self) -> typing.Optional["RuleStack"]:
        '''
        :schema: CfnRuleStackProps#RuleStackRunning
        '''
        result = self._values.get("rule_stack_running")
        return typing.cast(typing.Optional["RuleStack"], result)

    @builtins.property
    def rule_stack_state(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnRuleStackProps#RuleStackState
        '''
        result = self._values.get("rule_stack_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_objects(self) -> typing.Optional["SecurityObjects"]:
        '''
        :schema: CfnRuleStackProps#SecurityObjects
        '''
        result = self._values.get("security_objects")
        return typing.cast(typing.Optional["SecurityObjects"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: CfnRuleStackProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CustomSecurityProfiles",
    jsii_struct_bases=[],
    name_mapping={"file_blocking": "fileBlocking"},
)
class CustomSecurityProfiles:
    def __init__(
        self,
        *,
        file_blocking: typing.Optional[typing.Union["FileBlocking", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Custom Security Profiles object.

        :param file_blocking: 

        :schema: CustomSecurityProfiles
        '''
        if isinstance(file_blocking, dict):
            file_blocking = FileBlocking(**file_blocking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84027f810d39d2895ccee8d2febe92c4a03ae5ec46c0964447535dd6704dac1)
            check_type(argname="argument file_blocking", value=file_blocking, expected_type=type_hints["file_blocking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_blocking is not None:
            self._values["file_blocking"] = file_blocking

    @builtins.property
    def file_blocking(self) -> typing.Optional["FileBlocking"]:
        '''
        :schema: CustomSecurityProfiles#FileBlocking
        '''
        result = self._values.get("file_blocking")
        return typing.cast(typing.Optional["FileBlocking"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomSecurityProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CustomUrlCategory",
    jsii_struct_bases=[],
    name_mapping={
        "url_targets": "urlTargets",
        "action": "action",
        "audit_comment": "auditComment",
        "description": "description",
        "name": "name",
    },
)
class CustomUrlCategory:
    def __init__(
        self,
        *,
        url_targets: typing.Sequence[builtins.str],
        action: typing.Optional["CustomUrlCategoryAction"] = None,
        audit_comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url_targets: 
        :param action: 
        :param audit_comment: 
        :param description: 
        :param name: 

        :schema: CustomUrlCategory
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830c73308933291a3ee2d4d48c42bc9f15796ce5f156e5be52961cc636981f16)
            check_type(argname="argument url_targets", value=url_targets, expected_type=type_hints["url_targets"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url_targets": url_targets,
        }
        if action is not None:
            self._values["action"] = action
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def url_targets(self) -> typing.List[builtins.str]:
        '''
        :schema: CustomUrlCategory#URLTargets
        '''
        result = self._values.get("url_targets")
        assert result is not None, "Required property 'url_targets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def action(self) -> typing.Optional["CustomUrlCategoryAction"]:
        '''
        :schema: CustomUrlCategory#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["CustomUrlCategoryAction"], result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CustomUrlCategory#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CustomUrlCategory#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CustomUrlCategory#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomUrlCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.CustomUrlCategoryAction"
)
class CustomUrlCategoryAction(enum.Enum):
    '''
    :schema: CustomUrlCategoryAction
    '''

    NONE = "NONE"
    '''none.'''
    ALLOW = "ALLOW"
    '''allow.'''
    ALERT = "ALERT"
    '''alert.'''
    BLOCK = "BLOCK"
    '''block.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.FileBlocking",
    jsii_struct_bases=[],
    name_mapping={
        "file_type": "fileType",
        "action": "action",
        "audit_comment": "auditComment",
        "description": "description",
        "direction": "direction",
    },
)
class FileBlocking:
    def __init__(
        self,
        *,
        file_type: builtins.str,
        action: typing.Optional["FileBlockingAction"] = None,
        audit_comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        direction: typing.Optional["FileBlockingDirection"] = None,
    ) -> None:
        '''
        :param file_type: 
        :param action: 
        :param audit_comment: 
        :param description: 
        :param direction: 

        :schema: FileBlocking
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ce2a610ca6171bdcaac621e91a827220c3e2edf033d01a98867c3f9e895171)
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_type": file_type,
        }
        if action is not None:
            self._values["action"] = action
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if description is not None:
            self._values["description"] = description
        if direction is not None:
            self._values["direction"] = direction

    @builtins.property
    def file_type(self) -> builtins.str:
        '''
        :schema: FileBlocking#FileType
        '''
        result = self._values.get("file_type")
        assert result is not None, "Required property 'file_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional["FileBlockingAction"]:
        '''
        :schema: FileBlocking#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["FileBlockingAction"], result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: FileBlocking#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: FileBlocking#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional["FileBlockingDirection"]:
        '''
        :schema: FileBlocking#Direction
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional["FileBlockingDirection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileBlocking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.FileBlockingAction"
)
class FileBlockingAction(enum.Enum):
    '''
    :schema: FileBlockingAction
    '''

    ALERT = "ALERT"
    '''alert.'''
    BLOCK = "BLOCK"
    '''block.'''
    CONTINUE = "CONTINUE"
    '''continue.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.FileBlockingDirection"
)
class FileBlockingDirection(enum.Enum):
    '''
    :schema: FileBlockingDirection
    '''

    UPLOAD = "UPLOAD"
    '''upload.'''
    DOWNLOAD = "DOWNLOAD"
    '''download.'''
    BOTH = "BOTH"
    '''both.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.FqdnList",
    jsii_struct_bases=[],
    name_mapping={
        "fqdn_list": "fqdnList",
        "name": "name",
        "audit_comment": "auditComment",
        "description": "description",
    },
)
class FqdnList:
    def __init__(
        self,
        *,
        fqdn_list: typing.Sequence[builtins.str],
        name: builtins.str,
        audit_comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fqdn_list: 
        :param name: 
        :param audit_comment: 
        :param description: 

        :schema: FqdnList
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3127c4f1f9c8f2fe964983aa853d820989a9882d87e2d9cf93dd8a26c6c1178b)
            check_type(argname="argument fqdn_list", value=fqdn_list, expected_type=type_hints["fqdn_list"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqdn_list": fqdn_list,
            "name": name,
        }
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def fqdn_list(self) -> typing.List[builtins.str]:
        '''
        :schema: FqdnList#FqdnList
        '''
        result = self._values.get("fqdn_list")
        assert result is not None, "Required property 'fqdn_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: FqdnList#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: FqdnList#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: FqdnList#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FqdnList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.IntelligentFeed",
    jsii_struct_bases=[],
    name_mapping={
        "feed_url": "feedUrl",
        "frequency": "frequency",
        "name": "name",
        "type": "type",
        "audit_comment": "auditComment",
        "certificate": "certificate",
        "description": "description",
        "time": "time",
    },
)
class IntelligentFeed:
    def __init__(
        self,
        *,
        feed_url: builtins.str,
        frequency: "IntelligentFeedFrequency",
        name: builtins.str,
        type: "IntelligentFeedType",
        audit_comment: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param feed_url: 
        :param frequency: 
        :param name: 
        :param type: 
        :param audit_comment: 
        :param certificate: 
        :param description: 
        :param time: 

        :schema: IntelligentFeed
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec9c2ae63a4f349bc39761203d676765b828d7da4c1124c1e206d6d2d5fb899)
            check_type(argname="argument feed_url", value=feed_url, expected_type=type_hints["feed_url"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feed_url": feed_url,
            "frequency": frequency,
            "name": name,
            "type": type,
        }
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if certificate is not None:
            self._values["certificate"] = certificate
        if description is not None:
            self._values["description"] = description
        if time is not None:
            self._values["time"] = time

    @builtins.property
    def feed_url(self) -> builtins.str:
        '''
        :schema: IntelligentFeed#FeedURL
        '''
        result = self._values.get("feed_url")
        assert result is not None, "Required property 'feed_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def frequency(self) -> "IntelligentFeedFrequency":
        '''
        :schema: IntelligentFeed#Frequency
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast("IntelligentFeedFrequency", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: IntelligentFeed#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "IntelligentFeedType":
        '''
        :schema: IntelligentFeed#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("IntelligentFeedType", result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: IntelligentFeed#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''
        :schema: IntelligentFeed#Certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: IntelligentFeed#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: IntelligentFeed#Time
        '''
        result = self._values.get("time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntelligentFeed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.IntelligentFeedFrequency"
)
class IntelligentFeedFrequency(enum.Enum):
    '''
    :schema: IntelligentFeedFrequency
    '''

    HOURLY = "HOURLY"
    '''HOURLY.'''
    DAILY = "DAILY"
    '''DAILY.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.IntelligentFeedType"
)
class IntelligentFeedType(enum.Enum):
    '''
    :schema: IntelligentFeedType
    '''

    IP_UNDERSCORE_LIST = "IP_UNDERSCORE_LIST"
    '''IP_LIST.'''
    URL_UNDERSCORE_LIST = "URL_UNDERSCORE_LIST"
    '''URL_LIST.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.PrefixList",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "prefix_list": "prefixList",
        "audit_comment": "auditComment",
        "description": "description",
    },
)
class PrefixList:
    def __init__(
        self,
        *,
        name: builtins.str,
        prefix_list: typing.Sequence[builtins.str],
        audit_comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''SecurityObjects PrefixList.

        :param name: 
        :param prefix_list: 
        :param audit_comment: 
        :param description: 

        :schema: PrefixList
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68ead3c17f66dcf33cc7221a2d82876562da8f6a9f7b7ae4c672f7b4ae987e7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument prefix_list", value=prefix_list, expected_type=type_hints["prefix_list"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "prefix_list": prefix_list,
        }
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: PrefixList#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_list(self) -> typing.List[builtins.str]:
        '''
        :schema: PrefixList#PrefixList
        '''
        result = self._values.get("prefix_list")
        assert result is not None, "Required property 'prefix_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: PrefixList#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: PrefixList#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrefixList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.Rule",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "rule_list_type": "ruleListType",
        "rule_name": "ruleName",
        "action": "action",
        "applications": "applications",
        "audit_comment": "auditComment",
        "category": "category",
        "decryption_rule_type": "decryptionRuleType",
        "description": "description",
        "destination": "destination",
        "enabled": "enabled",
        "inbound_inspection_certificate": "inboundInspectionCertificate",
        "logging": "logging",
        "negate_destination": "negateDestination",
        "negate_source": "negateSource",
        "protocol": "protocol",
        "prot_port_list": "protPortList",
        "source": "source",
        "tags": "tags",
    },
)
class Rule:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        rule_list_type: builtins.str,
        rule_name: builtins.str,
        action: typing.Optional["RuleAction"] = None,
        applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_comment: typing.Optional[builtins.str] = None,
        category: typing.Optional[typing.Union["UrlCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        decryption_rule_type: typing.Optional["RuleDecryptionRuleType"] = None,
        description: typing.Optional[builtins.str] = None,
        destination: typing.Optional[typing.Union["RuleDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        inbound_inspection_certificate: typing.Optional[builtins.str] = None,
        logging: typing.Optional[builtins.bool] = None,
        negate_destination: typing.Optional[builtins.bool] = None,
        negate_source: typing.Optional[builtins.bool] = None,
        protocol: typing.Optional[builtins.str] = None,
        prot_port_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[typing.Union["RuleSource", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param priority: Priority of the Rule.
        :param rule_list_type: RuleList type: LocalRule, PreRule, PostRule.
        :param rule_name: 
        :param action: 
        :param applications: 
        :param audit_comment: 
        :param category: 
        :param decryption_rule_type: 
        :param description: 
        :param destination: 
        :param enabled: 
        :param inbound_inspection_certificate: 
        :param logging: 
        :param negate_destination: 
        :param negate_source: 
        :param protocol: 
        :param prot_port_list: 
        :param source: 
        :param tags: 

        :schema: Rule
        '''
        if isinstance(category, dict):
            category = UrlCategory(**category)
        if isinstance(destination, dict):
            destination = RuleDestination(**destination)
        if isinstance(source, dict):
            source = RuleSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1559e2eb543be761cfb946660f1bef4742af014d57a6fe77237f8e873b39f53f)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rule_list_type", value=rule_list_type, expected_type=type_hints["rule_list_type"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument decryption_rule_type", value=decryption_rule_type, expected_type=type_hints["decryption_rule_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument inbound_inspection_certificate", value=inbound_inspection_certificate, expected_type=type_hints["inbound_inspection_certificate"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument negate_destination", value=negate_destination, expected_type=type_hints["negate_destination"])
            check_type(argname="argument negate_source", value=negate_source, expected_type=type_hints["negate_source"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument prot_port_list", value=prot_port_list, expected_type=type_hints["prot_port_list"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "rule_list_type": rule_list_type,
            "rule_name": rule_name,
        }
        if action is not None:
            self._values["action"] = action
        if applications is not None:
            self._values["applications"] = applications
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if category is not None:
            self._values["category"] = category
        if decryption_rule_type is not None:
            self._values["decryption_rule_type"] = decryption_rule_type
        if description is not None:
            self._values["description"] = description
        if destination is not None:
            self._values["destination"] = destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if inbound_inspection_certificate is not None:
            self._values["inbound_inspection_certificate"] = inbound_inspection_certificate
        if logging is not None:
            self._values["logging"] = logging
        if negate_destination is not None:
            self._values["negate_destination"] = negate_destination
        if negate_source is not None:
            self._values["negate_source"] = negate_source
        if protocol is not None:
            self._values["protocol"] = protocol
        if prot_port_list is not None:
            self._values["prot_port_list"] = prot_port_list
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Priority of the Rule.

        :schema: Rule#Priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_list_type(self) -> builtins.str:
        '''RuleList type: LocalRule, PreRule, PostRule.

        :schema: Rule#RuleListType
        '''
        result = self._values.get("rule_list_type")
        assert result is not None, "Required property 'rule_list_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''
        :schema: Rule#RuleName
        '''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional["RuleAction"]:
        '''
        :schema: Rule#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["RuleAction"], result)

    @builtins.property
    def applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: Rule#Applications
        '''
        result = self._values.get("applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Rule#AuditComment
        '''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def category(self) -> typing.Optional["UrlCategory"]:
        '''
        :schema: Rule#Category
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional["UrlCategory"], result)

    @builtins.property
    def decryption_rule_type(self) -> typing.Optional["RuleDecryptionRuleType"]:
        '''
        :schema: Rule#DecryptionRuleType
        '''
        result = self._values.get("decryption_rule_type")
        return typing.cast(typing.Optional["RuleDecryptionRuleType"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Rule#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional["RuleDestination"]:
        '''
        :schema: Rule#Destination
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional["RuleDestination"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Rule#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inbound_inspection_certificate(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Rule#InboundInspectionCertificate
        '''
        result = self._values.get("inbound_inspection_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Rule#Logging
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def negate_destination(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Rule#NegateDestination
        '''
        result = self._values.get("negate_destination")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def negate_source(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Rule#NegateSource
        '''
        result = self._values.get("negate_source")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Rule#Protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prot_port_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: Rule#ProtPortList
        '''
        result = self._values.get("prot_port_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional["RuleSource"]:
        '''
        :schema: Rule#Source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["RuleSource"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''
        :schema: Rule#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Rule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleAction"
)
class RuleAction(enum.Enum):
    '''
    :schema: RuleAction
    '''

    ALLOW = "ALLOW"
    '''Allow.'''
    DENY_SILENT = "DENY_SILENT"
    '''DenySilent.'''
    DENY_RESET_SERVER = "DENY_RESET_SERVER"
    '''DenyResetServer.'''
    DENY_RESET_BOTH = "DENY_RESET_BOTH"
    '''DenyResetBoth.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleDecryptionRuleType"
)
class RuleDecryptionRuleType(enum.Enum):
    '''
    :schema: RuleDecryptionRuleType
    '''

    SSL_OUTBOUND_INSPECTION = "SSL_OUTBOUND_INSPECTION"
    '''SSLOutboundInspection.'''
    SSL_INBOUND_INSPECTION = "SSL_INBOUND_INSPECTION"
    '''SSLInboundInspection.'''
    SSL_OUTBOUND_NO_INSPECTION = "SSL_OUTBOUND_NO_INSPECTION"
    '''SSLOutboundNoInspection.'''
    SSL_INBOUND_NO_INSPECTION = "SSL_INBOUND_NO_INSPECTION"
    '''SSLInboundNoInspection.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleDestination",
    jsii_struct_bases=[],
    name_mapping={
        "cidrs": "cidrs",
        "countries": "countries",
        "feeds": "feeds",
        "fqdn_lists": "fqdnLists",
        "prefix_lists": "prefixLists",
    },
)
class RuleDestination:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        fqdn_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: 
        :param countries: Country code.
        :param feeds: 
        :param fqdn_lists: 
        :param prefix_lists: 

        :schema: RuleDestination
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe09e1879bd3e3353da8968910e88d1687146fd84be5571ec51513a513edc79e)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument countries", value=countries, expected_type=type_hints["countries"])
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
            check_type(argname="argument fqdn_lists", value=fqdn_lists, expected_type=type_hints["fqdn_lists"])
            check_type(argname="argument prefix_lists", value=prefix_lists, expected_type=type_hints["prefix_lists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs
        if countries is not None:
            self._values["countries"] = countries
        if feeds is not None:
            self._values["feeds"] = feeds
        if fqdn_lists is not None:
            self._values["fqdn_lists"] = fqdn_lists
        if prefix_lists is not None:
            self._values["prefix_lists"] = prefix_lists

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleDestination#Cidrs
        '''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def countries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Country code.

        :schema: RuleDestination#Countries
        '''
        result = self._values.get("countries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleDestination#Feeds
        '''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fqdn_lists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleDestination#FqdnLists
        '''
        result = self._values.get("fqdn_lists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix_lists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleDestination#PrefixLists
        '''
        result = self._values.get("prefix_lists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleSource",
    jsii_struct_bases=[],
    name_mapping={
        "cidrs": "cidrs",
        "countries": "countries",
        "feeds": "feeds",
        "prefix_lists": "prefixLists",
    },
)
class RuleSource:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: 
        :param countries: Country code.
        :param feeds: 
        :param prefix_lists: 

        :schema: RuleSource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1079bd7b35024c37a4b39590b99145a22f04c01c1d29393854434497561c78d2)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument countries", value=countries, expected_type=type_hints["countries"])
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
            check_type(argname="argument prefix_lists", value=prefix_lists, expected_type=type_hints["prefix_lists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs
        if countries is not None:
            self._values["countries"] = countries
        if feeds is not None:
            self._values["feeds"] = feeds
        if prefix_lists is not None:
            self._values["prefix_lists"] = prefix_lists

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleSource#Cidrs
        '''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def countries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Country code.

        :schema: RuleSource#Countries
        '''
        result = self._values.get("countries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleSource#Feeds
        '''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix_lists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: RuleSource#PrefixLists
        '''
        result = self._values.get("prefix_lists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStack",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "deploy": "deploy",
        "description": "description",
        "lookup_x_forwarded_for": "lookupXForwardedFor",
        "min_app_id_version": "minAppIdVersion",
        "profiles": "profiles",
        "scope": "scope",
    },
)
class RuleStack:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        deploy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        lookup_x_forwarded_for: typing.Optional["RuleStackLookupXForwardedFor"] = None,
        min_app_id_version: typing.Optional[builtins.str] = None,
        profiles: typing.Optional[typing.Union["RuleStackProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
        scope: typing.Optional["RuleStackScope"] = None,
    ) -> None:
        '''
        :param account_id: 
        :param deploy: Deploy RuleStack YES/NO.
        :param description: 
        :param lookup_x_forwarded_for: 
        :param min_app_id_version: 
        :param profiles: 
        :param scope: 

        :schema: RuleStack
        '''
        if isinstance(profiles, dict):
            profiles = RuleStackProfiles(**profiles)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc27e150c9a6696d53c09a804509dc46f37719e6bdb1473a194188b6884b961)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument lookup_x_forwarded_for", value=lookup_x_forwarded_for, expected_type=type_hints["lookup_x_forwarded_for"])
            check_type(argname="argument min_app_id_version", value=min_app_id_version, expected_type=type_hints["min_app_id_version"])
            check_type(argname="argument profiles", value=profiles, expected_type=type_hints["profiles"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if deploy is not None:
            self._values["deploy"] = deploy
        if description is not None:
            self._values["description"] = description
        if lookup_x_forwarded_for is not None:
            self._values["lookup_x_forwarded_for"] = lookup_x_forwarded_for
        if min_app_id_version is not None:
            self._values["min_app_id_version"] = min_app_id_version
        if profiles is not None:
            self._values["profiles"] = profiles
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RuleStack#AccountId
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deploy(self) -> typing.Optional[builtins.str]:
        '''Deploy RuleStack YES/NO.

        :schema: RuleStack#Deploy
        '''
        result = self._values.get("deploy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RuleStack#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lookup_x_forwarded_for(self) -> typing.Optional["RuleStackLookupXForwardedFor"]:
        '''
        :schema: RuleStack#LookupXForwardedFor
        '''
        result = self._values.get("lookup_x_forwarded_for")
        return typing.cast(typing.Optional["RuleStackLookupXForwardedFor"], result)

    @builtins.property
    def min_app_id_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RuleStack#MinAppIdVersion
        '''
        result = self._values.get("min_app_id_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profiles(self) -> typing.Optional["RuleStackProfiles"]:
        '''
        :schema: RuleStack#Profiles
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional["RuleStackProfiles"], result)

    @builtins.property
    def scope(self) -> typing.Optional["RuleStackScope"]:
        '''
        :schema: RuleStack#Scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional["RuleStackScope"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackLookupXForwardedFor"
)
class RuleStackLookupXForwardedFor(enum.Enum):
    '''
    :schema: RuleStackLookupXForwardedFor
    '''

    SECURITY_POLICY = "SECURITY_POLICY"
    '''SecurityPolicy.'''
    NONE = "NONE"
    '''None.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfiles",
    jsii_struct_bases=[],
    name_mapping={
        "anti_spyware_profile": "antiSpywareProfile",
        "anti_virus_profile": "antiVirusProfile",
        "file_blocking_profile": "fileBlockingProfile",
        "outbound_trust_certificate": "outboundTrustCertificate",
        "outbound_untrust_certificate": "outboundUntrustCertificate",
        "url_filtering_profile": "urlFilteringProfile",
        "vulnerability_profile": "vulnerabilityProfile",
    },
)
class RuleStackProfiles:
    def __init__(
        self,
        *,
        anti_spyware_profile: typing.Optional["RuleStackProfilesAntiSpywareProfile"] = None,
        anti_virus_profile: typing.Optional["RuleStackProfilesAntiVirusProfile"] = None,
        file_blocking_profile: typing.Optional["RuleStackProfilesFileBlockingProfile"] = None,
        outbound_trust_certificate: typing.Optional[builtins.str] = None,
        outbound_untrust_certificate: typing.Optional[builtins.str] = None,
        url_filtering_profile: typing.Optional["RuleStackProfilesUrlFilteringProfile"] = None,
        vulnerability_profile: typing.Optional["RuleStackProfilesVulnerabilityProfile"] = None,
    ) -> None:
        '''
        :param anti_spyware_profile: 
        :param anti_virus_profile: 
        :param file_blocking_profile: 
        :param outbound_trust_certificate: 
        :param outbound_untrust_certificate: 
        :param url_filtering_profile: 
        :param vulnerability_profile: 

        :schema: RuleStackProfiles
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a675ea3ae19d813822fc5d604c1e2eb443efc88ea80adef866c36efd57709096)
            check_type(argname="argument anti_spyware_profile", value=anti_spyware_profile, expected_type=type_hints["anti_spyware_profile"])
            check_type(argname="argument anti_virus_profile", value=anti_virus_profile, expected_type=type_hints["anti_virus_profile"])
            check_type(argname="argument file_blocking_profile", value=file_blocking_profile, expected_type=type_hints["file_blocking_profile"])
            check_type(argname="argument outbound_trust_certificate", value=outbound_trust_certificate, expected_type=type_hints["outbound_trust_certificate"])
            check_type(argname="argument outbound_untrust_certificate", value=outbound_untrust_certificate, expected_type=type_hints["outbound_untrust_certificate"])
            check_type(argname="argument url_filtering_profile", value=url_filtering_profile, expected_type=type_hints["url_filtering_profile"])
            check_type(argname="argument vulnerability_profile", value=vulnerability_profile, expected_type=type_hints["vulnerability_profile"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if anti_spyware_profile is not None:
            self._values["anti_spyware_profile"] = anti_spyware_profile
        if anti_virus_profile is not None:
            self._values["anti_virus_profile"] = anti_virus_profile
        if file_blocking_profile is not None:
            self._values["file_blocking_profile"] = file_blocking_profile
        if outbound_trust_certificate is not None:
            self._values["outbound_trust_certificate"] = outbound_trust_certificate
        if outbound_untrust_certificate is not None:
            self._values["outbound_untrust_certificate"] = outbound_untrust_certificate
        if url_filtering_profile is not None:
            self._values["url_filtering_profile"] = url_filtering_profile
        if vulnerability_profile is not None:
            self._values["vulnerability_profile"] = vulnerability_profile

    @builtins.property
    def anti_spyware_profile(
        self,
    ) -> typing.Optional["RuleStackProfilesAntiSpywareProfile"]:
        '''
        :schema: RuleStackProfiles#AntiSpywareProfile
        '''
        result = self._values.get("anti_spyware_profile")
        return typing.cast(typing.Optional["RuleStackProfilesAntiSpywareProfile"], result)

    @builtins.property
    def anti_virus_profile(
        self,
    ) -> typing.Optional["RuleStackProfilesAntiVirusProfile"]:
        '''
        :schema: RuleStackProfiles#AntiVirusProfile
        '''
        result = self._values.get("anti_virus_profile")
        return typing.cast(typing.Optional["RuleStackProfilesAntiVirusProfile"], result)

    @builtins.property
    def file_blocking_profile(
        self,
    ) -> typing.Optional["RuleStackProfilesFileBlockingProfile"]:
        '''
        :schema: RuleStackProfiles#FileBlockingProfile
        '''
        result = self._values.get("file_blocking_profile")
        return typing.cast(typing.Optional["RuleStackProfilesFileBlockingProfile"], result)

    @builtins.property
    def outbound_trust_certificate(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RuleStackProfiles#OutboundTrustCertificate
        '''
        result = self._values.get("outbound_trust_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_untrust_certificate(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RuleStackProfiles#OutboundUntrustCertificate
        '''
        result = self._values.get("outbound_untrust_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_filtering_profile(
        self,
    ) -> typing.Optional["RuleStackProfilesUrlFilteringProfile"]:
        '''
        :schema: RuleStackProfiles#URLFilteringProfile
        '''
        result = self._values.get("url_filtering_profile")
        return typing.cast(typing.Optional["RuleStackProfilesUrlFilteringProfile"], result)

    @builtins.property
    def vulnerability_profile(
        self,
    ) -> typing.Optional["RuleStackProfilesVulnerabilityProfile"]:
        '''
        :schema: RuleStackProfiles#VulnerabilityProfile
        '''
        result = self._values.get("vulnerability_profile")
        return typing.cast(typing.Optional["RuleStackProfilesVulnerabilityProfile"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleStackProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfilesAntiSpywareProfile"
)
class RuleStackProfilesAntiSpywareProfile(enum.Enum):
    '''
    :schema: RuleStackProfilesAntiSpywareProfile
    '''

    BEST_PRACTICE = "BEST_PRACTICE"
    '''BestPractice.'''
    NONE = "NONE"
    '''None.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfilesAntiVirusProfile"
)
class RuleStackProfilesAntiVirusProfile(enum.Enum):
    '''
    :schema: RuleStackProfilesAntiVirusProfile
    '''

    BEST_PRACTICE = "BEST_PRACTICE"
    '''BestPractice.'''
    NONE = "NONE"
    '''None.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfilesFileBlockingProfile"
)
class RuleStackProfilesFileBlockingProfile(enum.Enum):
    '''
    :schema: RuleStackProfilesFileBlockingProfile
    '''

    CUSTOM = "CUSTOM"
    '''Custom.'''
    BEST_PRACTICE = "BEST_PRACTICE"
    '''BestPractice.'''
    NONE = "NONE"
    '''None.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfilesUrlFilteringProfile"
)
class RuleStackProfilesUrlFilteringProfile(enum.Enum):
    '''
    :schema: RuleStackProfilesUrlFilteringProfile
    '''

    BEST_PRACTICE = "BEST_PRACTICE"
    '''BestPractice.'''
    NONE = "NONE"
    '''None.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackProfilesVulnerabilityProfile"
)
class RuleStackProfilesVulnerabilityProfile(enum.Enum):
    '''
    :schema: RuleStackProfilesVulnerabilityProfile
    '''

    BEST_PRACTICE = "BEST_PRACTICE"
    '''BestPractice.'''
    NONE = "NONE"
    '''None.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.RuleStackScope"
)
class RuleStackScope(enum.Enum):
    '''
    :schema: RuleStackScope
    '''

    LOCAL = "LOCAL"
    '''Local.'''
    GLOBAL = "GLOBAL"
    '''Global.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.SecurityObjects",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_objects": "certificateObjects",
        "custom_url_categories": "customUrlCategories",
        "fqdn_lists": "fqdnLists",
        "intelligent_feeds": "intelligentFeeds",
        "prefix_lists": "prefixLists",
    },
)
class SecurityObjects:
    def __init__(
        self,
        *,
        certificate_objects: typing.Optional[typing.Sequence[typing.Union[CertObject, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_url_categories: typing.Optional[typing.Sequence[typing.Union[CustomUrlCategory, typing.Dict[builtins.str, typing.Any]]]] = None,
        fqdn_lists: typing.Optional[typing.Sequence[typing.Union[FqdnList, typing.Dict[builtins.str, typing.Any]]]] = None,
        intelligent_feeds: typing.Optional[typing.Sequence[typing.Union[IntelligentFeed, typing.Dict[builtins.str, typing.Any]]]] = None,
        prefix_lists: typing.Optional[typing.Sequence[typing.Union[PrefixList, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Security objects.

        :param certificate_objects: 
        :param custom_url_categories: 
        :param fqdn_lists: 
        :param intelligent_feeds: 
        :param prefix_lists: 

        :schema: SecurityObjects
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee7d3683ff6eac0f3ac267705b36fe7905bf1aa920e54f9233a748cf58bf808)
            check_type(argname="argument certificate_objects", value=certificate_objects, expected_type=type_hints["certificate_objects"])
            check_type(argname="argument custom_url_categories", value=custom_url_categories, expected_type=type_hints["custom_url_categories"])
            check_type(argname="argument fqdn_lists", value=fqdn_lists, expected_type=type_hints["fqdn_lists"])
            check_type(argname="argument intelligent_feeds", value=intelligent_feeds, expected_type=type_hints["intelligent_feeds"])
            check_type(argname="argument prefix_lists", value=prefix_lists, expected_type=type_hints["prefix_lists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_objects is not None:
            self._values["certificate_objects"] = certificate_objects
        if custom_url_categories is not None:
            self._values["custom_url_categories"] = custom_url_categories
        if fqdn_lists is not None:
            self._values["fqdn_lists"] = fqdn_lists
        if intelligent_feeds is not None:
            self._values["intelligent_feeds"] = intelligent_feeds
        if prefix_lists is not None:
            self._values["prefix_lists"] = prefix_lists

    @builtins.property
    def certificate_objects(self) -> typing.Optional[typing.List[CertObject]]:
        '''
        :schema: SecurityObjects#CertificateObjects
        '''
        result = self._values.get("certificate_objects")
        return typing.cast(typing.Optional[typing.List[CertObject]], result)

    @builtins.property
    def custom_url_categories(self) -> typing.Optional[typing.List[CustomUrlCategory]]:
        '''
        :schema: SecurityObjects#CustomUrlCategories
        '''
        result = self._values.get("custom_url_categories")
        return typing.cast(typing.Optional[typing.List[CustomUrlCategory]], result)

    @builtins.property
    def fqdn_lists(self) -> typing.Optional[typing.List[FqdnList]]:
        '''
        :schema: SecurityObjects#FqdnLists
        '''
        result = self._values.get("fqdn_lists")
        return typing.cast(typing.Optional[typing.List[FqdnList]], result)

    @builtins.property
    def intelligent_feeds(self) -> typing.Optional[typing.List[IntelligentFeed]]:
        '''
        :schema: SecurityObjects#IntelligentFeeds
        '''
        result = self._values.get("intelligent_feeds")
        return typing.cast(typing.Optional[typing.List[IntelligentFeed]], result)

    @builtins.property
    def prefix_lists(self) -> typing.Optional[typing.List[PrefixList]]:
        '''
        :schema: SecurityObjects#PrefixLists
        '''
        result = self._values.get("prefix_lists")
        return typing.cast(typing.Optional[typing.List[PrefixList]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.Tag",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005bcd9714b565d3ed41be5286571c83f378b1fc3601af9e75d639f20c73ab3b)
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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/paloaltonetworks-cloudngfw-rulestack.UrlCategory",
    jsii_struct_bases=[],
    name_mapping={"feeds": "feeds", "url_category_names": "urlCategoryNames"},
)
class UrlCategory:
    def __init__(
        self,
        *,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        url_category_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param feeds: 
        :param url_category_names: 

        :schema: UrlCategory
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0818e65659d29fe233c74b177d28670185d0e7ba1ae096574821ecf6786123)
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
            check_type(argname="argument url_category_names", value=url_category_names, expected_type=type_hints["url_category_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if feeds is not None:
            self._values["feeds"] = feeds
        if url_category_names is not None:
            self._values["url_category_names"] = url_category_names

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: UrlCategory#Feeds
        '''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url_category_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: UrlCategory#URLCategoryNames
        '''
        result = self._values.get("url_category_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UrlCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CertObject",
    "CfnRuleStack",
    "CfnRuleStackProps",
    "CustomSecurityProfiles",
    "CustomUrlCategory",
    "CustomUrlCategoryAction",
    "FileBlocking",
    "FileBlockingAction",
    "FileBlockingDirection",
    "FqdnList",
    "IntelligentFeed",
    "IntelligentFeedFrequency",
    "IntelligentFeedType",
    "PrefixList",
    "Rule",
    "RuleAction",
    "RuleDecryptionRuleType",
    "RuleDestination",
    "RuleSource",
    "RuleStack",
    "RuleStackLookupXForwardedFor",
    "RuleStackProfiles",
    "RuleStackProfilesAntiSpywareProfile",
    "RuleStackProfilesAntiVirusProfile",
    "RuleStackProfilesFileBlockingProfile",
    "RuleStackProfilesUrlFilteringProfile",
    "RuleStackProfilesVulnerabilityProfile",
    "RuleStackScope",
    "SecurityObjects",
    "Tag",
    "UrlCategory",
]

publication.publish()

def _typecheckingstub__f3d6ac3c2386c5b531f8cee38336142892325fbd6142e5245726effb6f40e816(
    *,
    name: builtins.str,
    audit_comment: typing.Optional[builtins.str] = None,
    certificate_self_signed: typing.Optional[builtins.bool] = None,
    certificate_signer_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c7cc33ff17b835ba43d025d41b528d4ae64649dcb7cdadf4e7691344839560(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rule_stack_name: builtins.str,
    custom_security_profiles: typing.Optional[typing.Union[CustomSecurityProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
    describe: typing.Optional[builtins.bool] = None,
    rule_list: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_stack: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_candidate: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_running: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_state: typing.Optional[builtins.str] = None,
    security_objects: typing.Optional[typing.Union[SecurityObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c8136c1919524d24a364aecded9e10f8416af6b8e850c6863af00bcc221923(
    *,
    rule_stack_name: builtins.str,
    custom_security_profiles: typing.Optional[typing.Union[CustomSecurityProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
    describe: typing.Optional[builtins.bool] = None,
    rule_list: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_stack: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_candidate: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_running: typing.Optional[typing.Union[RuleStack, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_stack_state: typing.Optional[builtins.str] = None,
    security_objects: typing.Optional[typing.Union[SecurityObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84027f810d39d2895ccee8d2febe92c4a03ae5ec46c0964447535dd6704dac1(
    *,
    file_blocking: typing.Optional[typing.Union[FileBlocking, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830c73308933291a3ee2d4d48c42bc9f15796ce5f156e5be52961cc636981f16(
    *,
    url_targets: typing.Sequence[builtins.str],
    action: typing.Optional[CustomUrlCategoryAction] = None,
    audit_comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ce2a610ca6171bdcaac621e91a827220c3e2edf033d01a98867c3f9e895171(
    *,
    file_type: builtins.str,
    action: typing.Optional[FileBlockingAction] = None,
    audit_comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    direction: typing.Optional[FileBlockingDirection] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3127c4f1f9c8f2fe964983aa853d820989a9882d87e2d9cf93dd8a26c6c1178b(
    *,
    fqdn_list: typing.Sequence[builtins.str],
    name: builtins.str,
    audit_comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec9c2ae63a4f349bc39761203d676765b828d7da4c1124c1e206d6d2d5fb899(
    *,
    feed_url: builtins.str,
    frequency: IntelligentFeedFrequency,
    name: builtins.str,
    type: IntelligentFeedType,
    audit_comment: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68ead3c17f66dcf33cc7221a2d82876562da8f6a9f7b7ae4c672f7b4ae987e7(
    *,
    name: builtins.str,
    prefix_list: typing.Sequence[builtins.str],
    audit_comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1559e2eb543be761cfb946660f1bef4742af014d57a6fe77237f8e873b39f53f(
    *,
    priority: jsii.Number,
    rule_list_type: builtins.str,
    rule_name: builtins.str,
    action: typing.Optional[RuleAction] = None,
    applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_comment: typing.Optional[builtins.str] = None,
    category: typing.Optional[typing.Union[UrlCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    decryption_rule_type: typing.Optional[RuleDecryptionRuleType] = None,
    description: typing.Optional[builtins.str] = None,
    destination: typing.Optional[typing.Union[RuleDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    inbound_inspection_certificate: typing.Optional[builtins.str] = None,
    logging: typing.Optional[builtins.bool] = None,
    negate_destination: typing.Optional[builtins.bool] = None,
    negate_source: typing.Optional[builtins.bool] = None,
    protocol: typing.Optional[builtins.str] = None,
    prot_port_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[typing.Union[RuleSource, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe09e1879bd3e3353da8968910e88d1687146fd84be5571ec51513a513edc79e(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    countries: typing.Optional[typing.Sequence[builtins.str]] = None,
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    fqdn_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1079bd7b35024c37a4b39590b99145a22f04c01c1d29393854434497561c78d2(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    countries: typing.Optional[typing.Sequence[builtins.str]] = None,
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc27e150c9a6696d53c09a804509dc46f37719e6bdb1473a194188b6884b961(
    *,
    account_id: typing.Optional[builtins.str] = None,
    deploy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    lookup_x_forwarded_for: typing.Optional[RuleStackLookupXForwardedFor] = None,
    min_app_id_version: typing.Optional[builtins.str] = None,
    profiles: typing.Optional[typing.Union[RuleStackProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
    scope: typing.Optional[RuleStackScope] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a675ea3ae19d813822fc5d604c1e2eb443efc88ea80adef866c36efd57709096(
    *,
    anti_spyware_profile: typing.Optional[RuleStackProfilesAntiSpywareProfile] = None,
    anti_virus_profile: typing.Optional[RuleStackProfilesAntiVirusProfile] = None,
    file_blocking_profile: typing.Optional[RuleStackProfilesFileBlockingProfile] = None,
    outbound_trust_certificate: typing.Optional[builtins.str] = None,
    outbound_untrust_certificate: typing.Optional[builtins.str] = None,
    url_filtering_profile: typing.Optional[RuleStackProfilesUrlFilteringProfile] = None,
    vulnerability_profile: typing.Optional[RuleStackProfilesVulnerabilityProfile] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee7d3683ff6eac0f3ac267705b36fe7905bf1aa920e54f9233a748cf58bf808(
    *,
    certificate_objects: typing.Optional[typing.Sequence[typing.Union[CertObject, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_url_categories: typing.Optional[typing.Sequence[typing.Union[CustomUrlCategory, typing.Dict[builtins.str, typing.Any]]]] = None,
    fqdn_lists: typing.Optional[typing.Sequence[typing.Union[FqdnList, typing.Dict[builtins.str, typing.Any]]]] = None,
    intelligent_feeds: typing.Optional[typing.Sequence[typing.Union[IntelligentFeed, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix_lists: typing.Optional[typing.Sequence[typing.Union[PrefixList, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005bcd9714b565d3ed41be5286571c83f378b1fc3601af9e75d639f20c73ab3b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0818e65659d29fe233c74b177d28670185d0e7ba1ae096574821ecf6786123(
    *,
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    url_category_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
