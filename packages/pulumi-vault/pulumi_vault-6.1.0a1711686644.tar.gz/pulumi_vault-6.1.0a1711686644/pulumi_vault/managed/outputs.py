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
    'KeysAw',
    'KeysAzure',
    'KeysPkc',
]

@pulumi.output_type
class KeysAw(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessKey":
            suggest = "access_key"
        elif key == "keyBits":
            suggest = "key_bits"
        elif key == "keyType":
            suggest = "key_type"
        elif key == "kmsKey":
            suggest = "kms_key"
        elif key == "secretKey":
            suggest = "secret_key"
        elif key == "allowGenerateKey":
            suggest = "allow_generate_key"
        elif key == "allowReplaceKey":
            suggest = "allow_replace_key"
        elif key == "allowStoreKey":
            suggest = "allow_store_key"
        elif key == "anyMount":
            suggest = "any_mount"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeysAw. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeysAw.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeysAw.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_key: str,
                 key_bits: str,
                 key_type: str,
                 kms_key: str,
                 name: str,
                 secret_key: str,
                 allow_generate_key: Optional[bool] = None,
                 allow_replace_key: Optional[bool] = None,
                 allow_store_key: Optional[bool] = None,
                 any_mount: Optional[bool] = None,
                 curve: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 region: Optional[str] = None,
                 uuid: Optional[str] = None):
        """
        :param str access_key: The AWS access key to use.
        :param str key_bits: The size in bits for an RSA key.
        :param str key_type: The type of key to use.
        :param str kms_key: An identifier for the key.
        :param str name: A unique lowercase name that serves as identifying the key.
        :param str secret_key: The AWS access key to use.
        :param bool allow_generate_key: If no existing key can be found in 
               the referenced backend, instructs Vault to generate a key within the backend.
        :param bool allow_replace_key: Controls the ability for Vault to replace through
               generation or importing a key into the configured backend even
               if a key is present, if set to `false` those operations are forbidden
               if a key exists.
        :param bool allow_store_key: Controls the ability for Vault to import a key to the
               configured backend, if `false`, those operations will be forbidden.
        :param bool any_mount: If `true`, allows usage from any mount point within the
               namespace.
        :param str curve: The curve to use for an ECDSA key. Used when `key_type` 
               is `ECDSA`. Required if `allow_generate_key` is `true`.
        :param str endpoint: Used to specify a custom AWS endpoint.
        :param str region: The AWS region where the keys are stored (or will be stored).
        :param str uuid: ID of the managed key read from Vault
        """
        pulumi.set(__self__, "access_key", access_key)
        pulumi.set(__self__, "key_bits", key_bits)
        pulumi.set(__self__, "key_type", key_type)
        pulumi.set(__self__, "kms_key", kms_key)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "secret_key", secret_key)
        if allow_generate_key is not None:
            pulumi.set(__self__, "allow_generate_key", allow_generate_key)
        if allow_replace_key is not None:
            pulumi.set(__self__, "allow_replace_key", allow_replace_key)
        if allow_store_key is not None:
            pulumi.set(__self__, "allow_store_key", allow_store_key)
        if any_mount is not None:
            pulumi.set(__self__, "any_mount", any_mount)
        if curve is not None:
            pulumi.set(__self__, "curve", curve)
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> str:
        """
        The AWS access key to use.
        """
        return pulumi.get(self, "access_key")

    @property
    @pulumi.getter(name="keyBits")
    def key_bits(self) -> str:
        """
        The size in bits for an RSA key.
        """
        return pulumi.get(self, "key_bits")

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> str:
        """
        The type of key to use.
        """
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter(name="kmsKey")
    def kms_key(self) -> str:
        """
        An identifier for the key.
        """
        return pulumi.get(self, "kms_key")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A unique lowercase name that serves as identifying the key.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="secretKey")
    def secret_key(self) -> str:
        """
        The AWS access key to use.
        """
        return pulumi.get(self, "secret_key")

    @property
    @pulumi.getter(name="allowGenerateKey")
    def allow_generate_key(self) -> Optional[bool]:
        """
        If no existing key can be found in 
        the referenced backend, instructs Vault to generate a key within the backend.
        """
        return pulumi.get(self, "allow_generate_key")

    @property
    @pulumi.getter(name="allowReplaceKey")
    def allow_replace_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to replace through
        generation or importing a key into the configured backend even
        if a key is present, if set to `false` those operations are forbidden
        if a key exists.
        """
        return pulumi.get(self, "allow_replace_key")

    @property
    @pulumi.getter(name="allowStoreKey")
    def allow_store_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to import a key to the
        configured backend, if `false`, those operations will be forbidden.
        """
        return pulumi.get(self, "allow_store_key")

    @property
    @pulumi.getter(name="anyMount")
    def any_mount(self) -> Optional[bool]:
        """
        If `true`, allows usage from any mount point within the
        namespace.
        """
        return pulumi.get(self, "any_mount")

    @property
    @pulumi.getter
    def curve(self) -> Optional[str]:
        """
        The curve to use for an ECDSA key. Used when `key_type` 
        is `ECDSA`. Required if `allow_generate_key` is `true`.
        """
        return pulumi.get(self, "curve")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        Used to specify a custom AWS endpoint.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        """
        The AWS region where the keys are stored (or will be stored).
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def uuid(self) -> Optional[str]:
        """
        ID of the managed key read from Vault
        """
        return pulumi.get(self, "uuid")


@pulumi.output_type
class KeysAzure(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "clientSecret":
            suggest = "client_secret"
        elif key == "keyName":
            suggest = "key_name"
        elif key == "keyType":
            suggest = "key_type"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "vaultName":
            suggest = "vault_name"
        elif key == "allowGenerateKey":
            suggest = "allow_generate_key"
        elif key == "allowReplaceKey":
            suggest = "allow_replace_key"
        elif key == "allowStoreKey":
            suggest = "allow_store_key"
        elif key == "anyMount":
            suggest = "any_mount"
        elif key == "keyBits":
            suggest = "key_bits"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeysAzure. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeysAzure.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeysAzure.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 client_secret: str,
                 key_name: str,
                 key_type: str,
                 name: str,
                 tenant_id: str,
                 vault_name: str,
                 allow_generate_key: Optional[bool] = None,
                 allow_replace_key: Optional[bool] = None,
                 allow_store_key: Optional[bool] = None,
                 any_mount: Optional[bool] = None,
                 environment: Optional[str] = None,
                 key_bits: Optional[str] = None,
                 resource: Optional[str] = None,
                 uuid: Optional[str] = None):
        """
        :param str client_id: The client id for credentials to query the Azure APIs.
        :param str client_secret: The client secret for credentials to query the Azure APIs.
        :param str key_name: The Key Vault key to use for encryption and decryption.
        :param str key_type: The type of key to use.
        :param str name: A unique lowercase name that serves as identifying the key.
        :param str tenant_id: The tenant id for the Azure Active Directory organization.
        :param str vault_name: The Key Vault vault to use for encryption and decryption.
        :param bool allow_generate_key: If no existing key can be found in 
               the referenced backend, instructs Vault to generate a key within the backend.
        :param bool allow_replace_key: Controls the ability for Vault to replace through
               generation or importing a key into the configured backend even
               if a key is present, if set to `false` those operations are forbidden
               if a key exists.
        :param bool allow_store_key: Controls the ability for Vault to import a key to the
               configured backend, if `false`, those operations will be forbidden.
        :param bool any_mount: If `true`, allows usage from any mount point within the
               namespace.
        :param str environment: The Azure Cloud environment API endpoints to use.
        :param str key_bits: The size in bits for an RSA key.
        :param str resource: The Azure Key Vault resource's DNS Suffix to connect to.
        :param str uuid: ID of the managed key read from Vault
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "client_secret", client_secret)
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "key_type", key_type)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "vault_name", vault_name)
        if allow_generate_key is not None:
            pulumi.set(__self__, "allow_generate_key", allow_generate_key)
        if allow_replace_key is not None:
            pulumi.set(__self__, "allow_replace_key", allow_replace_key)
        if allow_store_key is not None:
            pulumi.set(__self__, "allow_store_key", allow_store_key)
        if any_mount is not None:
            pulumi.set(__self__, "any_mount", any_mount)
        if environment is not None:
            pulumi.set(__self__, "environment", environment)
        if key_bits is not None:
            pulumi.set(__self__, "key_bits", key_bits)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id for credentials to query the Azure APIs.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> str:
        """
        The client secret for credentials to query the Azure APIs.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        """
        The Key Vault key to use for encryption and decryption.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> str:
        """
        The type of key to use.
        """
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A unique lowercase name that serves as identifying the key.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id for the Azure Active Directory organization.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> str:
        """
        The Key Vault vault to use for encryption and decryption.
        """
        return pulumi.get(self, "vault_name")

    @property
    @pulumi.getter(name="allowGenerateKey")
    def allow_generate_key(self) -> Optional[bool]:
        """
        If no existing key can be found in 
        the referenced backend, instructs Vault to generate a key within the backend.
        """
        return pulumi.get(self, "allow_generate_key")

    @property
    @pulumi.getter(name="allowReplaceKey")
    def allow_replace_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to replace through
        generation or importing a key into the configured backend even
        if a key is present, if set to `false` those operations are forbidden
        if a key exists.
        """
        return pulumi.get(self, "allow_replace_key")

    @property
    @pulumi.getter(name="allowStoreKey")
    def allow_store_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to import a key to the
        configured backend, if `false`, those operations will be forbidden.
        """
        return pulumi.get(self, "allow_store_key")

    @property
    @pulumi.getter(name="anyMount")
    def any_mount(self) -> Optional[bool]:
        """
        If `true`, allows usage from any mount point within the
        namespace.
        """
        return pulumi.get(self, "any_mount")

    @property
    @pulumi.getter
    def environment(self) -> Optional[str]:
        """
        The Azure Cloud environment API endpoints to use.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="keyBits")
    def key_bits(self) -> Optional[str]:
        """
        The size in bits for an RSA key.
        """
        return pulumi.get(self, "key_bits")

    @property
    @pulumi.getter
    def resource(self) -> Optional[str]:
        """
        The Azure Key Vault resource's DNS Suffix to connect to.
        """
        return pulumi.get(self, "resource")

    @property
    @pulumi.getter
    def uuid(self) -> Optional[str]:
        """
        ID of the managed key read from Vault
        """
        return pulumi.get(self, "uuid")


@pulumi.output_type
class KeysPkc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyId":
            suggest = "key_id"
        elif key == "keyLabel":
            suggest = "key_label"
        elif key == "allowGenerateKey":
            suggest = "allow_generate_key"
        elif key == "allowReplaceKey":
            suggest = "allow_replace_key"
        elif key == "allowStoreKey":
            suggest = "allow_store_key"
        elif key == "anyMount":
            suggest = "any_mount"
        elif key == "forceRwSession":
            suggest = "force_rw_session"
        elif key == "keyBits":
            suggest = "key_bits"
        elif key == "tokenLabel":
            suggest = "token_label"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeysPkc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeysPkc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeysPkc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_id: str,
                 key_label: str,
                 library: str,
                 mechanism: str,
                 name: str,
                 pin: str,
                 allow_generate_key: Optional[bool] = None,
                 allow_replace_key: Optional[bool] = None,
                 allow_store_key: Optional[bool] = None,
                 any_mount: Optional[bool] = None,
                 curve: Optional[str] = None,
                 force_rw_session: Optional[str] = None,
                 key_bits: Optional[str] = None,
                 slot: Optional[str] = None,
                 token_label: Optional[str] = None,
                 uuid: Optional[str] = None):
        """
        :param str key_id: The id of a PKCS#11 key to use.
        :param str key_label: The label of the key to use.
        :param str library: The name of the kms_library stanza to use from Vault's config
               to lookup the local library path.
        :param str mechanism: The encryption/decryption mechanism to use, specified as a
               hexadecimal (prefixed by 0x) string.
        :param str name: A unique lowercase name that serves as identifying the key.
        :param str pin: The PIN for login.
        :param bool allow_generate_key: If no existing key can be found in 
               the referenced backend, instructs Vault to generate a key within the backend.
        :param bool allow_replace_key: Controls the ability for Vault to replace through
               generation or importing a key into the configured backend even
               if a key is present, if set to `false` those operations are forbidden
               if a key exists.
        :param bool allow_store_key: Controls the ability for Vault to import a key to the
               configured backend, if `false`, those operations will be forbidden.
        :param bool any_mount: If `true`, allows usage from any mount point within the
               namespace.
        :param str curve: The curve to use for an ECDSA key. Used when `key_type` 
               is `ECDSA`. Required if `allow_generate_key` is `true`.
        :param str force_rw_session: Force all operations to open up a read-write session to
               the HSM.
        :param str key_bits: The size in bits for an RSA key.
        :param str slot: The slot number to use, specified as a string in a decimal format
               (e.g. `2305843009213693953`).
        :param str token_label: The slot token label to use.
        :param str uuid: ID of the managed key read from Vault
        """
        pulumi.set(__self__, "key_id", key_id)
        pulumi.set(__self__, "key_label", key_label)
        pulumi.set(__self__, "library", library)
        pulumi.set(__self__, "mechanism", mechanism)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "pin", pin)
        if allow_generate_key is not None:
            pulumi.set(__self__, "allow_generate_key", allow_generate_key)
        if allow_replace_key is not None:
            pulumi.set(__self__, "allow_replace_key", allow_replace_key)
        if allow_store_key is not None:
            pulumi.set(__self__, "allow_store_key", allow_store_key)
        if any_mount is not None:
            pulumi.set(__self__, "any_mount", any_mount)
        if curve is not None:
            pulumi.set(__self__, "curve", curve)
        if force_rw_session is not None:
            pulumi.set(__self__, "force_rw_session", force_rw_session)
        if key_bits is not None:
            pulumi.set(__self__, "key_bits", key_bits)
        if slot is not None:
            pulumi.set(__self__, "slot", slot)
        if token_label is not None:
            pulumi.set(__self__, "token_label", token_label)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        """
        The id of a PKCS#11 key to use.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyLabel")
    def key_label(self) -> str:
        """
        The label of the key to use.
        """
        return pulumi.get(self, "key_label")

    @property
    @pulumi.getter
    def library(self) -> str:
        """
        The name of the kms_library stanza to use from Vault's config
        to lookup the local library path.
        """
        return pulumi.get(self, "library")

    @property
    @pulumi.getter
    def mechanism(self) -> str:
        """
        The encryption/decryption mechanism to use, specified as a
        hexadecimal (prefixed by 0x) string.
        """
        return pulumi.get(self, "mechanism")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A unique lowercase name that serves as identifying the key.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def pin(self) -> str:
        """
        The PIN for login.
        """
        return pulumi.get(self, "pin")

    @property
    @pulumi.getter(name="allowGenerateKey")
    def allow_generate_key(self) -> Optional[bool]:
        """
        If no existing key can be found in 
        the referenced backend, instructs Vault to generate a key within the backend.
        """
        return pulumi.get(self, "allow_generate_key")

    @property
    @pulumi.getter(name="allowReplaceKey")
    def allow_replace_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to replace through
        generation or importing a key into the configured backend even
        if a key is present, if set to `false` those operations are forbidden
        if a key exists.
        """
        return pulumi.get(self, "allow_replace_key")

    @property
    @pulumi.getter(name="allowStoreKey")
    def allow_store_key(self) -> Optional[bool]:
        """
        Controls the ability for Vault to import a key to the
        configured backend, if `false`, those operations will be forbidden.
        """
        return pulumi.get(self, "allow_store_key")

    @property
    @pulumi.getter(name="anyMount")
    def any_mount(self) -> Optional[bool]:
        """
        If `true`, allows usage from any mount point within the
        namespace.
        """
        return pulumi.get(self, "any_mount")

    @property
    @pulumi.getter
    def curve(self) -> Optional[str]:
        """
        The curve to use for an ECDSA key. Used when `key_type` 
        is `ECDSA`. Required if `allow_generate_key` is `true`.
        """
        return pulumi.get(self, "curve")

    @property
    @pulumi.getter(name="forceRwSession")
    def force_rw_session(self) -> Optional[str]:
        """
        Force all operations to open up a read-write session to
        the HSM.
        """
        return pulumi.get(self, "force_rw_session")

    @property
    @pulumi.getter(name="keyBits")
    def key_bits(self) -> Optional[str]:
        """
        The size in bits for an RSA key.
        """
        return pulumi.get(self, "key_bits")

    @property
    @pulumi.getter
    def slot(self) -> Optional[str]:
        """
        The slot number to use, specified as a string in a decimal format
        (e.g. `2305843009213693953`).
        """
        return pulumi.get(self, "slot")

    @property
    @pulumi.getter(name="tokenLabel")
    def token_label(self) -> Optional[str]:
        """
        The slot token label to use.
        """
        return pulumi.get(self, "token_label")

    @property
    @pulumi.getter
    def uuid(self) -> Optional[str]:
        """
        ID of the managed key read from Vault
        """
        return pulumi.get(self, "uuid")


