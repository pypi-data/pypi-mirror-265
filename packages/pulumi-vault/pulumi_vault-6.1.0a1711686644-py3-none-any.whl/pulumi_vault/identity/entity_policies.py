# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EntityPoliciesArgs', 'EntityPolicies']

@pulumi.input_type
class EntityPoliciesArgs:
    def __init__(__self__, *,
                 entity_id: pulumi.Input[str],
                 policies: pulumi.Input[Sequence[pulumi.Input[str]]],
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EntityPolicies resource.
        :param pulumi.Input[str] entity_id: Entity ID to assign policies to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policies: List of policies to assign to the entity
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        """
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "policies", policies)
        if exclusive is not None:
            pulumi.set(__self__, "exclusive", exclusive)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> pulumi.Input[str]:
        """
        Entity ID to assign policies to.
        """
        return pulumi.get(self, "entity_id")

    @entity_id.setter
    def entity_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_id", value)

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of policies to assign to the entity
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "policies", value)

    @property
    @pulumi.getter
    def exclusive(self) -> Optional[pulumi.Input[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

    @exclusive.setter
    def exclusive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclusive", value)

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
class _EntityPoliciesState:
    def __init__(__self__, *,
                 entity_id: Optional[pulumi.Input[str]] = None,
                 entity_name: Optional[pulumi.Input[str]] = None,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering EntityPolicies resources.
        :param pulumi.Input[str] entity_id: Entity ID to assign policies to.
        :param pulumi.Input[str] entity_name: The name of the entity that are assigned the policies.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policies: List of policies to assign to the entity
        """
        if entity_id is not None:
            pulumi.set(__self__, "entity_id", entity_id)
        if entity_name is not None:
            pulumi.set(__self__, "entity_name", entity_name)
        if exclusive is not None:
            pulumi.set(__self__, "exclusive", exclusive)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> Optional[pulumi.Input[str]]:
        """
        Entity ID to assign policies to.
        """
        return pulumi.get(self, "entity_id")

    @entity_id.setter
    def entity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entity_id", value)

    @property
    @pulumi.getter(name="entityName")
    def entity_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the entity that are assigned the policies.
        """
        return pulumi.get(self, "entity_name")

    @entity_name.setter
    def entity_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entity_name", value)

    @property
    @pulumi.getter
    def exclusive(self) -> Optional[pulumi.Input[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

    @exclusive.setter
    def exclusive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclusive", value)

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

    @property
    @pulumi.getter
    def policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of policies to assign to the entity
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "policies", value)


class EntityPolicies(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entity_id: Optional[pulumi.Input[str]] = None,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages policies for an Identity Entity for Vault. The [Identity secrets engine](https://www.vaultproject.io/docs/secrets/identity/index.html) is the identity management solution for Vault.

        ## Example Usage

        ### Exclusive Policies

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        entity = vault.identity.Entity("entity", external_policies=True)
        policies = vault.identity.EntityPolicies("policies",
            policies=[
                "default",
                "test",
            ],
            exclusive=True,
            entity_id=entity.id)
        ```
        <!--End PulumiCodeChooser -->

        ### Non-exclusive Policies

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        entity = vault.identity.Entity("entity", external_policies=True)
        default = vault.identity.EntityPolicies("default",
            policies=[
                "default",
                "test",
            ],
            exclusive=False,
            entity_id=entity.id)
        others = vault.identity.EntityPolicies("others",
            policies=["others"],
            exclusive=False,
            entity_id=entity.id)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] entity_id: Entity ID to assign policies to.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policies: List of policies to assign to the entity
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EntityPoliciesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages policies for an Identity Entity for Vault. The [Identity secrets engine](https://www.vaultproject.io/docs/secrets/identity/index.html) is the identity management solution for Vault.

        ## Example Usage

        ### Exclusive Policies

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        entity = vault.identity.Entity("entity", external_policies=True)
        policies = vault.identity.EntityPolicies("policies",
            policies=[
                "default",
                "test",
            ],
            exclusive=True,
            entity_id=entity.id)
        ```
        <!--End PulumiCodeChooser -->

        ### Non-exclusive Policies

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        entity = vault.identity.Entity("entity", external_policies=True)
        default = vault.identity.EntityPolicies("default",
            policies=[
                "default",
                "test",
            ],
            exclusive=False,
            entity_id=entity.id)
        others = vault.identity.EntityPolicies("others",
            policies=["others"],
            exclusive=False,
            entity_id=entity.id)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param EntityPoliciesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EntityPoliciesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entity_id: Optional[pulumi.Input[str]] = None,
                 exclusive: Optional[pulumi.Input[bool]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EntityPoliciesArgs.__new__(EntityPoliciesArgs)

            if entity_id is None and not opts.urn:
                raise TypeError("Missing required property 'entity_id'")
            __props__.__dict__["entity_id"] = entity_id
            __props__.__dict__["exclusive"] = exclusive
            __props__.__dict__["namespace"] = namespace
            if policies is None and not opts.urn:
                raise TypeError("Missing required property 'policies'")
            __props__.__dict__["policies"] = policies
            __props__.__dict__["entity_name"] = None
        super(EntityPolicies, __self__).__init__(
            'vault:identity/entityPolicies:EntityPolicies',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            entity_id: Optional[pulumi.Input[str]] = None,
            entity_name: Optional[pulumi.Input[str]] = None,
            exclusive: Optional[pulumi.Input[bool]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'EntityPolicies':
        """
        Get an existing EntityPolicies resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] entity_id: Entity ID to assign policies to.
        :param pulumi.Input[str] entity_name: The name of the entity that are assigned the policies.
        :param pulumi.Input[bool] exclusive: Defaults to `true`.
               
               If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.
               
               If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policies: List of policies to assign to the entity
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EntityPoliciesState.__new__(_EntityPoliciesState)

        __props__.__dict__["entity_id"] = entity_id
        __props__.__dict__["entity_name"] = entity_name
        __props__.__dict__["exclusive"] = exclusive
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["policies"] = policies
        return EntityPolicies(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> pulumi.Output[str]:
        """
        Entity ID to assign policies to.
        """
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter(name="entityName")
    def entity_name(self) -> pulumi.Output[str]:
        """
        The name of the entity that are assigned the policies.
        """
        return pulumi.get(self, "entity_name")

    @property
    @pulumi.getter
    def exclusive(self) -> pulumi.Output[Optional[bool]]:
        """
        Defaults to `true`.

        If `true`, this resource will take exclusive control of the policies assigned to the entity and will set it equal to what is specified in the resource.

        If set to `false`, this resource will simply ensure that the policies specified in the resource are present in the entity. When destroying the resource, the resource will ensure that the policies specified in the resource are removed.
        """
        return pulumi.get(self, "exclusive")

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

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Output[Sequence[str]]:
        """
        List of policies to assign to the entity
        """
        return pulumi.get(self, "policies")

