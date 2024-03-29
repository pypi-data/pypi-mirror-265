# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GroupMemberEntityIdsArgs', 'GroupMemberEntityIds']

@pulumi.input_type
class GroupMemberEntityIdsArgs:
    def __init__(__self__, *,
                 group_id: pulumi.Input[str],
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 member_entity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GroupMemberEntityIds resource.
        :param pulumi.Input[str] group_id: Group ID to assign member entities to.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] member_entity_ids: List of member entities that belong to the group
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        """
        pulumi.set(__self__, "group_id", group_id)
        if exclusive is not None:
            pulumi.set(__self__, "exclusive", exclusive)
        if member_entity_ids is not None:
            pulumi.set(__self__, "member_entity_ids", member_entity_ids)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        """
        Group ID to assign member entities to.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter
    def exclusive(self) -> Optional[pulumi.Input[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

    @exclusive.setter
    def exclusive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclusive", value)

    @property
    @pulumi.getter(name="memberEntityIds")
    def member_entity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of member entities that belong to the group
        """
        return pulumi.get(self, "member_entity_ids")

    @member_entity_ids.setter
    def member_entity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "member_entity_ids", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)


@pulumi.input_type
class _GroupMemberEntityIdsState:
    def __init__(__self__, *,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 member_entity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering GroupMemberEntityIds resources.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        :param pulumi.Input[str] group_id: Group ID to assign member entities to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] member_entity_ids: List of member entities that belong to the group
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        """
        if exclusive is not None:
            pulumi.set(__self__, "exclusive", exclusive)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if member_entity_ids is not None:
            pulumi.set(__self__, "member_entity_ids", member_entity_ids)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def exclusive(self) -> Optional[pulumi.Input[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

    @exclusive.setter
    def exclusive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclusive", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Group ID to assign member entities to.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="memberEntityIds")
    def member_entity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of member entities that belong to the group
        """
        return pulumi.get(self, "member_entity_ids")

    @member_entity_ids.setter
    def member_entity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "member_entity_ids", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)


class GroupMemberEntityIds(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 member_entity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages member entities for an Identity Group for Vault. The [Identity secrets engine](https://www.vaultproject.io/docs/secrets/identity/index.html) is the identity management solution for Vault.

        ## Example Usage

        ### Exclusive Member Entities

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        internal = vault.identity.Group("internal",
            type="internal",
            external_member_entity_ids=True,
            metadata={
                "version": "2",
            })
        user = vault.identity.Entity("user")
        members = vault.identity.GroupMemberEntityIds("members",
            exclusive=True,
            member_entity_ids=[user.id],
            group_id=internal.id)
        ```
        <!--End PulumiCodeChooser -->

        ### Non-exclusive Member Entities

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        internal = vault.identity.Group("internal",
            type="internal",
            external_member_entity_ids=True,
            metadata={
                "version": "2",
            })
        test_user = vault.identity.Entity("testUser")
        second_test_user = vault.identity.Entity("secondTestUser")
        dev_user = vault.identity.Entity("devUser")
        test = vault.identity.GroupMemberEntityIds("test",
            member_entity_ids=[
                test_user.id,
                second_test_user.id,
            ],
            exclusive=False,
            group_id=internal.id)
        others = vault.identity.GroupMemberEntityIds("others",
            member_entity_ids=[dev_user.id],
            exclusive=False,
            group_id=internal.id)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        :param pulumi.Input[str] group_id: Group ID to assign member entities to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] member_entity_ids: List of member entities that belong to the group
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GroupMemberEntityIdsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages member entities for an Identity Group for Vault. The [Identity secrets engine](https://www.vaultproject.io/docs/secrets/identity/index.html) is the identity management solution for Vault.

        ## Example Usage

        ### Exclusive Member Entities

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        internal = vault.identity.Group("internal",
            type="internal",
            external_member_entity_ids=True,
            metadata={
                "version": "2",
            })
        user = vault.identity.Entity("user")
        members = vault.identity.GroupMemberEntityIds("members",
            exclusive=True,
            member_entity_ids=[user.id],
            group_id=internal.id)
        ```
        <!--End PulumiCodeChooser -->

        ### Non-exclusive Member Entities

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        internal = vault.identity.Group("internal",
            type="internal",
            external_member_entity_ids=True,
            metadata={
                "version": "2",
            })
        test_user = vault.identity.Entity("testUser")
        second_test_user = vault.identity.Entity("secondTestUser")
        dev_user = vault.identity.Entity("devUser")
        test = vault.identity.GroupMemberEntityIds("test",
            member_entity_ids=[
                test_user.id,
                second_test_user.id,
            ],
            exclusive=False,
            group_id=internal.id)
        others = vault.identity.GroupMemberEntityIds("others",
            member_entity_ids=[dev_user.id],
            exclusive=False,
            group_id=internal.id)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param GroupMemberEntityIdsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupMemberEntityIdsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 member_entity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupMemberEntityIdsArgs.__new__(GroupMemberEntityIdsArgs)

            __props__.__dict__["exclusive"] = exclusive
            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            __props__.__dict__["member_entity_ids"] = member_entity_ids
            __props__.__dict__["namespace"] = namespace
        super(GroupMemberEntityIds, __self__).__init__(
            'vault:identity/groupMemberEntityIds:GroupMemberEntityIds',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            exclusive: Optional[pulumi.Input[bool]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            member_entity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            namespace: Optional[pulumi.Input[str]] = None) -> 'GroupMemberEntityIds':
        """
        Get an existing GroupMemberEntityIds resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        :param pulumi.Input[str] group_id: Group ID to assign member entities to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] member_entity_ids: List of member entities that belong to the group
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupMemberEntityIdsState.__new__(_GroupMemberEntityIdsState)

        __props__.__dict__["exclusive"] = exclusive
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["member_entity_ids"] = member_entity_ids
        __props__.__dict__["namespace"] = namespace
        return GroupMemberEntityIds(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def exclusive(self) -> pulumi.Output[Optional[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the member entities that belong to the group and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the member entities specified in the resource are present in the group. When destroying the resource, the resource will ensure that the member entities specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        Group ID to assign member entities to.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="memberEntityIds")
    def member_entity_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of member entities that belong to the group
        """
        return pulumi.get(self, "member_entity_ids")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

