# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'AuthBackendGroup',
    'AuthBackendUser',
]

@pulumi.output_type
class AuthBackendGroup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupName":
            suggest = "group_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuthBackendGroup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuthBackendGroup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AuthBackendGroup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 group_name: str,
                 policies: Sequence[str]):
        """
        :param str group_name: Name of the group within the Okta
        :param Sequence[str] policies: Vault policies to associate with this group
        """
        pulumi.set(__self__, "group_name", group_name)
        pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> str:
        """
        Name of the group within the Okta
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def policies(self) -> Sequence[str]:
        """
        Vault policies to associate with this group
        """
        return pulumi.get(self, "policies")


@pulumi.output_type
class AuthBackendUser(dict):
    def __init__(__self__, *,
                 username: str,
                 groups: Optional[Sequence[str]] = None,
                 policies: Optional[Sequence[str]] = None):
        """
        :param str username: Name of the user within Okta
        :param Sequence[str] groups: List of Okta groups to associate with this user
        :param Sequence[str] policies: Vault policies to associate with this group
        """
        pulumi.set(__self__, "username", username)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        Name of the user within Okta
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter
    def groups(self) -> Optional[Sequence[str]]:
        """
        List of Okta groups to associate with this user
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def policies(self) -> Optional[Sequence[str]]:
        """
        Vault policies to associate with this group
        """
        return pulumi.get(self, "policies")


