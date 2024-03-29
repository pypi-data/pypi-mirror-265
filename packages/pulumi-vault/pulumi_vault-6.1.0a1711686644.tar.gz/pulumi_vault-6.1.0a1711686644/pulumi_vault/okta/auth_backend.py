# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['AuthBackendArgs', 'AuthBackend']

@pulumi.input_type
class AuthBackendArgs:
    def __init__(__self__, *,
                 organization: pulumi.Input[str],
                 base_url: Optional[pulumi.Input[str]] = None,
                 bypass_okta_mfa: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disable_remount: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]] = None,
                 max_ttl: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]] = None):
        """
        The set of arguments for constructing a AuthBackend resource.
        :param pulumi.Input[str] organization: The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        :param pulumi.Input[str] base_url: The Okta url. Examples: oktapreview.com, okta.com
        :param pulumi.Input[bool] bypass_okta_mfa: When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        :param pulumi.Input[str] description: The description of the auth backend
        :param pulumi.Input[bool] disable_remount: If set, opts out of mount migration on path updates.
               See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        :param pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]] groups: Associate Okta groups with policies within Vault.
               See below for more details.
        :param pulumi.Input[str] max_ttl: Maximum duration after which authentication will be expired
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] path: Path to mount the Okta auth backend. Default to path `okta`.
        :param pulumi.Input[str] token: The Okta API token. This is required to query Okta for user group membership.
               If this is not supplied only locally configured groups will be enabled.
        :param pulumi.Input[str] ttl: Duration after which authentication will be expired.
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]] users: Associate Okta users with groups or policies within Vault.
               See below for more details.
        """
        pulumi.set(__self__, "organization", organization)
        if base_url is not None:
            pulumi.set(__self__, "base_url", base_url)
        if bypass_okta_mfa is not None:
            pulumi.set(__self__, "bypass_okta_mfa", bypass_okta_mfa)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disable_remount is not None:
            pulumi.set(__self__, "disable_remount", disable_remount)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if max_ttl is not None:
            pulumi.set(__self__, "max_ttl", max_ttl)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if token is not None:
            pulumi.set(__self__, "token", token)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def organization(self) -> pulumi.Input[str]:
        """
        The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        """
        return pulumi.get(self, "organization")

    @organization.setter
    def organization(self, value: pulumi.Input[str]):
        pulumi.set(self, "organization", value)

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> Optional[pulumi.Input[str]]:
        """
        The Okta url. Examples: oktapreview.com, okta.com
        """
        return pulumi.get(self, "base_url")

    @base_url.setter
    def base_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_url", value)

    @property
    @pulumi.getter(name="bypassOktaMfa")
    def bypass_okta_mfa(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        """
        return pulumi.get(self, "bypass_okta_mfa")

    @bypass_okta_mfa.setter
    def bypass_okta_mfa(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_okta_mfa", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the auth backend
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="disableRemount")
    def disable_remount(self) -> Optional[pulumi.Input[bool]]:
        """
        If set, opts out of mount migration on path updates.
        See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        """
        return pulumi.get(self, "disable_remount")

    @disable_remount.setter
    def disable_remount(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_remount", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]]:
        """
        Associate Okta groups with policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> Optional[pulumi.Input[str]]:
        """
        Maximum duration after which authentication will be expired
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "max_ttl")

    @max_ttl.setter
    def max_ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "max_ttl", value)

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
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        Path to mount the Okta auth backend. Default to path `okta`.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        The Okta API token. This is required to query Okta for user group membership.
        If this is not supplied only locally configured groups will be enabled.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[str]]:
        """
        Duration after which authentication will be expired.
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]]:
        """
        Associate Okta users with groups or policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]]):
        pulumi.set(self, "users", value)


@pulumi.input_type
class _AuthBackendState:
    def __init__(__self__, *,
                 accessor: Optional[pulumi.Input[str]] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 bypass_okta_mfa: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disable_remount: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]] = None,
                 max_ttl: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]] = None):
        """
        Input properties used for looking up and filtering AuthBackend resources.
        :param pulumi.Input[str] accessor: The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        :param pulumi.Input[str] base_url: The Okta url. Examples: oktapreview.com, okta.com
        :param pulumi.Input[bool] bypass_okta_mfa: When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        :param pulumi.Input[str] description: The description of the auth backend
        :param pulumi.Input[bool] disable_remount: If set, opts out of mount migration on path updates.
               See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        :param pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]] groups: Associate Okta groups with policies within Vault.
               See below for more details.
        :param pulumi.Input[str] max_ttl: Maximum duration after which authentication will be expired
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] organization: The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        :param pulumi.Input[str] path: Path to mount the Okta auth backend. Default to path `okta`.
        :param pulumi.Input[str] token: The Okta API token. This is required to query Okta for user group membership.
               If this is not supplied only locally configured groups will be enabled.
        :param pulumi.Input[str] ttl: Duration after which authentication will be expired.
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]] users: Associate Okta users with groups or policies within Vault.
               See below for more details.
        """
        if accessor is not None:
            pulumi.set(__self__, "accessor", accessor)
        if base_url is not None:
            pulumi.set(__self__, "base_url", base_url)
        if bypass_okta_mfa is not None:
            pulumi.set(__self__, "bypass_okta_mfa", bypass_okta_mfa)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disable_remount is not None:
            pulumi.set(__self__, "disable_remount", disable_remount)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if max_ttl is not None:
            pulumi.set(__self__, "max_ttl", max_ttl)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if organization is not None:
            pulumi.set(__self__, "organization", organization)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if token is not None:
            pulumi.set(__self__, "token", token)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def accessor(self) -> Optional[pulumi.Input[str]]:
        """
        The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        """
        return pulumi.get(self, "accessor")

    @accessor.setter
    def accessor(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accessor", value)

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> Optional[pulumi.Input[str]]:
        """
        The Okta url. Examples: oktapreview.com, okta.com
        """
        return pulumi.get(self, "base_url")

    @base_url.setter
    def base_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_url", value)

    @property
    @pulumi.getter(name="bypassOktaMfa")
    def bypass_okta_mfa(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        """
        return pulumi.get(self, "bypass_okta_mfa")

    @bypass_okta_mfa.setter
    def bypass_okta_mfa(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_okta_mfa", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the auth backend
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="disableRemount")
    def disable_remount(self) -> Optional[pulumi.Input[bool]]:
        """
        If set, opts out of mount migration on path updates.
        See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        """
        return pulumi.get(self, "disable_remount")

    @disable_remount.setter
    def disable_remount(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_remount", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]]:
        """
        Associate Okta groups with policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendGroupArgs']]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> Optional[pulumi.Input[str]]:
        """
        Maximum duration after which authentication will be expired
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "max_ttl")

    @max_ttl.setter
    def max_ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "max_ttl", value)

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
    def organization(self) -> Optional[pulumi.Input[str]]:
        """
        The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        """
        return pulumi.get(self, "organization")

    @organization.setter
    def organization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        Path to mount the Okta auth backend. Default to path `okta`.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        The Okta API token. This is required to query Okta for user group membership.
        If this is not supplied only locally configured groups will be enabled.
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[str]]:
        """
        Duration after which authentication will be expired.
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]]:
        """
        Associate Okta users with groups or policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuthBackendUserArgs']]]]):
        pulumi.set(self, "users", value)


class AuthBackend(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 bypass_okta_mfa: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disable_remount: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendGroupArgs']]]]] = None,
                 max_ttl: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendUserArgs']]]]] = None,
                 __props__=None):
        """
        Provides a resource for managing an
        [Okta auth backend within Vault](https://www.vaultproject.io/docs/auth/okta.html).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        example = vault.okta.AuthBackend("example",
            description="Demonstration of the Terraform Okta auth backend",
            groups=[vault.okta.AuthBackendGroupArgs(
                group_name="foo",
                policies=[
                    "one",
                    "two",
                ],
            )],
            organization="example",
            token="something that should be kept secret",
            users=[vault.okta.AuthBackendUserArgs(
                groups=["foo"],
                username="bar",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Okta authentication backends can be imported using its `path`, e.g.

        ```sh
        $ pulumi import vault:okta/authBackend:AuthBackend example okta
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] base_url: The Okta url. Examples: oktapreview.com, okta.com
        :param pulumi.Input[bool] bypass_okta_mfa: When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        :param pulumi.Input[str] description: The description of the auth backend
        :param pulumi.Input[bool] disable_remount: If set, opts out of mount migration on path updates.
               See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendGroupArgs']]]] groups: Associate Okta groups with policies within Vault.
               See below for more details.
        :param pulumi.Input[str] max_ttl: Maximum duration after which authentication will be expired
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] organization: The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        :param pulumi.Input[str] path: Path to mount the Okta auth backend. Default to path `okta`.
        :param pulumi.Input[str] token: The Okta API token. This is required to query Okta for user group membership.
               If this is not supplied only locally configured groups will be enabled.
        :param pulumi.Input[str] ttl: Duration after which authentication will be expired.
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendUserArgs']]]] users: Associate Okta users with groups or policies within Vault.
               See below for more details.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AuthBackendArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource for managing an
        [Okta auth backend within Vault](https://www.vaultproject.io/docs/auth/okta.html).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        example = vault.okta.AuthBackend("example",
            description="Demonstration of the Terraform Okta auth backend",
            groups=[vault.okta.AuthBackendGroupArgs(
                group_name="foo",
                policies=[
                    "one",
                    "two",
                ],
            )],
            organization="example",
            token="something that should be kept secret",
            users=[vault.okta.AuthBackendUserArgs(
                groups=["foo"],
                username="bar",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Okta authentication backends can be imported using its `path`, e.g.

        ```sh
        $ pulumi import vault:okta/authBackend:AuthBackend example okta
        ```

        :param str resource_name: The name of the resource.
        :param AuthBackendArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AuthBackendArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 bypass_okta_mfa: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disable_remount: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendGroupArgs']]]]] = None,
                 max_ttl: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendUserArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AuthBackendArgs.__new__(AuthBackendArgs)

            __props__.__dict__["base_url"] = base_url
            __props__.__dict__["bypass_okta_mfa"] = bypass_okta_mfa
            __props__.__dict__["description"] = description
            __props__.__dict__["disable_remount"] = disable_remount
            __props__.__dict__["groups"] = groups
            __props__.__dict__["max_ttl"] = max_ttl
            __props__.__dict__["namespace"] = namespace
            if organization is None and not opts.urn:
                raise TypeError("Missing required property 'organization'")
            __props__.__dict__["organization"] = organization
            __props__.__dict__["path"] = path
            __props__.__dict__["token"] = None if token is None else pulumi.Output.secret(token)
            __props__.__dict__["ttl"] = ttl
            __props__.__dict__["users"] = users
            __props__.__dict__["accessor"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["token"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(AuthBackend, __self__).__init__(
            'vault:okta/authBackend:AuthBackend',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accessor: Optional[pulumi.Input[str]] = None,
            base_url: Optional[pulumi.Input[str]] = None,
            bypass_okta_mfa: Optional[pulumi.Input[bool]] = None,
            description: Optional[pulumi.Input[str]] = None,
            disable_remount: Optional[pulumi.Input[bool]] = None,
            groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendGroupArgs']]]]] = None,
            max_ttl: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            organization: Optional[pulumi.Input[str]] = None,
            path: Optional[pulumi.Input[str]] = None,
            token: Optional[pulumi.Input[str]] = None,
            ttl: Optional[pulumi.Input[str]] = None,
            users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendUserArgs']]]]] = None) -> 'AuthBackend':
        """
        Get an existing AuthBackend resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accessor: The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        :param pulumi.Input[str] base_url: The Okta url. Examples: oktapreview.com, okta.com
        :param pulumi.Input[bool] bypass_okta_mfa: When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        :param pulumi.Input[str] description: The description of the auth backend
        :param pulumi.Input[bool] disable_remount: If set, opts out of mount migration on path updates.
               See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendGroupArgs']]]] groups: Associate Okta groups with policies within Vault.
               See below for more details.
        :param pulumi.Input[str] max_ttl: Maximum duration after which authentication will be expired
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] organization: The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        :param pulumi.Input[str] path: Path to mount the Okta auth backend. Default to path `okta`.
        :param pulumi.Input[str] token: The Okta API token. This is required to query Okta for user group membership.
               If this is not supplied only locally configured groups will be enabled.
        :param pulumi.Input[str] ttl: Duration after which authentication will be expired.
               [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuthBackendUserArgs']]]] users: Associate Okta users with groups or policies within Vault.
               See below for more details.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AuthBackendState.__new__(_AuthBackendState)

        __props__.__dict__["accessor"] = accessor
        __props__.__dict__["base_url"] = base_url
        __props__.__dict__["bypass_okta_mfa"] = bypass_okta_mfa
        __props__.__dict__["description"] = description
        __props__.__dict__["disable_remount"] = disable_remount
        __props__.__dict__["groups"] = groups
        __props__.__dict__["max_ttl"] = max_ttl
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["organization"] = organization
        __props__.__dict__["path"] = path
        __props__.__dict__["token"] = token
        __props__.__dict__["ttl"] = ttl
        __props__.__dict__["users"] = users
        return AuthBackend(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def accessor(self) -> pulumi.Output[str]:
        """
        The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        """
        return pulumi.get(self, "accessor")

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> pulumi.Output[Optional[str]]:
        """
        The Okta url. Examples: oktapreview.com, okta.com
        """
        return pulumi.get(self, "base_url")

    @property
    @pulumi.getter(name="bypassOktaMfa")
    def bypass_okta_mfa(self) -> pulumi.Output[Optional[bool]]:
        """
        When true, requests by Okta for a MFA check will be bypassed. This also disallows certain status checks on the account, such as whether the password is expired.
        """
        return pulumi.get(self, "bypass_okta_mfa")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the auth backend
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="disableRemount")
    def disable_remount(self) -> pulumi.Output[Optional[bool]]:
        """
        If set, opts out of mount migration on path updates.
        See here for more info on [Mount Migration](https://www.vaultproject.io/docs/concepts/mount-migration)
        """
        return pulumi.get(self, "disable_remount")

    @property
    @pulumi.getter
    def groups(self) -> pulumi.Output[Sequence['outputs.AuthBackendGroup']]:
        """
        Associate Okta groups with policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> pulumi.Output[Optional[str]]:
        """
        Maximum duration after which authentication will be expired
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "max_ttl")

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
    def organization(self) -> pulumi.Output[str]:
        """
        The Okta organization. This will be the first part of the url `https://XXX.okta.com`
        """
        return pulumi.get(self, "organization")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        """
        Path to mount the Okta auth backend. Default to path `okta`.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def token(self) -> pulumi.Output[Optional[str]]:
        """
        The Okta API token. This is required to query Okta for user group membership.
        If this is not supplied only locally configured groups will be enabled.
        """
        return pulumi.get(self, "token")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[str]]:
        """
        Duration after which authentication will be expired.
        [See the documentation for info on valid duration formats](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def users(self) -> pulumi.Output[Sequence['outputs.AuthBackendUser']]:
        """
        Associate Okta users with groups or policies within Vault.
        See below for more details.
        """
        return pulumi.get(self, "users")

