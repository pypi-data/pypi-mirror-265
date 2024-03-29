# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SecretBackendRoleArgs', 'SecretBackendRole']

@pulumi.input_type
class SecretBackendRoleArgs:
    def __init__(__self__, *,
                 backend: pulumi.Input[str],
                 creation_statements: pulumi.Input[Sequence[pulumi.Input[str]]],
                 db_name: pulumi.Input[str],
                 credential_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 credential_type: Optional[pulumi.Input[str]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 max_ttl: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 renew_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 revocation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rollback_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SecretBackendRole resource.
        :param pulumi.Input[str] backend: The unique name of the Vault mount to configure.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] creation_statements: The database statements to execute when
               creating a user.
        :param pulumi.Input[str] db_name: The unique name of the database connection to use for
               the role.
        :param pulumi.Input[Mapping[str, Any]] credential_config: Specifies the configuration
               for the given `credential_type`.
               
               The following options are available for each `credential_type` value:
        :param pulumi.Input[str] credential_type: Specifies the type of credential that
               will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
               See the plugin's API page for credential types supported by individual databases.
        :param pulumi.Input[int] default_ttl: The default number of seconds for leases for this
               role.
        :param pulumi.Input[int] max_ttl: The maximum number of seconds for leases for this
               role.
        :param pulumi.Input[str] name: A unique name to give the role.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured namespace.
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] renew_statements: The database statements to execute when
               renewing a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] revocation_statements: The database statements to execute when
               revoking a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rollback_statements: The database statements to execute when
               rolling back creation due to an error.
        """
        pulumi.set(__self__, "backend", backend)
        pulumi.set(__self__, "creation_statements", creation_statements)
        pulumi.set(__self__, "db_name", db_name)
        if credential_config is not None:
            pulumi.set(__self__, "credential_config", credential_config)
        if credential_type is not None:
            pulumi.set(__self__, "credential_type", credential_type)
        if default_ttl is not None:
            pulumi.set(__self__, "default_ttl", default_ttl)
        if max_ttl is not None:
            pulumi.set(__self__, "max_ttl", max_ttl)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if renew_statements is not None:
            pulumi.set(__self__, "renew_statements", renew_statements)
        if revocation_statements is not None:
            pulumi.set(__self__, "revocation_statements", revocation_statements)
        if rollback_statements is not None:
            pulumi.set(__self__, "rollback_statements", rollback_statements)

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Input[str]:
        """
        The unique name of the Vault mount to configure.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: pulumi.Input[str]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter(name="creationStatements")
    def creation_statements(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The database statements to execute when
        creating a user.
        """
        return pulumi.get(self, "creation_statements")

    @creation_statements.setter
    def creation_statements(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "creation_statements", value)

    @property
    @pulumi.getter(name="dbName")
    def db_name(self) -> pulumi.Input[str]:
        """
        The unique name of the database connection to use for
        the role.
        """
        return pulumi.get(self, "db_name")

    @db_name.setter
    def db_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_name", value)

    @property
    @pulumi.getter(name="credentialConfig")
    def credential_config(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Specifies the configuration
        for the given `credential_type`.

        The following options are available for each `credential_type` value:
        """
        return pulumi.get(self, "credential_config")

    @credential_config.setter
    def credential_config(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "credential_config", value)

    @property
    @pulumi.getter(name="credentialType")
    def credential_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of credential that
        will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
        See the plugin's API page for credential types supported by individual databases.
        """
        return pulumi.get(self, "credential_type")

    @credential_type.setter
    def credential_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credential_type", value)

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The default number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "default_ttl")

    @default_ttl.setter
    def default_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_ttl", value)

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "max_ttl")

    @max_ttl.setter
    def max_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_ttl", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name to give the role.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured namespace.
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="renewStatements")
    def renew_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        renewing a user.
        """
        return pulumi.get(self, "renew_statements")

    @renew_statements.setter
    def renew_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "renew_statements", value)

    @property
    @pulumi.getter(name="revocationStatements")
    def revocation_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        revoking a user.
        """
        return pulumi.get(self, "revocation_statements")

    @revocation_statements.setter
    def revocation_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "revocation_statements", value)

    @property
    @pulumi.getter(name="rollbackStatements")
    def rollback_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        rolling back creation due to an error.
        """
        return pulumi.get(self, "rollback_statements")

    @rollback_statements.setter
    def rollback_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "rollback_statements", value)


@pulumi.input_type
class _SecretBackendRoleState:
    def __init__(__self__, *,
                 backend: Optional[pulumi.Input[str]] = None,
                 creation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credential_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 credential_type: Optional[pulumi.Input[str]] = None,
                 db_name: Optional[pulumi.Input[str]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 max_ttl: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 renew_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 revocation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rollback_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering SecretBackendRole resources.
        :param pulumi.Input[str] backend: The unique name of the Vault mount to configure.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] creation_statements: The database statements to execute when
               creating a user.
        :param pulumi.Input[Mapping[str, Any]] credential_config: Specifies the configuration
               for the given `credential_type`.
               
               The following options are available for each `credential_type` value:
        :param pulumi.Input[str] credential_type: Specifies the type of credential that
               will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
               See the plugin's API page for credential types supported by individual databases.
        :param pulumi.Input[str] db_name: The unique name of the database connection to use for
               the role.
        :param pulumi.Input[int] default_ttl: The default number of seconds for leases for this
               role.
        :param pulumi.Input[int] max_ttl: The maximum number of seconds for leases for this
               role.
        :param pulumi.Input[str] name: A unique name to give the role.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured namespace.
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] renew_statements: The database statements to execute when
               renewing a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] revocation_statements: The database statements to execute when
               revoking a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rollback_statements: The database statements to execute when
               rolling back creation due to an error.
        """
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if creation_statements is not None:
            pulumi.set(__self__, "creation_statements", creation_statements)
        if credential_config is not None:
            pulumi.set(__self__, "credential_config", credential_config)
        if credential_type is not None:
            pulumi.set(__self__, "credential_type", credential_type)
        if db_name is not None:
            pulumi.set(__self__, "db_name", db_name)
        if default_ttl is not None:
            pulumi.set(__self__, "default_ttl", default_ttl)
        if max_ttl is not None:
            pulumi.set(__self__, "max_ttl", max_ttl)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if renew_statements is not None:
            pulumi.set(__self__, "renew_statements", renew_statements)
        if revocation_statements is not None:
            pulumi.set(__self__, "revocation_statements", revocation_statements)
        if rollback_statements is not None:
            pulumi.set(__self__, "rollback_statements", rollback_statements)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input[str]]:
        """
        The unique name of the Vault mount to configure.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter(name="creationStatements")
    def creation_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        creating a user.
        """
        return pulumi.get(self, "creation_statements")

    @creation_statements.setter
    def creation_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "creation_statements", value)

    @property
    @pulumi.getter(name="credentialConfig")
    def credential_config(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Specifies the configuration
        for the given `credential_type`.

        The following options are available for each `credential_type` value:
        """
        return pulumi.get(self, "credential_config")

    @credential_config.setter
    def credential_config(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "credential_config", value)

    @property
    @pulumi.getter(name="credentialType")
    def credential_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of credential that
        will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
        See the plugin's API page for credential types supported by individual databases.
        """
        return pulumi.get(self, "credential_type")

    @credential_type.setter
    def credential_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credential_type", value)

    @property
    @pulumi.getter(name="dbName")
    def db_name(self) -> Optional[pulumi.Input[str]]:
        """
        The unique name of the database connection to use for
        the role.
        """
        return pulumi.get(self, "db_name")

    @db_name.setter
    def db_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_name", value)

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The default number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "default_ttl")

    @default_ttl.setter
    def default_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_ttl", value)

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "max_ttl")

    @max_ttl.setter
    def max_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_ttl", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name to give the role.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured namespace.
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="renewStatements")
    def renew_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        renewing a user.
        """
        return pulumi.get(self, "renew_statements")

    @renew_statements.setter
    def renew_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "renew_statements", value)

    @property
    @pulumi.getter(name="revocationStatements")
    def revocation_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        revoking a user.
        """
        return pulumi.get(self, "revocation_statements")

    @revocation_statements.setter
    def revocation_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "revocation_statements", value)

    @property
    @pulumi.getter(name="rollbackStatements")
    def rollback_statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The database statements to execute when
        rolling back creation due to an error.
        """
        return pulumi.get(self, "rollback_statements")

    @rollback_statements.setter
    def rollback_statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "rollback_statements", value)


class SecretBackendRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 creation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credential_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 credential_type: Optional[pulumi.Input[str]] = None,
                 db_name: Optional[pulumi.Input[str]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 max_ttl: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 renew_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 revocation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rollback_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        db = vault.Mount("db",
            path="postgres",
            type="database")
        postgres = vault.database.SecretBackendConnection("postgres",
            backend=db.path,
            allowed_roles=[
                "dev",
                "prod",
            ],
            postgresql=vault.database.SecretBackendConnectionPostgresqlArgs(
                connection_url="postgres://username:password@host:port/database",
            ))
        role = vault.database.SecretBackendRole("role",
            backend=db.path,
            db_name=postgres.name,
            creation_statements=["CREATE ROLE \\"{{name}}\\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Database secret backend roles can be imported using the `backend`, `/roles/`, and the `name` e.g.

        ```sh
        $ pulumi import vault:database/secretBackendRole:SecretBackendRole example postgres/roles/my-role
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend: The unique name of the Vault mount to configure.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] creation_statements: The database statements to execute when
               creating a user.
        :param pulumi.Input[Mapping[str, Any]] credential_config: Specifies the configuration
               for the given `credential_type`.
               
               The following options are available for each `credential_type` value:
        :param pulumi.Input[str] credential_type: Specifies the type of credential that
               will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
               See the plugin's API page for credential types supported by individual databases.
        :param pulumi.Input[str] db_name: The unique name of the database connection to use for
               the role.
        :param pulumi.Input[int] default_ttl: The default number of seconds for leases for this
               role.
        :param pulumi.Input[int] max_ttl: The maximum number of seconds for leases for this
               role.
        :param pulumi.Input[str] name: A unique name to give the role.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured namespace.
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] renew_statements: The database statements to execute when
               renewing a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] revocation_statements: The database statements to execute when
               revoking a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rollback_statements: The database statements to execute when
               rolling back creation due to an error.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecretBackendRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_vault as vault

        db = vault.Mount("db",
            path="postgres",
            type="database")
        postgres = vault.database.SecretBackendConnection("postgres",
            backend=db.path,
            allowed_roles=[
                "dev",
                "prod",
            ],
            postgresql=vault.database.SecretBackendConnectionPostgresqlArgs(
                connection_url="postgres://username:password@host:port/database",
            ))
        role = vault.database.SecretBackendRole("role",
            backend=db.path,
            db_name=postgres.name,
            creation_statements=["CREATE ROLE \\"{{name}}\\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Database secret backend roles can be imported using the `backend`, `/roles/`, and the `name` e.g.

        ```sh
        $ pulumi import vault:database/secretBackendRole:SecretBackendRole example postgres/roles/my-role
        ```

        :param str resource_name: The name of the resource.
        :param SecretBackendRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecretBackendRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 creation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credential_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 credential_type: Optional[pulumi.Input[str]] = None,
                 db_name: Optional[pulumi.Input[str]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 max_ttl: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 renew_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 revocation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rollback_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecretBackendRoleArgs.__new__(SecretBackendRoleArgs)

            if backend is None and not opts.urn:
                raise TypeError("Missing required property 'backend'")
            __props__.__dict__["backend"] = backend
            if creation_statements is None and not opts.urn:
                raise TypeError("Missing required property 'creation_statements'")
            __props__.__dict__["creation_statements"] = creation_statements
            __props__.__dict__["credential_config"] = credential_config
            __props__.__dict__["credential_type"] = credential_type
            if db_name is None and not opts.urn:
                raise TypeError("Missing required property 'db_name'")
            __props__.__dict__["db_name"] = db_name
            __props__.__dict__["default_ttl"] = default_ttl
            __props__.__dict__["max_ttl"] = max_ttl
            __props__.__dict__["name"] = name
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["renew_statements"] = renew_statements
            __props__.__dict__["revocation_statements"] = revocation_statements
            __props__.__dict__["rollback_statements"] = rollback_statements
        super(SecretBackendRole, __self__).__init__(
            'vault:database/secretBackendRole:SecretBackendRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend: Optional[pulumi.Input[str]] = None,
            creation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            credential_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            credential_type: Optional[pulumi.Input[str]] = None,
            db_name: Optional[pulumi.Input[str]] = None,
            default_ttl: Optional[pulumi.Input[int]] = None,
            max_ttl: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            renew_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            revocation_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            rollback_statements: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'SecretBackendRole':
        """
        Get an existing SecretBackendRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend: The unique name of the Vault mount to configure.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] creation_statements: The database statements to execute when
               creating a user.
        :param pulumi.Input[Mapping[str, Any]] credential_config: Specifies the configuration
               for the given `credential_type`.
               
               The following options are available for each `credential_type` value:
        :param pulumi.Input[str] credential_type: Specifies the type of credential that
               will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
               See the plugin's API page for credential types supported by individual databases.
        :param pulumi.Input[str] db_name: The unique name of the database connection to use for
               the role.
        :param pulumi.Input[int] default_ttl: The default number of seconds for leases for this
               role.
        :param pulumi.Input[int] max_ttl: The maximum number of seconds for leases for this
               role.
        :param pulumi.Input[str] name: A unique name to give the role.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured namespace.
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] renew_statements: The database statements to execute when
               renewing a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] revocation_statements: The database statements to execute when
               revoking a user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rollback_statements: The database statements to execute when
               rolling back creation due to an error.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecretBackendRoleState.__new__(_SecretBackendRoleState)

        __props__.__dict__["backend"] = backend
        __props__.__dict__["creation_statements"] = creation_statements
        __props__.__dict__["credential_config"] = credential_config
        __props__.__dict__["credential_type"] = credential_type
        __props__.__dict__["db_name"] = db_name
        __props__.__dict__["default_ttl"] = default_ttl
        __props__.__dict__["max_ttl"] = max_ttl
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["renew_statements"] = renew_statements
        __props__.__dict__["revocation_statements"] = revocation_statements
        __props__.__dict__["rollback_statements"] = rollback_statements
        return SecretBackendRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Output[str]:
        """
        The unique name of the Vault mount to configure.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter(name="creationStatements")
    def creation_statements(self) -> pulumi.Output[Sequence[str]]:
        """
        The database statements to execute when
        creating a user.
        """
        return pulumi.get(self, "creation_statements")

    @property
    @pulumi.getter(name="credentialConfig")
    def credential_config(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        Specifies the configuration
        for the given `credential_type`.

        The following options are available for each `credential_type` value:
        """
        return pulumi.get(self, "credential_config")

    @property
    @pulumi.getter(name="credentialType")
    def credential_type(self) -> pulumi.Output[str]:
        """
        Specifies the type of credential that
        will be generated for the role. Options include: `password`, `rsa_private_key`, `client_certificate`.
        See the plugin's API page for credential types supported by individual databases.
        """
        return pulumi.get(self, "credential_type")

    @property
    @pulumi.getter(name="dbName")
    def db_name(self) -> pulumi.Output[str]:
        """
        The unique name of the database connection to use for
        the role.
        """
        return pulumi.get(self, "db_name")

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The default number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "default_ttl")

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum number of seconds for leases for this
        role.
        """
        return pulumi.get(self, "max_ttl")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name to give the role.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured namespace.
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="renewStatements")
    def renew_statements(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The database statements to execute when
        renewing a user.
        """
        return pulumi.get(self, "renew_statements")

    @property
    @pulumi.getter(name="revocationStatements")
    def revocation_statements(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The database statements to execute when
        revoking a user.
        """
        return pulumi.get(self, "revocation_statements")

    @property
    @pulumi.getter(name="rollbackStatements")
    def rollback_statements(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The database statements to execute when
        rolling back creation due to an error.
        """
        return pulumi.get(self, "rollback_statements")

