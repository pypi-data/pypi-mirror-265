'''
# @reapit-cdk/entra-id-application

![npm version](https://img.shields.io/npm/v/@reapit-cdk/entra-id-application)
![npm downloads](https://img.shields.io/npm/dm/@reapit-cdk/entra-id-application)
![coverage: 0%25](https://img.shields.io/badge/coverage-0%25-red)
![Integ Tests: X](https://img.shields.io/badge/Integ%20Tests-X-red)

This construct creates and manages a Microsoft Entra ID Application

## Package Installation:

```sh
yarn add --dev @reapit-cdk/entra-id-application
# or
npm install @reapit-cdk/entra-id-application --save-dev
```

## Usage

```python
import { CfnOutput, Stack, App, Duration } from 'aws-cdk-lib'
import { EntraIDApplication } from '@reapit-cdk/entra-id-application'
import { Secret } from 'aws-cdk-lib/aws-secretsmanager'

const app = new App()
const stack = new Stack(app, 'stack-name')
const entraApp = new EntraIDApplication(stack, 'entra-id-app', {
  /**
   * 1. Create an application in Entra ID with scopes:
   *  - Application.ReadWrite.All
   * 2. Create a client secret which lasts a day
   * 3. Run the setup script and follow the instructions from there.
   * (Clone the repo
   *  run yarn
   *  cd packages/constructs/entra-id-application
   *  yarn setup
   *    --clientId <client id aka app id>
   *    --clientSecret <client secret value>
   *    --tenantId <your tenant id>
   *    --keyId <secret id>
   * )
   */
  bootstrapClientSecret: Secret.fromSecretCompleteArn(stack, 'bootstrap-client-secret', 'bootstrap-client-secret-arn'),
  config: {
    displayName: 'My Application',
    requiredResourceAccess: [
      {
        resourceAppId: '00000003-0000-0000-c000-000000000000', // microsoft graph
        resourceAccess: [
          {
            id: '14dad69e-099b-42c9-810b-d002981feec1', // user: profile
            type: 'Scope',
          },
          {
            id: '37f7f235-527c-4136-accd-4a02d197296e', // user: openid
            type: 'Scope',
          },
          {
            id: '64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0', // user: email
            type: 'Scope',
          },
        ],
      },
    ],
    web: {
      redirectUris: ['https://example.org'],
    },
  },
})

const { secret } = entraApp.createKey(stack, 'key', {
  keyInfo: {
    displayName: 'api',
  },
  validFor: Duration.days(31),
})

new CfnOutput(stack, 'appId', {
  value: entraApp.getAttString('appId'),
})

new CfnOutput(stack, 'client-secret-arn', {
  value: secret.secretArn,
})

// This is the client secret (don't do this)
new CfnOutput(stack, 'client-secret-secretText', {
  value: secret.secretValueFromJson('secretText').toString(),
})
```
'''
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
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
import reapit_cdk.replicated_key as _reapit_cdk_replicated_key_c62599cb


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.CreateKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_info": "keyInfo",
        "valid_for": "validFor",
        "removal_policy": "removalPolicy",
        "replica_regions": "replicaRegions",
        "replicated_key": "replicatedKey",
    },
)
class CreateKeyProps:
    def __init__(
        self,
        *,
        key_info: typing.Union["KeyCreationInfo", typing.Dict[builtins.str, typing.Any]],
        valid_for: _aws_cdk_ceddda9d.Duration,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replicated_key: typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey] = None,
    ) -> None:
        '''
        :param key_info: 
        :param valid_for: 
        :param removal_policy: 
        :param replica_regions: 
        :param replicated_key: 
        '''
        if isinstance(key_info, dict):
            key_info = KeyCreationInfo(**key_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc76244475382ef47e0e7fc7c850bd242d09694f5b63f310d38a8e534cb91a6)
            check_type(argname="argument key_info", value=key_info, expected_type=type_hints["key_info"])
            check_type(argname="argument valid_for", value=valid_for, expected_type=type_hints["valid_for"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument replicated_key", value=replicated_key, expected_type=type_hints["replicated_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_info": key_info,
            "valid_for": valid_for,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if replicated_key is not None:
            self._values["replicated_key"] = replicated_key

    @builtins.property
    def key_info(self) -> "KeyCreationInfo":
        result = self._values.get("key_info")
        assert result is not None, "Required property 'key_info' is missing"
        return typing.cast("KeyCreationInfo", result)

    @builtins.property
    def valid_for(self) -> _aws_cdk_ceddda9d.Duration:
        result = self._values.get("valid_for")
        assert result is not None, "Required property 'valid_for' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def replica_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replicated_key(
        self,
    ) -> typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey]:
        result = self._values.get("replicated_key")
        return typing.cast(typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.Entity",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class Entity:
    def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba6f7c6967d8878b283dd8392186ed965838103c2dac52f273b531c39008cf)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Entity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EntraIDApplication(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@reapit-cdk/entra-id-application.EntraIDApplication",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bootstrap_client_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        config: typing.Union["Application", typing.Dict[builtins.str, typing.Any]],
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bootstrap_client_secret: 
        :param config: 
        :param removal_policy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887fae4761f108819051c2d84c7db9843ed02543e64312502a57548ab7d74ae0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EntraIDApplicationProps(
            bootstrap_client_secret=bootstrap_client_secret,
            config=config,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createKey")
    def create_key(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        key_info: typing.Union["KeyCreationInfo", typing.Dict[builtins.str, typing.Any]],
        valid_for: _aws_cdk_ceddda9d.Duration,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replicated_key: typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey] = None,
    ) -> "EntraIDApplicationKey":
        '''
        :param scope: -
        :param id: -
        :param key_info: 
        :param valid_for: 
        :param removal_policy: 
        :param replica_regions: 
        :param replicated_key: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a12d2c352659d4799f69ba893a50f643a83bd3e087f005963093e53ef33785)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CreateKeyProps(
            key_info=key_info,
            valid_for=valid_for,
            removal_policy=removal_policy,
            replica_regions=replica_regions,
            replicated_key=replicated_key,
        )

        return typing.cast("EntraIDApplicationKey", jsii.invoke(self, "createKey", [scope, id, props]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attr: builtins.str) -> builtins.str:
        '''
        :param attr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4d4b673368f602df2c9fe66e388f111f5d9838377d4bbb0e20f4000957764e)
            check_type(argname="argument attr", value=attr, expected_type=type_hints["attr"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attr]))


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.EntraIDApplicationKey",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "end_date_time": "endDateTime",
        "hint": "hint",
        "key_id": "keyId",
        "secret": "secret",
        "start_date_time": "startDateTime",
    },
)
class EntraIDApplicationKey:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        end_date_time: builtins.str,
        hint: builtins.str,
        key_id: builtins.str,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.Secret,
        start_date_time: builtins.str,
    ) -> None:
        '''
        :param display_name: 
        :param end_date_time: 
        :param hint: 
        :param key_id: 
        :param secret: 
        :param start_date_time: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bb134ab620c7d0e68385b5da56f3cad73c59eac78d8a1f92533781512f1f46)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument end_date_time", value=end_date_time, expected_type=type_hints["end_date_time"])
            check_type(argname="argument hint", value=hint, expected_type=type_hints["hint"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument start_date_time", value=start_date_time, expected_type=type_hints["start_date_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "end_date_time": end_date_time,
            "hint": hint,
            "key_id": key_id,
            "secret": secret,
            "start_date_time": start_date_time,
        }

    @builtins.property
    def display_name(self) -> builtins.str:
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_date_time(self) -> builtins.str:
        result = self._values.get("end_date_time")
        assert result is not None, "Required property 'end_date_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hint(self) -> builtins.str:
        result = self._values.get("hint")
        assert result is not None, "Required property 'hint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_id(self) -> builtins.str:
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, result)

    @builtins.property
    def start_date_time(self) -> builtins.str:
        result = self._values.get("start_date_time")
        assert result is not None, "Required property 'start_date_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EntraIDApplicationKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.EntraIDApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "bootstrap_client_secret": "bootstrapClientSecret",
        "config": "config",
        "removal_policy": "removalPolicy",
    },
)
class EntraIDApplicationProps:
    def __init__(
        self,
        *,
        bootstrap_client_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        config: typing.Union["Application", typing.Dict[builtins.str, typing.Any]],
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param bootstrap_client_secret: 
        :param config: 
        :param removal_policy: 
        '''
        if isinstance(config, dict):
            config = Application(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e23c38fba80c9e9c01d4c00546a649e0caaf339b292b8705ca4d82f6cb1867f)
            check_type(argname="argument bootstrap_client_secret", value=bootstrap_client_secret, expected_type=type_hints["bootstrap_client_secret"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bootstrap_client_secret": bootstrap_client_secret,
            "config": config,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def bootstrap_client_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        result = self._values.get("bootstrap_client_secret")
        assert result is not None, "Required property 'bootstrap_client_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def config(self) -> "Application":
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("Application", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EntraIDApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EntraSelfRotatingKey(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@reapit-cdk/entra-id-application.EntraSelfRotatingKey",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcfb68fcd54a3a509d96403f528a3faae41183ea499109afd021643755a3b0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EntraSelfRotatingKeyProps(secret=secret)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.EntraSelfRotatingKeyProps",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class EntraSelfRotatingKeyProps:
    def __init__(self, *, secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret) -> None:
        '''
        :param secret: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6787e0d1e602cd3d870aaf8ee3544db7e63f09908e4cd1f04adcadb0a33d003c)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EntraSelfRotatingKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.KeyCreationInfo",
    jsii_struct_bases=[],
    name_mapping={"display_name": "displayName", "hint": "hint"},
)
class KeyCreationInfo:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        hint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: 
        :param hint: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12c03e560140c0dcd5c41e681df882c1cf1669100b74930165179f8edc993ec)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument hint", value=hint, expected_type=type_hints["hint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if hint is not None:
            self._values["hint"] = hint

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyCreationInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.DirectoryObject",
    jsii_struct_bases=[Entity],
    name_mapping={"id": "id", "deleted_date_time": "deletedDateTime"},
)
class DirectoryObject(Entity):
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        deleted_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: 
        :param deleted_date_time: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19705685e7dad09b4a121294ba5276290b43e0f5454d3a97aab28db418ab3866)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument deleted_date_time", value=deleted_date_time, expected_type=type_hints["deleted_date_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if deleted_date_time is not None:
            self._values["deleted_date_time"] = deleted_date_time

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deleted_date_time(self) -> typing.Optional[builtins.str]:
        result = self._values.get("deleted_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectoryObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@reapit-cdk/entra-id-application.Application",
    jsii_struct_bases=[DirectoryObject],
    name_mapping={
        "id": "id",
        "deleted_date_time": "deletedDateTime",
        "add_ins": "addIns",
        "api": "api",
        "app_id": "appId",
        "application_template_id": "applicationTemplateId",
        "app_management_policies": "appManagementPolicies",
        "app_roles": "appRoles",
        "certification": "certification",
        "created_date_time": "createdDateTime",
        "created_on_behalf_of": "createdOnBehalfOf",
        "default_redirect_uri": "defaultRedirectUri",
        "description": "description",
        "disabled_by_microsoft_status": "disabledByMicrosoftStatus",
        "display_name": "displayName",
        "extension_properties": "extensionProperties",
        "federated_identity_credentials": "federatedIdentityCredentials",
        "group_membership_claims": "groupMembershipClaims",
        "home_realm_discovery_policies": "homeRealmDiscoveryPolicies",
        "identifier_uris": "identifierUris",
        "info": "info",
        "is_device_only_auth_supported": "isDeviceOnlyAuthSupported",
        "is_fallback_public_client": "isFallbackPublicClient",
        "key_credentials": "keyCredentials",
        "logo": "logo",
        "notes": "notes",
        "oauth2_require_post_response": "oauth2RequirePostResponse",
        "optional_claims": "optionalClaims",
        "owners": "owners",
        "parental_control_settings": "parentalControlSettings",
        "password_credentials": "passwordCredentials",
        "public_client": "publicClient",
        "publisher_domain": "publisherDomain",
        "request_signature_verification": "requestSignatureVerification",
        "required_resource_access": "requiredResourceAccess",
        "saml_metadata_url": "samlMetadataUrl",
        "service_management_reference": "serviceManagementReference",
        "sign_in_audience": "signInAudience",
        "spa": "spa",
        "synchronization": "synchronization",
        "tags": "tags",
        "token_encryption_key_id": "tokenEncryptionKeyId",
        "token_issuance_policies": "tokenIssuancePolicies",
        "token_lifetime_policies": "tokenLifetimePolicies",
        "verified_publisher": "verifiedPublisher",
        "web": "web",
    },
)
class Application(DirectoryObject):
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        deleted_date_time: typing.Optional[builtins.str] = None,
        add_ins: typing.Optional[typing.Sequence[typing.Any]] = None,
        api: typing.Any = None,
        app_id: typing.Optional[builtins.str] = None,
        application_template_id: typing.Optional[builtins.str] = None,
        app_management_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
        app_roles: typing.Optional[typing.Sequence[typing.Any]] = None,
        certification: typing.Any = None,
        created_date_time: typing.Optional[builtins.str] = None,
        created_on_behalf_of: typing.Optional[typing.Union[DirectoryObject, typing.Dict[builtins.str, typing.Any]]] = None,
        default_redirect_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disabled_by_microsoft_status: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        extension_properties: typing.Optional[typing.Sequence[typing.Any]] = None,
        federated_identity_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
        group_membership_claims: typing.Optional[builtins.str] = None,
        home_realm_discovery_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
        identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        info: typing.Any = None,
        is_device_only_auth_supported: typing.Optional[builtins.bool] = None,
        is_fallback_public_client: typing.Optional[builtins.bool] = None,
        key_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
        logo: typing.Any = None,
        notes: typing.Optional[builtins.str] = None,
        oauth2_require_post_response: typing.Optional[builtins.bool] = None,
        optional_claims: typing.Any = None,
        owners: typing.Optional[typing.Sequence[typing.Union[DirectoryObject, typing.Dict[builtins.str, typing.Any]]]] = None,
        parental_control_settings: typing.Any = None,
        password_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
        public_client: typing.Any = None,
        publisher_domain: typing.Optional[builtins.str] = None,
        request_signature_verification: typing.Any = None,
        required_resource_access: typing.Optional[typing.Sequence[typing.Any]] = None,
        saml_metadata_url: typing.Optional[builtins.str] = None,
        service_management_reference: typing.Optional[builtins.str] = None,
        sign_in_audience: typing.Optional[builtins.str] = None,
        spa: typing.Any = None,
        synchronization: typing.Any = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        token_encryption_key_id: typing.Optional[builtins.str] = None,
        token_issuance_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
        token_lifetime_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
        verified_publisher: typing.Any = None,
        web: typing.Any = None,
    ) -> None:
        '''
        :param id: 
        :param deleted_date_time: 
        :param add_ins: Defines custom behavior that a consuming service can use to call an app in specific contexts. For example, applications that can render file streams may set the addIns property for its 'FileHandler' functionality. This will let services like Office 365 call the application in the context of a document the user is working on.
        :param api: 
        :param app_id: The unique identifier for the application that is assigned to an application by Azure AD. Not nullable. Read-only. Supports $filter (eq).
        :param application_template_id: 
        :param app_management_policies: 
        :param app_roles: The collection of roles defined for the application. With app role assignments, these roles can be assigned to users, groups, or service principals associated with other applications. Not nullable.
        :param certification: 
        :param created_date_time: The date and time the application was registered. The DateTimeOffset type represents date and time information using ISO 8601 format and is always in UTC time. For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z. Read-only. Supports $filter (eq, ne, not, ge, le, in, and eq on null values) and $orderBy.
        :param created_on_behalf_of: 
        :param default_redirect_uri: 
        :param description: Free text field to provide a description of the application object to end users. The maximum allowed size is 1024 characters. Supports $filter (eq, ne, not, ge, le, startsWith) and $search.
        :param disabled_by_microsoft_status: Specifies whether Microsoft has disabled the registered application. Possible values are: null (default value), NotDisabled, and DisabledDueToViolationOfServicesAgreement (reasons may include suspicious, abusive, or malicious activity, or a violation of the Microsoft Services Agreement). Supports $filter (eq, ne, not).
        :param display_name: The display name for the application. Supports $filter (eq, ne, not, ge, le, in, startsWith, and eq on null values), $search, and $orderBy.
        :param extension_properties: 
        :param federated_identity_credentials: 
        :param group_membership_claims: Configures the groups claim issued in a user or OAuth 2.0 access token that the application expects. To set this attribute, use one of the following valid string values: None, SecurityGroup (for security groups and Azure AD roles), All (this gets all of the security groups, distribution groups, and Azure AD directory roles that the signed-in user is a member of).
        :param home_realm_discovery_policies: 
        :param identifier_uris: Also known as App ID URI, this value is set when an application is used as a resource app. The identifierUris acts as the prefix for the scopes you'll reference in your API's code, and it must be globally unique. You can use the default value provided, which is in the form api://&lt;application-client-id&gt;, or specify a more readable URI like https://contoso.com/api. For more information on valid identifierUris patterns and best practices, see Azure AD application registration security best practices. Not nullable. Supports $filter (eq, ne, ge, le, startsWith).
        :param info: Basic profile information of the application such as app's marketing, support, terms of service and privacy statement URLs. The terms of service and privacy statement are surfaced to users through the user consent experience. For more info, see How to: Add Terms of service and privacy statement for registered Azure AD apps. Supports $filter (eq, ne, not, ge, le, and eq on null values).
        :param is_device_only_auth_supported: 
        :param is_fallback_public_client: Specifies the fallback application type as public client, such as an installed application running on a mobile device. The default value is false which means the fallback application type is confidential client such as a web app. There are certain scenarios where Azure AD cannot determine the client application type. For example, the ROPC flow where it is configured without specifying a redirect URI. In those cases Azure AD interprets the application type based on the value of this property.
        :param key_credentials: 
        :param logo: 
        :param notes: 
        :param oauth2_require_post_response: 
        :param optional_claims: Application developers can configure optional claims in their Azure AD applications to specify the claims that are sent to their application by the Microsoft security token service. For more information, see How to: Provide optional claims to your app.
        :param owners: Directory objects that are owners of the application. Read-only. Nullable. Supports $expand and $filter (/$count eq 0, /$count ne 0, /$count eq 1, /$count ne 1).
        :param parental_control_settings: 
        :param password_credentials: 
        :param public_client: 
        :param publisher_domain: The verified publisher domain for the application. Read-only. For more information, see How to: Configure an application's publisher domain. Supports $filter (eq, ne, ge, le, startsWith).
        :param request_signature_verification: 
        :param required_resource_access: Specifies the resources that the application needs to access. This property also specifies the set of delegated permissions and application roles that it needs for each of those resources. This configuration of access to the required resources drives the consent experience. No more than 50 resource services (APIs) can be configured. Beginning mid-October 2021, the total number of required permissions must not exceed 400. For more information, see Limits on requested permissions per app. Not nullable. Supports $filter (eq, not, ge, le).
        :param saml_metadata_url: The URL where the service exposes SAML metadata for federation. This property is valid only for single-tenant applications. Nullable.
        :param service_management_reference: 
        :param sign_in_audience: Specifies the Microsoft accounts that are supported for the current application. The possible values are: AzureADMyOrg, AzureADMultipleOrgs, AzureADandPersonalMicrosoftAccount (default), and PersonalMicrosoftAccount. See more in the table. The value of this object also limits the number of permissions an app can request. For more information, see Limits on requested permissions per app. The value for this property has implications on other app object properties. As a result, if you change this property, you may need to change other properties first. For more information, see Validation differences for signInAudience.Supports $filter (eq, ne, not).
        :param spa: Specifies settings for a single-page application, including sign out URLs and redirect URIs for authorization codes and access tokens.
        :param synchronization: Represents the capability for Azure Active Directory (Azure AD) identity synchronization through the Microsoft Graph API.
        :param tags: Custom strings that can be used to categorize and identify the application. Not nullable. Strings added here will also appear in the tags property of any associated service principals.Supports $filter (eq, not, ge, le, startsWith) and $search.
        :param token_encryption_key_id: Specifies the keyId of a public key from the keyCredentials collection. When configured, Azure AD encrypts all the tokens it emits by using the key this property points to. The application code that receives the encrypted token must use the matching private key to decrypt the token before it can be used for the signed-in user.
        :param token_issuance_policies: 
        :param token_lifetime_policies: 
        :param verified_publisher: Specifies the verified publisher of the application. For more information about how publisher verification helps support application security, trustworthiness, and compliance, see Publisher verification.
        :param web: 
        '''
        if isinstance(created_on_behalf_of, dict):
            created_on_behalf_of = DirectoryObject(**created_on_behalf_of)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9051f0d0c2580661bb965ead2953ce3de7ef5e45ea099fc8085b24866bea3ef0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument deleted_date_time", value=deleted_date_time, expected_type=type_hints["deleted_date_time"])
            check_type(argname="argument add_ins", value=add_ins, expected_type=type_hints["add_ins"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument application_template_id", value=application_template_id, expected_type=type_hints["application_template_id"])
            check_type(argname="argument app_management_policies", value=app_management_policies, expected_type=type_hints["app_management_policies"])
            check_type(argname="argument app_roles", value=app_roles, expected_type=type_hints["app_roles"])
            check_type(argname="argument certification", value=certification, expected_type=type_hints["certification"])
            check_type(argname="argument created_date_time", value=created_date_time, expected_type=type_hints["created_date_time"])
            check_type(argname="argument created_on_behalf_of", value=created_on_behalf_of, expected_type=type_hints["created_on_behalf_of"])
            check_type(argname="argument default_redirect_uri", value=default_redirect_uri, expected_type=type_hints["default_redirect_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled_by_microsoft_status", value=disabled_by_microsoft_status, expected_type=type_hints["disabled_by_microsoft_status"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument extension_properties", value=extension_properties, expected_type=type_hints["extension_properties"])
            check_type(argname="argument federated_identity_credentials", value=federated_identity_credentials, expected_type=type_hints["federated_identity_credentials"])
            check_type(argname="argument group_membership_claims", value=group_membership_claims, expected_type=type_hints["group_membership_claims"])
            check_type(argname="argument home_realm_discovery_policies", value=home_realm_discovery_policies, expected_type=type_hints["home_realm_discovery_policies"])
            check_type(argname="argument identifier_uris", value=identifier_uris, expected_type=type_hints["identifier_uris"])
            check_type(argname="argument info", value=info, expected_type=type_hints["info"])
            check_type(argname="argument is_device_only_auth_supported", value=is_device_only_auth_supported, expected_type=type_hints["is_device_only_auth_supported"])
            check_type(argname="argument is_fallback_public_client", value=is_fallback_public_client, expected_type=type_hints["is_fallback_public_client"])
            check_type(argname="argument key_credentials", value=key_credentials, expected_type=type_hints["key_credentials"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument oauth2_require_post_response", value=oauth2_require_post_response, expected_type=type_hints["oauth2_require_post_response"])
            check_type(argname="argument optional_claims", value=optional_claims, expected_type=type_hints["optional_claims"])
            check_type(argname="argument owners", value=owners, expected_type=type_hints["owners"])
            check_type(argname="argument parental_control_settings", value=parental_control_settings, expected_type=type_hints["parental_control_settings"])
            check_type(argname="argument password_credentials", value=password_credentials, expected_type=type_hints["password_credentials"])
            check_type(argname="argument public_client", value=public_client, expected_type=type_hints["public_client"])
            check_type(argname="argument publisher_domain", value=publisher_domain, expected_type=type_hints["publisher_domain"])
            check_type(argname="argument request_signature_verification", value=request_signature_verification, expected_type=type_hints["request_signature_verification"])
            check_type(argname="argument required_resource_access", value=required_resource_access, expected_type=type_hints["required_resource_access"])
            check_type(argname="argument saml_metadata_url", value=saml_metadata_url, expected_type=type_hints["saml_metadata_url"])
            check_type(argname="argument service_management_reference", value=service_management_reference, expected_type=type_hints["service_management_reference"])
            check_type(argname="argument sign_in_audience", value=sign_in_audience, expected_type=type_hints["sign_in_audience"])
            check_type(argname="argument spa", value=spa, expected_type=type_hints["spa"])
            check_type(argname="argument synchronization", value=synchronization, expected_type=type_hints["synchronization"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument token_encryption_key_id", value=token_encryption_key_id, expected_type=type_hints["token_encryption_key_id"])
            check_type(argname="argument token_issuance_policies", value=token_issuance_policies, expected_type=type_hints["token_issuance_policies"])
            check_type(argname="argument token_lifetime_policies", value=token_lifetime_policies, expected_type=type_hints["token_lifetime_policies"])
            check_type(argname="argument verified_publisher", value=verified_publisher, expected_type=type_hints["verified_publisher"])
            check_type(argname="argument web", value=web, expected_type=type_hints["web"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if deleted_date_time is not None:
            self._values["deleted_date_time"] = deleted_date_time
        if add_ins is not None:
            self._values["add_ins"] = add_ins
        if api is not None:
            self._values["api"] = api
        if app_id is not None:
            self._values["app_id"] = app_id
        if application_template_id is not None:
            self._values["application_template_id"] = application_template_id
        if app_management_policies is not None:
            self._values["app_management_policies"] = app_management_policies
        if app_roles is not None:
            self._values["app_roles"] = app_roles
        if certification is not None:
            self._values["certification"] = certification
        if created_date_time is not None:
            self._values["created_date_time"] = created_date_time
        if created_on_behalf_of is not None:
            self._values["created_on_behalf_of"] = created_on_behalf_of
        if default_redirect_uri is not None:
            self._values["default_redirect_uri"] = default_redirect_uri
        if description is not None:
            self._values["description"] = description
        if disabled_by_microsoft_status is not None:
            self._values["disabled_by_microsoft_status"] = disabled_by_microsoft_status
        if display_name is not None:
            self._values["display_name"] = display_name
        if extension_properties is not None:
            self._values["extension_properties"] = extension_properties
        if federated_identity_credentials is not None:
            self._values["federated_identity_credentials"] = federated_identity_credentials
        if group_membership_claims is not None:
            self._values["group_membership_claims"] = group_membership_claims
        if home_realm_discovery_policies is not None:
            self._values["home_realm_discovery_policies"] = home_realm_discovery_policies
        if identifier_uris is not None:
            self._values["identifier_uris"] = identifier_uris
        if info is not None:
            self._values["info"] = info
        if is_device_only_auth_supported is not None:
            self._values["is_device_only_auth_supported"] = is_device_only_auth_supported
        if is_fallback_public_client is not None:
            self._values["is_fallback_public_client"] = is_fallback_public_client
        if key_credentials is not None:
            self._values["key_credentials"] = key_credentials
        if logo is not None:
            self._values["logo"] = logo
        if notes is not None:
            self._values["notes"] = notes
        if oauth2_require_post_response is not None:
            self._values["oauth2_require_post_response"] = oauth2_require_post_response
        if optional_claims is not None:
            self._values["optional_claims"] = optional_claims
        if owners is not None:
            self._values["owners"] = owners
        if parental_control_settings is not None:
            self._values["parental_control_settings"] = parental_control_settings
        if password_credentials is not None:
            self._values["password_credentials"] = password_credentials
        if public_client is not None:
            self._values["public_client"] = public_client
        if publisher_domain is not None:
            self._values["publisher_domain"] = publisher_domain
        if request_signature_verification is not None:
            self._values["request_signature_verification"] = request_signature_verification
        if required_resource_access is not None:
            self._values["required_resource_access"] = required_resource_access
        if saml_metadata_url is not None:
            self._values["saml_metadata_url"] = saml_metadata_url
        if service_management_reference is not None:
            self._values["service_management_reference"] = service_management_reference
        if sign_in_audience is not None:
            self._values["sign_in_audience"] = sign_in_audience
        if spa is not None:
            self._values["spa"] = spa
        if synchronization is not None:
            self._values["synchronization"] = synchronization
        if tags is not None:
            self._values["tags"] = tags
        if token_encryption_key_id is not None:
            self._values["token_encryption_key_id"] = token_encryption_key_id
        if token_issuance_policies is not None:
            self._values["token_issuance_policies"] = token_issuance_policies
        if token_lifetime_policies is not None:
            self._values["token_lifetime_policies"] = token_lifetime_policies
        if verified_publisher is not None:
            self._values["verified_publisher"] = verified_publisher
        if web is not None:
            self._values["web"] = web

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deleted_date_time(self) -> typing.Optional[builtins.str]:
        result = self._values.get("deleted_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def add_ins(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Defines custom behavior that a consuming service can use to call an app in specific contexts.

        For example, applications
        that can render file streams may set the addIns property for its 'FileHandler' functionality. This will let services
        like Office 365 call the application in the context of a document the user is working on.
        '''
        result = self._values.get("add_ins")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def api(self) -> typing.Any:
        result = self._values.get("api")
        return typing.cast(typing.Any, result)

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the application that is assigned to an application by Azure AD.

        Not nullable. Read-only.
        Supports $filter (eq).
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_template_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("application_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_management_policies(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("app_management_policies")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def app_roles(self) -> typing.Optional[typing.List[typing.Any]]:
        '''The collection of roles defined for the application.

        With app role assignments, these roles can be assigned to users,
        groups, or service principals associated with other applications. Not nullable.
        '''
        result = self._values.get("app_roles")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def certification(self) -> typing.Any:
        result = self._values.get("certification")
        return typing.cast(typing.Any, result)

    @builtins.property
    def created_date_time(self) -> typing.Optional[builtins.str]:
        '''The date and time the application was registered.

        The DateTimeOffset type represents date and time information using
        ISO 8601 format and is always in UTC time. For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z. Read-only.
        Supports $filter (eq, ne, not, ge, le, in, and eq on null values) and $orderBy.
        '''
        result = self._values.get("created_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_on_behalf_of(self) -> typing.Optional[DirectoryObject]:
        result = self._values.get("created_on_behalf_of")
        return typing.cast(typing.Optional[DirectoryObject], result)

    @builtins.property
    def default_redirect_uri(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default_redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free text field to provide a description of the application object to end users.

        The maximum allowed size is 1024
        characters. Supports $filter (eq, ne, not, ge, le, startsWith) and $search.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled_by_microsoft_status(self) -> typing.Optional[builtins.str]:
        '''Specifies whether Microsoft has disabled the registered application.

        Possible values are: null (default value),
        NotDisabled, and DisabledDueToViolationOfServicesAgreement (reasons may include suspicious, abusive, or malicious
        activity, or a violation of the Microsoft Services Agreement). Supports $filter (eq, ne, not).
        '''
        result = self._values.get("disabled_by_microsoft_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for the application.

        Supports $filter (eq, ne, not, ge, le, in, startsWith, and eq on null values),
        $search, and $orderBy.
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension_properties(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("extension_properties")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def federated_identity_credentials(
        self,
    ) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("federated_identity_credentials")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def group_membership_claims(self) -> typing.Optional[builtins.str]:
        '''Configures the groups claim issued in a user or OAuth 2.0 access token that the application expects. To set this attribute, use one of the following valid string values: None, SecurityGroup (for security groups and Azure AD roles), All (this gets all of the security groups, distribution groups, and Azure AD directory roles that the signed-in user is a member of).'''
        result = self._values.get("group_membership_claims")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_realm_discovery_policies(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("home_realm_discovery_policies")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def identifier_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Also known as App ID URI, this value is set when an application is used as a resource app.

        The identifierUris acts as
        the prefix for the scopes you'll reference in your API's code, and it must be globally unique. You can use the default
        value provided, which is in the form api://<application-client-id>, or specify a more readable URI like
        https://contoso.com/api. For more information on valid identifierUris patterns and best practices, see Azure AD
        application registration security best practices. Not nullable. Supports $filter (eq, ne, ge, le, startsWith).
        '''
        result = self._values.get("identifier_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def info(self) -> typing.Any:
        '''Basic profile information of the application such as app's marketing, support, terms of service and privacy statement URLs.

        The terms of service and privacy statement are surfaced to users through the user consent experience. For more
        info, see How to: Add Terms of service and privacy statement for registered Azure AD apps. Supports $filter (eq, ne,
        not, ge, le, and eq on null values).
        '''
        result = self._values.get("info")
        return typing.cast(typing.Any, result)

    @builtins.property
    def is_device_only_auth_supported(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("is_device_only_auth_supported")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_fallback_public_client(self) -> typing.Optional[builtins.bool]:
        '''Specifies the fallback application type as public client, such as an installed application running on a mobile device.

        The default value is false which means the fallback application type is confidential client such as a web app. There
        are certain scenarios where Azure AD cannot determine the client application type. For example, the ROPC flow where it
        is configured without specifying a redirect URI. In those cases Azure AD interprets the application type based on the
        value of this property.
        '''
        result = self._values.get("is_fallback_public_client")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_credentials(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("key_credentials")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def logo(self) -> typing.Any:
        result = self._values.get("logo")
        return typing.cast(typing.Any, result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_require_post_response(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("oauth2_require_post_response")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def optional_claims(self) -> typing.Any:
        '''Application developers can configure optional claims in their Azure AD applications to specify the claims that are sent to their application by the Microsoft security token service.

        For more information, see How to: Provide optional claims
        to your app.
        '''
        result = self._values.get("optional_claims")
        return typing.cast(typing.Any, result)

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[DirectoryObject]]:
        '''Directory objects that are owners of the application.

        Read-only. Nullable. Supports $expand and $filter (/$count eq 0,
        /$count ne 0, /$count eq 1, /$count ne 1).
        '''
        result = self._values.get("owners")
        return typing.cast(typing.Optional[typing.List[DirectoryObject]], result)

    @builtins.property
    def parental_control_settings(self) -> typing.Any:
        result = self._values.get("parental_control_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def password_credentials(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("password_credentials")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def public_client(self) -> typing.Any:
        result = self._values.get("public_client")
        return typing.cast(typing.Any, result)

    @builtins.property
    def publisher_domain(self) -> typing.Optional[builtins.str]:
        '''The verified publisher domain for the application.

        Read-only. For more information, see How to: Configure an
        application's publisher domain. Supports $filter (eq, ne, ge, le, startsWith).
        '''
        result = self._values.get("publisher_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_verification(self) -> typing.Any:
        result = self._values.get("request_signature_verification")
        return typing.cast(typing.Any, result)

    @builtins.property
    def required_resource_access(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Specifies the resources that the application needs to access.

        This property also specifies the set of delegated
        permissions and application roles that it needs for each of those resources. This configuration of access to the
        required resources drives the consent experience. No more than 50 resource services (APIs) can be configured. Beginning
        mid-October 2021, the total number of required permissions must not exceed 400. For more information, see Limits on
        requested permissions per app. Not nullable. Supports $filter (eq, not, ge, le).
        '''
        result = self._values.get("required_resource_access")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def saml_metadata_url(self) -> typing.Optional[builtins.str]:
        '''The URL where the service exposes SAML metadata for federation.

        This property is valid only for single-tenant
        applications. Nullable.
        '''
        result = self._values.get("saml_metadata_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_management_reference(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_management_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in_audience(self) -> typing.Optional[builtins.str]:
        '''Specifies the Microsoft accounts that are supported for the current application.

        The possible values are: AzureADMyOrg,
        AzureADMultipleOrgs, AzureADandPersonalMicrosoftAccount (default), and PersonalMicrosoftAccount. See more in the table.
        The value of this object also limits the number of permissions an app can request. For more information, see Limits on
        requested permissions per app. The value for this property has implications on other app object properties. As a
        result, if you change this property, you may need to change other properties first. For more information, see
        Validation differences for signInAudience.Supports $filter (eq, ne, not).
        '''
        result = self._values.get("sign_in_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spa(self) -> typing.Any:
        '''Specifies settings for a single-page application, including sign out URLs and redirect URIs for authorization codes and access tokens.'''
        result = self._values.get("spa")
        return typing.cast(typing.Any, result)

    @builtins.property
    def synchronization(self) -> typing.Any:
        '''Represents the capability for Azure Active Directory (Azure AD) identity synchronization through the Microsoft Graph API.'''
        result = self._values.get("synchronization")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom strings that can be used to categorize and identify the application.

        Not nullable. Strings added here will also
        appear in the tags property of any associated service principals.Supports $filter (eq, not, ge, le, startsWith) and
        $search.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token_encryption_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the keyId of a public key from the keyCredentials collection.

        When configured, Azure AD encrypts all the
        tokens it emits by using the key this property points to. The application code that receives the encrypted token must
        use the matching private key to decrypt the token before it can be used for the signed-in user.
        '''
        result = self._values.get("token_encryption_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_issuance_policies(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("token_issuance_policies")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def token_lifetime_policies(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("token_lifetime_policies")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def verified_publisher(self) -> typing.Any:
        '''Specifies the verified publisher of the application.

        For more information about how publisher verification helps
        support application security, trustworthiness, and compliance, see Publisher verification.
        '''
        result = self._values.get("verified_publisher")
        return typing.cast(typing.Any, result)

    @builtins.property
    def web(self) -> typing.Any:
        result = self._values.get("web")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Application(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Application",
    "CreateKeyProps",
    "DirectoryObject",
    "Entity",
    "EntraIDApplication",
    "EntraIDApplicationKey",
    "EntraIDApplicationProps",
    "EntraSelfRotatingKey",
    "EntraSelfRotatingKeyProps",
    "KeyCreationInfo",
]

publication.publish()

def _typecheckingstub__dfc76244475382ef47e0e7fc7c850bd242d09694f5b63f310d38a8e534cb91a6(
    *,
    key_info: typing.Union[KeyCreationInfo, typing.Dict[builtins.str, typing.Any]],
    valid_for: _aws_cdk_ceddda9d.Duration,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replicated_key: typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba6f7c6967d8878b283dd8392186ed965838103c2dac52f273b531c39008cf(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887fae4761f108819051c2d84c7db9843ed02543e64312502a57548ab7d74ae0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bootstrap_client_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    config: typing.Union[Application, typing.Dict[builtins.str, typing.Any]],
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a12d2c352659d4799f69ba893a50f643a83bd3e087f005963093e53ef33785(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    key_info: typing.Union[KeyCreationInfo, typing.Dict[builtins.str, typing.Any]],
    valid_for: _aws_cdk_ceddda9d.Duration,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    replicated_key: typing.Optional[_reapit_cdk_replicated_key_c62599cb.ReplicatedKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4d4b673368f602df2c9fe66e388f111f5d9838377d4bbb0e20f4000957764e(
    attr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bb134ab620c7d0e68385b5da56f3cad73c59eac78d8a1f92533781512f1f46(
    *,
    display_name: builtins.str,
    end_date_time: builtins.str,
    hint: builtins.str,
    key_id: builtins.str,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.Secret,
    start_date_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e23c38fba80c9e9c01d4c00546a649e0caaf339b292b8705ca4d82f6cb1867f(
    *,
    bootstrap_client_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    config: typing.Union[Application, typing.Dict[builtins.str, typing.Any]],
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcfb68fcd54a3a509d96403f528a3faae41183ea499109afd021643755a3b0a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6787e0d1e602cd3d870aaf8ee3544db7e63f09908e4cd1f04adcadb0a33d003c(
    *,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12c03e560140c0dcd5c41e681df882c1cf1669100b74930165179f8edc993ec(
    *,
    display_name: typing.Optional[builtins.str] = None,
    hint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19705685e7dad09b4a121294ba5276290b43e0f5454d3a97aab28db418ab3866(
    *,
    id: typing.Optional[builtins.str] = None,
    deleted_date_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9051f0d0c2580661bb965ead2953ce3de7ef5e45ea099fc8085b24866bea3ef0(
    *,
    id: typing.Optional[builtins.str] = None,
    deleted_date_time: typing.Optional[builtins.str] = None,
    add_ins: typing.Optional[typing.Sequence[typing.Any]] = None,
    api: typing.Any = None,
    app_id: typing.Optional[builtins.str] = None,
    application_template_id: typing.Optional[builtins.str] = None,
    app_management_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
    app_roles: typing.Optional[typing.Sequence[typing.Any]] = None,
    certification: typing.Any = None,
    created_date_time: typing.Optional[builtins.str] = None,
    created_on_behalf_of: typing.Optional[typing.Union[DirectoryObject, typing.Dict[builtins.str, typing.Any]]] = None,
    default_redirect_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disabled_by_microsoft_status: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    extension_properties: typing.Optional[typing.Sequence[typing.Any]] = None,
    federated_identity_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
    group_membership_claims: typing.Optional[builtins.str] = None,
    home_realm_discovery_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
    identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    info: typing.Any = None,
    is_device_only_auth_supported: typing.Optional[builtins.bool] = None,
    is_fallback_public_client: typing.Optional[builtins.bool] = None,
    key_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
    logo: typing.Any = None,
    notes: typing.Optional[builtins.str] = None,
    oauth2_require_post_response: typing.Optional[builtins.bool] = None,
    optional_claims: typing.Any = None,
    owners: typing.Optional[typing.Sequence[typing.Union[DirectoryObject, typing.Dict[builtins.str, typing.Any]]]] = None,
    parental_control_settings: typing.Any = None,
    password_credentials: typing.Optional[typing.Sequence[typing.Any]] = None,
    public_client: typing.Any = None,
    publisher_domain: typing.Optional[builtins.str] = None,
    request_signature_verification: typing.Any = None,
    required_resource_access: typing.Optional[typing.Sequence[typing.Any]] = None,
    saml_metadata_url: typing.Optional[builtins.str] = None,
    service_management_reference: typing.Optional[builtins.str] = None,
    sign_in_audience: typing.Optional[builtins.str] = None,
    spa: typing.Any = None,
    synchronization: typing.Any = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_encryption_key_id: typing.Optional[builtins.str] = None,
    token_issuance_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
    token_lifetime_policies: typing.Optional[typing.Sequence[typing.Any]] = None,
    verified_publisher: typing.Any = None,
    web: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
