# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AuthBackendCertArgs', 'AuthBackendCert']

@pulumi.input_type
class AuthBackendCertArgs:
    def __init__(__self__, *,
                 aws_public_cert: pulumi.Input[str],
                 cert_name: pulumi.Input[str],
                 backend: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AuthBackendCert resource.
        :param pulumi.Input[str] aws_public_cert: The  Base64 encoded AWS Public key required to
               verify PKCS7 signature of the EC2 instance metadata. You can find this key in
               the [AWS
               documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        :param pulumi.Input[str] cert_name: The name of the certificate.
        :param pulumi.Input[str] backend: The path the AWS auth backend being configured was
               mounted at.  Defaults to `aws`.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] type: Either "pkcs7" or "identity", indicating the type of
               document which can be verified using the given certificate. Defaults to
               "pkcs7".
        """
        pulumi.set(__self__, "aws_public_cert", aws_public_cert)
        pulumi.set(__self__, "cert_name", cert_name)
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="awsPublicCert")
    def aws_public_cert(self) -> pulumi.Input[str]:
        """
        The  Base64 encoded AWS Public key required to
        verify PKCS7 signature of the EC2 instance metadata. You can find this key in
        the [AWS
        documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        """
        return pulumi.get(self, "aws_public_cert")

    @aws_public_cert.setter
    def aws_public_cert(self, value: pulumi.Input[str]):
        pulumi.set(self, "aws_public_cert", value)

    @property
    @pulumi.getter(name="certName")
    def cert_name(self) -> pulumi.Input[str]:
        """
        The name of the certificate.
        """
        return pulumi.get(self, "cert_name")

    @cert_name.setter
    def cert_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cert_name", value)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input[str]]:
        """
        The path the AWS auth backend being configured was
        mounted at.  Defaults to `aws`.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend", value)

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
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Either "pkcs7" or "identity", indicating the type of
        document which can be verified using the given certificate. Defaults to
        "pkcs7".
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _AuthBackendCertState:
    def __init__(__self__, *,
                 aws_public_cert: Optional[pulumi.Input[str]] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 cert_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AuthBackendCert resources.
        :param pulumi.Input[str] aws_public_cert: The  Base64 encoded AWS Public key required to
               verify PKCS7 signature of the EC2 instance metadata. You can find this key in
               the [AWS
               documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        :param pulumi.Input[str] backend: The path the AWS auth backend being configured was
               mounted at.  Defaults to `aws`.
        :param pulumi.Input[str] cert_name: The name of the certificate.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] type: Either "pkcs7" or "identity", indicating the type of
               document which can be verified using the given certificate. Defaults to
               "pkcs7".
        """
        if aws_public_cert is not None:
            pulumi.set(__self__, "aws_public_cert", aws_public_cert)
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if cert_name is not None:
            pulumi.set(__self__, "cert_name", cert_name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="awsPublicCert")
    def aws_public_cert(self) -> Optional[pulumi.Input[str]]:
        """
        The  Base64 encoded AWS Public key required to
        verify PKCS7 signature of the EC2 instance metadata. You can find this key in
        the [AWS
        documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        """
        return pulumi.get(self, "aws_public_cert")

    @aws_public_cert.setter
    def aws_public_cert(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_public_cert", value)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input[str]]:
        """
        The path the AWS auth backend being configured was
        mounted at.  Defaults to `aws`.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter(name="certName")
    def cert_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the certificate.
        """
        return pulumi.get(self, "cert_name")

    @cert_name.setter
    def cert_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert_name", value)

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
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Either "pkcs7" or "identity", indicating the type of
        document which can be verified using the given certificate. Defaults to
        "pkcs7".
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class AuthBackendCert(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_public_cert: Optional[pulumi.Input[str]] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 cert_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ## Import

        AWS auth backend certificates can be imported using `auth/`, the `backend` path, `/config/certificate/`, and the `cert_name` e.g.

        ```sh
        $ pulumi import vault:aws/authBackendCert:AuthBackendCert example auth/aws/config/certificate/my-cert
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_public_cert: The  Base64 encoded AWS Public key required to
               verify PKCS7 signature of the EC2 instance metadata. You can find this key in
               the [AWS
               documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        :param pulumi.Input[str] backend: The path the AWS auth backend being configured was
               mounted at.  Defaults to `aws`.
        :param pulumi.Input[str] cert_name: The name of the certificate.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] type: Either "pkcs7" or "identity", indicating the type of
               document which can be verified using the given certificate. Defaults to
               "pkcs7".
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AuthBackendCertArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ## Import

        AWS auth backend certificates can be imported using `auth/`, the `backend` path, `/config/certificate/`, and the `cert_name` e.g.

        ```sh
        $ pulumi import vault:aws/authBackendCert:AuthBackendCert example auth/aws/config/certificate/my-cert
        ```

        :param str resource_name: The name of the resource.
        :param AuthBackendCertArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AuthBackendCertArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_public_cert: Optional[pulumi.Input[str]] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 cert_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AuthBackendCertArgs.__new__(AuthBackendCertArgs)

            if aws_public_cert is None and not opts.urn:
                raise TypeError("Missing required property 'aws_public_cert'")
            __props__.__dict__["aws_public_cert"] = aws_public_cert
            __props__.__dict__["backend"] = backend
            if cert_name is None and not opts.urn:
                raise TypeError("Missing required property 'cert_name'")
            __props__.__dict__["cert_name"] = cert_name
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["type"] = type
        super(AuthBackendCert, __self__).__init__(
            'vault:aws/authBackendCert:AuthBackendCert',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aws_public_cert: Optional[pulumi.Input[str]] = None,
            backend: Optional[pulumi.Input[str]] = None,
            cert_name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'AuthBackendCert':
        """
        Get an existing AuthBackendCert resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_public_cert: The  Base64 encoded AWS Public key required to
               verify PKCS7 signature of the EC2 instance metadata. You can find this key in
               the [AWS
               documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        :param pulumi.Input[str] backend: The path the AWS auth backend being configured was
               mounted at.  Defaults to `aws`.
        :param pulumi.Input[str] cert_name: The name of the certificate.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[str] type: Either "pkcs7" or "identity", indicating the type of
               document which can be verified using the given certificate. Defaults to
               "pkcs7".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AuthBackendCertState.__new__(_AuthBackendCertState)

        __props__.__dict__["aws_public_cert"] = aws_public_cert
        __props__.__dict__["backend"] = backend
        __props__.__dict__["cert_name"] = cert_name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["type"] = type
        return AuthBackendCert(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsPublicCert")
    def aws_public_cert(self) -> pulumi.Output[str]:
        """
        The  Base64 encoded AWS Public key required to
        verify PKCS7 signature of the EC2 instance metadata. You can find this key in
        the [AWS
        documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html).
        """
        return pulumi.get(self, "aws_public_cert")

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Output[Optional[str]]:
        """
        The path the AWS auth backend being configured was
        mounted at.  Defaults to `aws`.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter(name="certName")
    def cert_name(self) -> pulumi.Output[str]:
        """
        The name of the certificate.
        """
        return pulumi.get(self, "cert_name")

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
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Either "pkcs7" or "identity", indicating the type of
        document which can be verified using the given certificate. Defaults to
        "pkcs7".
        """
        return pulumi.get(self, "type")

