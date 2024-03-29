# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['RaftAutopilotArgs', 'RaftAutopilot']

@pulumi.input_type
class RaftAutopilotArgs:
    def __init__(__self__, *,
                 cleanup_dead_servers: Optional[pulumi.Input[bool]] = None,
                 dead_server_last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 disable_upgrade_migration: Optional[pulumi.Input[bool]] = None,
                 last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 max_trailing_logs: Optional[pulumi.Input[int]] = None,
                 min_quorum: Optional[pulumi.Input[int]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 server_stabilization_time: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RaftAutopilot resource.
        :param pulumi.Input[bool] cleanup_dead_servers: Specifies whether to remove dead server nodes
               periodically or when a new server joins. This requires that `min-quorum` is also set.
        :param pulumi.Input[str] dead_server_last_contact_threshold: Limit the amount of time a 
               server can go without leader contact before being considered failed. This only takes
               effect when `cleanup_dead_servers` is set.
        :param pulumi.Input[bool] disable_upgrade_migration: Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        :param pulumi.Input[str] last_contact_threshold: Limit the amount of time a server can go 
               without leader contact before being considered unhealthy.
        :param pulumi.Input[int] max_trailing_logs: Maximum number of log entries in the Raft log 
               that a server can be behind its leader before being considered unhealthy.
        :param pulumi.Input[int] min_quorum: Minimum number of servers allowed in a cluster before 
               autopilot can prune dead servers. This should at least be 3. Applicable only for
               voting nodes.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] server_stabilization_time: Minimum amount of time a server must be 
               stable in the 'healthy' state before being added to the cluster.
        """
        if cleanup_dead_servers is not None:
            pulumi.set(__self__, "cleanup_dead_servers", cleanup_dead_servers)
        if dead_server_last_contact_threshold is not None:
            pulumi.set(__self__, "dead_server_last_contact_threshold", dead_server_last_contact_threshold)
        if disable_upgrade_migration is not None:
            pulumi.set(__self__, "disable_upgrade_migration", disable_upgrade_migration)
        if last_contact_threshold is not None:
            pulumi.set(__self__, "last_contact_threshold", last_contact_threshold)
        if max_trailing_logs is not None:
            pulumi.set(__self__, "max_trailing_logs", max_trailing_logs)
        if min_quorum is not None:
            pulumi.set(__self__, "min_quorum", min_quorum)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if server_stabilization_time is not None:
            pulumi.set(__self__, "server_stabilization_time", server_stabilization_time)

    @property
    @pulumi.getter(name="cleanupDeadServers")
    def cleanup_dead_servers(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to remove dead server nodes
        periodically or when a new server joins. This requires that `min-quorum` is also set.
        """
        return pulumi.get(self, "cleanup_dead_servers")

    @cleanup_dead_servers.setter
    def cleanup_dead_servers(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cleanup_dead_servers", value)

    @property
    @pulumi.getter(name="deadServerLastContactThreshold")
    def dead_server_last_contact_threshold(self) -> Optional[pulumi.Input[str]]:
        """
        Limit the amount of time a 
        server can go without leader contact before being considered failed. This only takes
        effect when `cleanup_dead_servers` is set.
        """
        return pulumi.get(self, "dead_server_last_contact_threshold")

    @dead_server_last_contact_threshold.setter
    def dead_server_last_contact_threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dead_server_last_contact_threshold", value)

    @property
    @pulumi.getter(name="disableUpgradeMigration")
    def disable_upgrade_migration(self) -> Optional[pulumi.Input[bool]]:
        """
        Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        """
        return pulumi.get(self, "disable_upgrade_migration")

    @disable_upgrade_migration.setter
    def disable_upgrade_migration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_upgrade_migration", value)

    @property
    @pulumi.getter(name="lastContactThreshold")
    def last_contact_threshold(self) -> Optional[pulumi.Input[str]]:
        """
        Limit the amount of time a server can go 
        without leader contact before being considered unhealthy.
        """
        return pulumi.get(self, "last_contact_threshold")

    @last_contact_threshold.setter
    def last_contact_threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_contact_threshold", value)

    @property
    @pulumi.getter(name="maxTrailingLogs")
    def max_trailing_logs(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum number of log entries in the Raft log 
        that a server can be behind its leader before being considered unhealthy.
        """
        return pulumi.get(self, "max_trailing_logs")

    @max_trailing_logs.setter
    def max_trailing_logs(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_trailing_logs", value)

    @property
    @pulumi.getter(name="minQuorum")
    def min_quorum(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum number of servers allowed in a cluster before 
        autopilot can prune dead servers. This should at least be 3. Applicable only for
        voting nodes.
        """
        return pulumi.get(self, "min_quorum")

    @min_quorum.setter
    def min_quorum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_quorum", value)

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
    @pulumi.getter(name="serverStabilizationTime")
    def server_stabilization_time(self) -> Optional[pulumi.Input[str]]:
        """
        Minimum amount of time a server must be 
        stable in the 'healthy' state before being added to the cluster.
        """
        return pulumi.get(self, "server_stabilization_time")

    @server_stabilization_time.setter
    def server_stabilization_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_stabilization_time", value)


@pulumi.input_type
class _RaftAutopilotState:
    def __init__(__self__, *,
                 cleanup_dead_servers: Optional[pulumi.Input[bool]] = None,
                 dead_server_last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 disable_upgrade_migration: Optional[pulumi.Input[bool]] = None,
                 last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 max_trailing_logs: Optional[pulumi.Input[int]] = None,
                 min_quorum: Optional[pulumi.Input[int]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 server_stabilization_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RaftAutopilot resources.
        :param pulumi.Input[bool] cleanup_dead_servers: Specifies whether to remove dead server nodes
               periodically or when a new server joins. This requires that `min-quorum` is also set.
        :param pulumi.Input[str] dead_server_last_contact_threshold: Limit the amount of time a 
               server can go without leader contact before being considered failed. This only takes
               effect when `cleanup_dead_servers` is set.
        :param pulumi.Input[bool] disable_upgrade_migration: Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        :param pulumi.Input[str] last_contact_threshold: Limit the amount of time a server can go 
               without leader contact before being considered unhealthy.
        :param pulumi.Input[int] max_trailing_logs: Maximum number of log entries in the Raft log 
               that a server can be behind its leader before being considered unhealthy.
        :param pulumi.Input[int] min_quorum: Minimum number of servers allowed in a cluster before 
               autopilot can prune dead servers. This should at least be 3. Applicable only for
               voting nodes.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] server_stabilization_time: Minimum amount of time a server must be 
               stable in the 'healthy' state before being added to the cluster.
        """
        if cleanup_dead_servers is not None:
            pulumi.set(__self__, "cleanup_dead_servers", cleanup_dead_servers)
        if dead_server_last_contact_threshold is not None:
            pulumi.set(__self__, "dead_server_last_contact_threshold", dead_server_last_contact_threshold)
        if disable_upgrade_migration is not None:
            pulumi.set(__self__, "disable_upgrade_migration", disable_upgrade_migration)
        if last_contact_threshold is not None:
            pulumi.set(__self__, "last_contact_threshold", last_contact_threshold)
        if max_trailing_logs is not None:
            pulumi.set(__self__, "max_trailing_logs", max_trailing_logs)
        if min_quorum is not None:
            pulumi.set(__self__, "min_quorum", min_quorum)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if server_stabilization_time is not None:
            pulumi.set(__self__, "server_stabilization_time", server_stabilization_time)

    @property
    @pulumi.getter(name="cleanupDeadServers")
    def cleanup_dead_servers(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to remove dead server nodes
        periodically or when a new server joins. This requires that `min-quorum` is also set.
        """
        return pulumi.get(self, "cleanup_dead_servers")

    @cleanup_dead_servers.setter
    def cleanup_dead_servers(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cleanup_dead_servers", value)

    @property
    @pulumi.getter(name="deadServerLastContactThreshold")
    def dead_server_last_contact_threshold(self) -> Optional[pulumi.Input[str]]:
        """
        Limit the amount of time a 
        server can go without leader contact before being considered failed. This only takes
        effect when `cleanup_dead_servers` is set.
        """
        return pulumi.get(self, "dead_server_last_contact_threshold")

    @dead_server_last_contact_threshold.setter
    def dead_server_last_contact_threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dead_server_last_contact_threshold", value)

    @property
    @pulumi.getter(name="disableUpgradeMigration")
    def disable_upgrade_migration(self) -> Optional[pulumi.Input[bool]]:
        """
        Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        """
        return pulumi.get(self, "disable_upgrade_migration")

    @disable_upgrade_migration.setter
    def disable_upgrade_migration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_upgrade_migration", value)

    @property
    @pulumi.getter(name="lastContactThreshold")
    def last_contact_threshold(self) -> Optional[pulumi.Input[str]]:
        """
        Limit the amount of time a server can go 
        without leader contact before being considered unhealthy.
        """
        return pulumi.get(self, "last_contact_threshold")

    @last_contact_threshold.setter
    def last_contact_threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_contact_threshold", value)

    @property
    @pulumi.getter(name="maxTrailingLogs")
    def max_trailing_logs(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum number of log entries in the Raft log 
        that a server can be behind its leader before being considered unhealthy.
        """
        return pulumi.get(self, "max_trailing_logs")

    @max_trailing_logs.setter
    def max_trailing_logs(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_trailing_logs", value)

    @property
    @pulumi.getter(name="minQuorum")
    def min_quorum(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum number of servers allowed in a cluster before 
        autopilot can prune dead servers. This should at least be 3. Applicable only for
        voting nodes.
        """
        return pulumi.get(self, "min_quorum")

    @min_quorum.setter
    def min_quorum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_quorum", value)

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
    @pulumi.getter(name="serverStabilizationTime")
    def server_stabilization_time(self) -> Optional[pulumi.Input[str]]:
        """
        Minimum amount of time a server must be 
        stable in the 'healthy' state before being added to the cluster.
        """
        return pulumi.get(self, "server_stabilization_time")

    @server_stabilization_time.setter
    def server_stabilization_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_stabilization_time", value)


class RaftAutopilot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cleanup_dead_servers: Optional[pulumi.Input[bool]] = None,
                 dead_server_last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 disable_upgrade_migration: Optional[pulumi.Input[bool]] = None,
                 last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 max_trailing_logs: Optional[pulumi.Input[int]] = None,
                 min_quorum: Optional[pulumi.Input[int]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 server_stabilization_time: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Autopilot enables automated workflows for managing Raft clusters. The
        current feature set includes 3 main features: Server Stabilization, Dead
        Server Cleanup and State API. **These three features are introduced in
        Vault 1.7.**

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        autopilot = vault.RaftAutopilot("autopilot",
            cleanup_dead_servers=True,
            dead_server_last_contact_threshold="24h0m0s",
            last_contact_threshold="10s",
            max_trailing_logs=1000,
            min_quorum=3,
            server_stabilization_time="10s")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Raft Autopilot config can be imported using the ID, e.g.

        ```sh
        $ pulumi import vault:index/raftAutopilot:RaftAutopilot autopilot sys/storage/raft/autopilot/configuration
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cleanup_dead_servers: Specifies whether to remove dead server nodes
               periodically or when a new server joins. This requires that `min-quorum` is also set.
        :param pulumi.Input[str] dead_server_last_contact_threshold: Limit the amount of time a 
               server can go without leader contact before being considered failed. This only takes
               effect when `cleanup_dead_servers` is set.
        :param pulumi.Input[bool] disable_upgrade_migration: Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        :param pulumi.Input[str] last_contact_threshold: Limit the amount of time a server can go 
               without leader contact before being considered unhealthy.
        :param pulumi.Input[int] max_trailing_logs: Maximum number of log entries in the Raft log 
               that a server can be behind its leader before being considered unhealthy.
        :param pulumi.Input[int] min_quorum: Minimum number of servers allowed in a cluster before 
               autopilot can prune dead servers. This should at least be 3. Applicable only for
               voting nodes.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] server_stabilization_time: Minimum amount of time a server must be 
               stable in the 'healthy' state before being added to the cluster.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RaftAutopilotArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Autopilot enables automated workflows for managing Raft clusters. The
        current feature set includes 3 main features: Server Stabilization, Dead
        Server Cleanup and State API. **These three features are introduced in
        Vault 1.7.**

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        autopilot = vault.RaftAutopilot("autopilot",
            cleanup_dead_servers=True,
            dead_server_last_contact_threshold="24h0m0s",
            last_contact_threshold="10s",
            max_trailing_logs=1000,
            min_quorum=3,
            server_stabilization_time="10s")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Raft Autopilot config can be imported using the ID, e.g.

        ```sh
        $ pulumi import vault:index/raftAutopilot:RaftAutopilot autopilot sys/storage/raft/autopilot/configuration
        ```

        :param str resource_name: The name of the resource.
        :param RaftAutopilotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RaftAutopilotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cleanup_dead_servers: Optional[pulumi.Input[bool]] = None,
                 dead_server_last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 disable_upgrade_migration: Optional[pulumi.Input[bool]] = None,
                 last_contact_threshold: Optional[pulumi.Input[str]] = None,
                 max_trailing_logs: Optional[pulumi.Input[int]] = None,
                 min_quorum: Optional[pulumi.Input[int]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 server_stabilization_time: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RaftAutopilotArgs.__new__(RaftAutopilotArgs)

            __props__.__dict__["cleanup_dead_servers"] = cleanup_dead_servers
            __props__.__dict__["dead_server_last_contact_threshold"] = dead_server_last_contact_threshold
            __props__.__dict__["disable_upgrade_migration"] = disable_upgrade_migration
            __props__.__dict__["last_contact_threshold"] = last_contact_threshold
            __props__.__dict__["max_trailing_logs"] = max_trailing_logs
            __props__.__dict__["min_quorum"] = min_quorum
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["server_stabilization_time"] = server_stabilization_time
        super(RaftAutopilot, __self__).__init__(
            'vault:index/raftAutopilot:RaftAutopilot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cleanup_dead_servers: Optional[pulumi.Input[bool]] = None,
            dead_server_last_contact_threshold: Optional[pulumi.Input[str]] = None,
            disable_upgrade_migration: Optional[pulumi.Input[bool]] = None,
            last_contact_threshold: Optional[pulumi.Input[str]] = None,
            max_trailing_logs: Optional[pulumi.Input[int]] = None,
            min_quorum: Optional[pulumi.Input[int]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            server_stabilization_time: Optional[pulumi.Input[str]] = None) -> 'RaftAutopilot':
        """
        Get an existing RaftAutopilot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cleanup_dead_servers: Specifies whether to remove dead server nodes
               periodically or when a new server joins. This requires that `min-quorum` is also set.
        :param pulumi.Input[str] dead_server_last_contact_threshold: Limit the amount of time a 
               server can go without leader contact before being considered failed. This only takes
               effect when `cleanup_dead_servers` is set.
        :param pulumi.Input[bool] disable_upgrade_migration: Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        :param pulumi.Input[str] last_contact_threshold: Limit the amount of time a server can go 
               without leader contact before being considered unhealthy.
        :param pulumi.Input[int] max_trailing_logs: Maximum number of log entries in the Raft log 
               that a server can be behind its leader before being considered unhealthy.
        :param pulumi.Input[int] min_quorum: Minimum number of servers allowed in a cluster before 
               autopilot can prune dead servers. This should at least be 3. Applicable only for
               voting nodes.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] server_stabilization_time: Minimum amount of time a server must be 
               stable in the 'healthy' state before being added to the cluster.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RaftAutopilotState.__new__(_RaftAutopilotState)

        __props__.__dict__["cleanup_dead_servers"] = cleanup_dead_servers
        __props__.__dict__["dead_server_last_contact_threshold"] = dead_server_last_contact_threshold
        __props__.__dict__["disable_upgrade_migration"] = disable_upgrade_migration
        __props__.__dict__["last_contact_threshold"] = last_contact_threshold
        __props__.__dict__["max_trailing_logs"] = max_trailing_logs
        __props__.__dict__["min_quorum"] = min_quorum
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["server_stabilization_time"] = server_stabilization_time
        return RaftAutopilot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cleanupDeadServers")
    def cleanup_dead_servers(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to remove dead server nodes
        periodically or when a new server joins. This requires that `min-quorum` is also set.
        """
        return pulumi.get(self, "cleanup_dead_servers")

    @property
    @pulumi.getter(name="deadServerLastContactThreshold")
    def dead_server_last_contact_threshold(self) -> pulumi.Output[Optional[str]]:
        """
        Limit the amount of time a 
        server can go without leader contact before being considered failed. This only takes
        effect when `cleanup_dead_servers` is set.
        """
        return pulumi.get(self, "dead_server_last_contact_threshold")

    @property
    @pulumi.getter(name="disableUpgradeMigration")
    def disable_upgrade_migration(self) -> pulumi.Output[Optional[bool]]:
        """
        Disables automatically upgrading Vault using autopilot. (Enterprise-only)
        """
        return pulumi.get(self, "disable_upgrade_migration")

    @property
    @pulumi.getter(name="lastContactThreshold")
    def last_contact_threshold(self) -> pulumi.Output[Optional[str]]:
        """
        Limit the amount of time a server can go 
        without leader contact before being considered unhealthy.
        """
        return pulumi.get(self, "last_contact_threshold")

    @property
    @pulumi.getter(name="maxTrailingLogs")
    def max_trailing_logs(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum number of log entries in the Raft log 
        that a server can be behind its leader before being considered unhealthy.
        """
        return pulumi.get(self, "max_trailing_logs")

    @property
    @pulumi.getter(name="minQuorum")
    def min_quorum(self) -> pulumi.Output[Optional[int]]:
        """
        Minimum number of servers allowed in a cluster before 
        autopilot can prune dead servers. This should at least be 3. Applicable only for
        voting nodes.
        """
        return pulumi.get(self, "min_quorum")

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
    @pulumi.getter(name="serverStabilizationTime")
    def server_stabilization_time(self) -> pulumi.Output[Optional[str]]:
        """
        Minimum amount of time a server must be 
        stable in the 'healthy' state before being added to the cluster.
        """
        return pulumi.get(self, "server_stabilization_time")

