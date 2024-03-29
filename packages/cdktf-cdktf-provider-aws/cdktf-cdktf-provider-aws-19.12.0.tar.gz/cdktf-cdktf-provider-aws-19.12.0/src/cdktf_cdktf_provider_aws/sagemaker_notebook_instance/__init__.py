'''
# `aws_sagemaker_notebook_instance`

Refer to the Terraform Registry for docs: [`aws_sagemaker_notebook_instance`](https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class SagemakerNotebookInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerNotebookInstance.SagemakerNotebookInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance aws_sagemaker_notebook_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_code_repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_code_repository: typing.Optional[builtins.str] = None,
        direct_internet_access: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_metadata_service_configuration: typing.Optional[typing.Union["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_config_name: typing.Optional[builtins.str] = None,
        platform_identifier: typing.Optional[builtins.str] = None,
        root_access: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance aws_sagemaker_notebook_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_type SagemakerNotebookInstance#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#name SagemakerNotebookInstance#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#role_arn SagemakerNotebookInstance#role_arn}.
        :param accelerator_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#accelerator_types SagemakerNotebookInstance#accelerator_types}.
        :param additional_code_repositories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#additional_code_repositories SagemakerNotebookInstance#additional_code_repositories}.
        :param default_code_repository: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#default_code_repository SagemakerNotebookInstance#default_code_repository}.
        :param direct_internet_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#direct_internet_access SagemakerNotebookInstance#direct_internet_access}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#id SagemakerNotebookInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_metadata_service_configuration: instance_metadata_service_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_metadata_service_configuration SagemakerNotebookInstance#instance_metadata_service_configuration}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#kms_key_id SagemakerNotebookInstance#kms_key_id}.
        :param lifecycle_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#lifecycle_config_name SagemakerNotebookInstance#lifecycle_config_name}.
        :param platform_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#platform_identifier SagemakerNotebookInstance#platform_identifier}.
        :param root_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#root_access SagemakerNotebookInstance#root_access}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#security_groups SagemakerNotebookInstance#security_groups}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#subnet_id SagemakerNotebookInstance#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags SagemakerNotebookInstance#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags_all SagemakerNotebookInstance#tags_all}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#volume_size SagemakerNotebookInstance#volume_size}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9278225b8d02238297f7e0cf936c8e8cdaac00e5c51edf20fd8ec047530b782)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerNotebookInstanceConfig(
            instance_type=instance_type,
            name=name,
            role_arn=role_arn,
            accelerator_types=accelerator_types,
            additional_code_repositories=additional_code_repositories,
            default_code_repository=default_code_repository,
            direct_internet_access=direct_internet_access,
            id=id,
            instance_metadata_service_configuration=instance_metadata_service_configuration,
            kms_key_id=kms_key_id,
            lifecycle_config_name=lifecycle_config_name,
            platform_identifier=platform_identifier,
            root_access=root_access,
            security_groups=security_groups,
            subnet_id=subnet_id,
            tags=tags,
            tags_all=tags_all,
            volume_size=volume_size,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SagemakerNotebookInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerNotebookInstance to import.
        :param import_from_id: The id of the existing SagemakerNotebookInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerNotebookInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af48a8b07f42411f9528104bde051824c7815c4a7a6375747b1c80083ee017b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstanceMetadataServiceConfiguration")
    def put_instance_metadata_service_configuration(
        self,
        *,
        minimum_instance_metadata_service_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimum_instance_metadata_service_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#minimum_instance_metadata_service_version SagemakerNotebookInstance#minimum_instance_metadata_service_version}.
        '''
        value = SagemakerNotebookInstanceInstanceMetadataServiceConfiguration(
            minimum_instance_metadata_service_version=minimum_instance_metadata_service_version,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceMetadataServiceConfiguration", [value]))

    @jsii.member(jsii_name="resetAcceleratorTypes")
    def reset_accelerator_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorTypes", []))

    @jsii.member(jsii_name="resetAdditionalCodeRepositories")
    def reset_additional_code_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalCodeRepositories", []))

    @jsii.member(jsii_name="resetDefaultCodeRepository")
    def reset_default_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultCodeRepository", []))

    @jsii.member(jsii_name="resetDirectInternetAccess")
    def reset_direct_internet_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectInternetAccess", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceMetadataServiceConfiguration")
    def reset_instance_metadata_service_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceMetadataServiceConfiguration", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetLifecycleConfigName")
    def reset_lifecycle_config_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigName", []))

    @jsii.member(jsii_name="resetPlatformIdentifier")
    def reset_platform_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformIdentifier", []))

    @jsii.member(jsii_name="resetRootAccess")
    def reset_root_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootAccess", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="instanceMetadataServiceConfiguration")
    def instance_metadata_service_configuration(
        self,
    ) -> "SagemakerNotebookInstanceInstanceMetadataServiceConfigurationOutputReference":
        return typing.cast("SagemakerNotebookInstanceInstanceMetadataServiceConfigurationOutputReference", jsii.get(self, "instanceMetadataServiceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceId")
    def network_interface_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkInterfaceId"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypesInput")
    def accelerator_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceleratorTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalCodeRepositoriesInput")
    def additional_code_repositories_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalCodeRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCodeRepositoryInput")
    def default_code_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultCodeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="directInternetAccessInput")
    def direct_internet_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directInternetAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceMetadataServiceConfigurationInput")
    def instance_metadata_service_configuration_input(
        self,
    ) -> typing.Optional["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration"]:
        return typing.cast(typing.Optional["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration"], jsii.get(self, "instanceMetadataServiceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigNameInput")
    def lifecycle_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="platformIdentifierInput")
    def platform_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="rootAccessInput")
    def root_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypes")
    def accelerator_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceleratorTypes"))

    @accelerator_types.setter
    def accelerator_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b250cc606bcc606b1ca32d91c1e1478fa442a809fde968c775223c1721a3192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorTypes", value)

    @builtins.property
    @jsii.member(jsii_name="additionalCodeRepositories")
    def additional_code_repositories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalCodeRepositories"))

    @additional_code_repositories.setter
    def additional_code_repositories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ea0ecb9ce9901d6ef7b95a0506c4a989ad3950e0de279fa6431e2706f3bfa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalCodeRepositories", value)

    @builtins.property
    @jsii.member(jsii_name="defaultCodeRepository")
    def default_code_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultCodeRepository"))

    @default_code_repository.setter
    def default_code_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fe391562e827cc1f660a399b28b0f06aee4b5cfcf0f750efe1320b1766c94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultCodeRepository", value)

    @builtins.property
    @jsii.member(jsii_name="directInternetAccess")
    def direct_internet_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directInternetAccess"))

    @direct_internet_access.setter
    def direct_internet_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a9a9b571680becbd25aee34e4cdbd8c9c3a4e40dfe60b83913faa9c70c0d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directInternetAccess", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa303cc3d20431d0edb9b3eeb557336fefe211a18b6ba2a110f71340eeece77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b4c07c4675ad9b9d777855f538718b02b924e0fcab06e8c0b396e21eeecba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279f8c5e44209fe6396ad2d7a4d5bb19d4b88b3370f70c51320d9afe2cbc14c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigName")
    def lifecycle_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigName"))

    @lifecycle_config_name.setter
    def lifecycle_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93166588a30951012cd463f11606b7b7230c3a3f873379f58470e236bd58409b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86f2178cf21fa9f2aee66294b7654d4b2c2888ea33f84ebd507a70621287bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="platformIdentifier")
    def platform_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformIdentifier"))

    @platform_identifier.setter
    def platform_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555c27d9e157a2a19b91ca944ec6ebdbd58f02802d08f2f532618b2bf0e900f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbcef9c61db37549772e9cb5ae8dcb606fcfe76e7369381a3f52fd18ece94d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="rootAccess")
    def root_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootAccess"))

    @root_access.setter
    def root_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e8dd333eb50eb8889a0e47a28d7314fc4e2c6596c0f56386a8a25939dd6982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootAccess", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f9618e3ffa188f7adbaa4dd5d93ab5ff1f9927ec56a09509400996ff74fa83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2724db6c01661868cf50bfc48adb2900326281080e57071e71f2cd212eb3207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a097bfac8c0ecbe1aa1e212ae03d24c39ecf2b8c205ff2bdfa275ccd049c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa379d878912f9f601bc891c4fb58ef439db4a9155082e03bea16e6a0b8ffa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5911059cd512e3645e2d7efb2e1a2c94ee1af4f8e6a96e607089709a6c69745a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerNotebookInstance.SagemakerNotebookInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_type": "instanceType",
        "name": "name",
        "role_arn": "roleArn",
        "accelerator_types": "acceleratorTypes",
        "additional_code_repositories": "additionalCodeRepositories",
        "default_code_repository": "defaultCodeRepository",
        "direct_internet_access": "directInternetAccess",
        "id": "id",
        "instance_metadata_service_configuration": "instanceMetadataServiceConfiguration",
        "kms_key_id": "kmsKeyId",
        "lifecycle_config_name": "lifecycleConfigName",
        "platform_identifier": "platformIdentifier",
        "root_access": "rootAccess",
        "security_groups": "securityGroups",
        "subnet_id": "subnetId",
        "tags": "tags",
        "tags_all": "tagsAll",
        "volume_size": "volumeSize",
    },
)
class SagemakerNotebookInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_type: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_code_repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_code_repository: typing.Optional[builtins.str] = None,
        direct_internet_access: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_metadata_service_configuration: typing.Optional[typing.Union["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_config_name: typing.Optional[builtins.str] = None,
        platform_identifier: typing.Optional[builtins.str] = None,
        root_access: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        volume_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_type SagemakerNotebookInstance#instance_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#name SagemakerNotebookInstance#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#role_arn SagemakerNotebookInstance#role_arn}.
        :param accelerator_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#accelerator_types SagemakerNotebookInstance#accelerator_types}.
        :param additional_code_repositories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#additional_code_repositories SagemakerNotebookInstance#additional_code_repositories}.
        :param default_code_repository: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#default_code_repository SagemakerNotebookInstance#default_code_repository}.
        :param direct_internet_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#direct_internet_access SagemakerNotebookInstance#direct_internet_access}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#id SagemakerNotebookInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_metadata_service_configuration: instance_metadata_service_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_metadata_service_configuration SagemakerNotebookInstance#instance_metadata_service_configuration}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#kms_key_id SagemakerNotebookInstance#kms_key_id}.
        :param lifecycle_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#lifecycle_config_name SagemakerNotebookInstance#lifecycle_config_name}.
        :param platform_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#platform_identifier SagemakerNotebookInstance#platform_identifier}.
        :param root_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#root_access SagemakerNotebookInstance#root_access}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#security_groups SagemakerNotebookInstance#security_groups}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#subnet_id SagemakerNotebookInstance#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags SagemakerNotebookInstance#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags_all SagemakerNotebookInstance#tags_all}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#volume_size SagemakerNotebookInstance#volume_size}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_metadata_service_configuration, dict):
            instance_metadata_service_configuration = SagemakerNotebookInstanceInstanceMetadataServiceConfiguration(**instance_metadata_service_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e759764af10b7036715a8ad9137130cd47d3db6d0472cf99493e010d4b4a19)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument accelerator_types", value=accelerator_types, expected_type=type_hints["accelerator_types"])
            check_type(argname="argument additional_code_repositories", value=additional_code_repositories, expected_type=type_hints["additional_code_repositories"])
            check_type(argname="argument default_code_repository", value=default_code_repository, expected_type=type_hints["default_code_repository"])
            check_type(argname="argument direct_internet_access", value=direct_internet_access, expected_type=type_hints["direct_internet_access"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_metadata_service_configuration", value=instance_metadata_service_configuration, expected_type=type_hints["instance_metadata_service_configuration"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument lifecycle_config_name", value=lifecycle_config_name, expected_type=type_hints["lifecycle_config_name"])
            check_type(argname="argument platform_identifier", value=platform_identifier, expected_type=type_hints["platform_identifier"])
            check_type(argname="argument root_access", value=root_access, expected_type=type_hints["root_access"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "name": name,
            "role_arn": role_arn,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if accelerator_types is not None:
            self._values["accelerator_types"] = accelerator_types
        if additional_code_repositories is not None:
            self._values["additional_code_repositories"] = additional_code_repositories
        if default_code_repository is not None:
            self._values["default_code_repository"] = default_code_repository
        if direct_internet_access is not None:
            self._values["direct_internet_access"] = direct_internet_access
        if id is not None:
            self._values["id"] = id
        if instance_metadata_service_configuration is not None:
            self._values["instance_metadata_service_configuration"] = instance_metadata_service_configuration
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if lifecycle_config_name is not None:
            self._values["lifecycle_config_name"] = lifecycle_config_name
        if platform_identifier is not None:
            self._values["platform_identifier"] = platform_identifier
        if root_access is not None:
            self._values["root_access"] = root_access
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if volume_size is not None:
            self._values["volume_size"] = volume_size

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_type SagemakerNotebookInstance#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#name SagemakerNotebookInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#role_arn SagemakerNotebookInstance#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#accelerator_types SagemakerNotebookInstance#accelerator_types}.'''
        result = self._values.get("accelerator_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_code_repositories(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#additional_code_repositories SagemakerNotebookInstance#additional_code_repositories}.'''
        result = self._values.get("additional_code_repositories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_code_repository(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#default_code_repository SagemakerNotebookInstance#default_code_repository}.'''
        result = self._values.get("default_code_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direct_internet_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#direct_internet_access SagemakerNotebookInstance#direct_internet_access}.'''
        result = self._values.get("direct_internet_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#id SagemakerNotebookInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_metadata_service_configuration(
        self,
    ) -> typing.Optional["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration"]:
        '''instance_metadata_service_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#instance_metadata_service_configuration SagemakerNotebookInstance#instance_metadata_service_configuration}
        '''
        result = self._values.get("instance_metadata_service_configuration")
        return typing.cast(typing.Optional["SagemakerNotebookInstanceInstanceMetadataServiceConfiguration"], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#kms_key_id SagemakerNotebookInstance#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#lifecycle_config_name SagemakerNotebookInstance#lifecycle_config_name}.'''
        result = self._values.get("lifecycle_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#platform_identifier SagemakerNotebookInstance#platform_identifier}.'''
        result = self._values.get("platform_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#root_access SagemakerNotebookInstance#root_access}.'''
        result = self._values.get("root_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#security_groups SagemakerNotebookInstance#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#subnet_id SagemakerNotebookInstance#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags SagemakerNotebookInstance#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#tags_all SagemakerNotebookInstance#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#volume_size SagemakerNotebookInstance#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerNotebookInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerNotebookInstance.SagemakerNotebookInstanceInstanceMetadataServiceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_instance_metadata_service_version": "minimumInstanceMetadataServiceVersion",
    },
)
class SagemakerNotebookInstanceInstanceMetadataServiceConfiguration:
    def __init__(
        self,
        *,
        minimum_instance_metadata_service_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimum_instance_metadata_service_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#minimum_instance_metadata_service_version SagemakerNotebookInstance#minimum_instance_metadata_service_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19655080fdcfc6bb8dc2eb567c3b4d0e950449d7392a2d516930c79066fa0026)
            check_type(argname="argument minimum_instance_metadata_service_version", value=minimum_instance_metadata_service_version, expected_type=type_hints["minimum_instance_metadata_service_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum_instance_metadata_service_version is not None:
            self._values["minimum_instance_metadata_service_version"] = minimum_instance_metadata_service_version

    @builtins.property
    def minimum_instance_metadata_service_version(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.43.0/docs/resources/sagemaker_notebook_instance#minimum_instance_metadata_service_version SagemakerNotebookInstance#minimum_instance_metadata_service_version}.'''
        result = self._values.get("minimum_instance_metadata_service_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerNotebookInstanceInstanceMetadataServiceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerNotebookInstanceInstanceMetadataServiceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerNotebookInstance.SagemakerNotebookInstanceInstanceMetadataServiceConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbe35adbf3f1a77a3b2493c9185f4f29839396c2ca48265097c50d6c9d83a50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinimumInstanceMetadataServiceVersion")
    def reset_minimum_instance_metadata_service_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumInstanceMetadataServiceVersion", []))

    @builtins.property
    @jsii.member(jsii_name="minimumInstanceMetadataServiceVersionInput")
    def minimum_instance_metadata_service_version_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumInstanceMetadataServiceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumInstanceMetadataServiceVersion")
    def minimum_instance_metadata_service_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumInstanceMetadataServiceVersion"))

    @minimum_instance_metadata_service_version.setter
    def minimum_instance_metadata_service_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18774ef3b784533841162ffb3de3ae87050f72adf47362138f4cf36514ce280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumInstanceMetadataServiceVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration]:
        return typing.cast(typing.Optional[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784997e3d8a3328beec98be319eec4fb31f1128eb776016b597342427f763d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerNotebookInstance",
    "SagemakerNotebookInstanceConfig",
    "SagemakerNotebookInstanceInstanceMetadataServiceConfiguration",
    "SagemakerNotebookInstanceInstanceMetadataServiceConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__c9278225b8d02238297f7e0cf936c8e8cdaac00e5c51edf20fd8ec047530b782(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_type: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_code_repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_code_repository: typing.Optional[builtins.str] = None,
    direct_internet_access: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_metadata_service_configuration: typing.Optional[typing.Union[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    lifecycle_config_name: typing.Optional[builtins.str] = None,
    platform_identifier: typing.Optional[builtins.str] = None,
    root_access: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af48a8b07f42411f9528104bde051824c7815c4a7a6375747b1c80083ee017b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b250cc606bcc606b1ca32d91c1e1478fa442a809fde968c775223c1721a3192(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ea0ecb9ce9901d6ef7b95a0506c4a989ad3950e0de279fa6431e2706f3bfa1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fe391562e827cc1f660a399b28b0f06aee4b5cfcf0f750efe1320b1766c94f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a9a9b571680becbd25aee34e4cdbd8c9c3a4e40dfe60b83913faa9c70c0d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa303cc3d20431d0edb9b3eeb557336fefe211a18b6ba2a110f71340eeece77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b4c07c4675ad9b9d777855f538718b02b924e0fcab06e8c0b396e21eeecba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279f8c5e44209fe6396ad2d7a4d5bb19d4b88b3370f70c51320d9afe2cbc14c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93166588a30951012cd463f11606b7b7230c3a3f873379f58470e236bd58409b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86f2178cf21fa9f2aee66294b7654d4b2c2888ea33f84ebd507a70621287bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555c27d9e157a2a19b91ca944ec6ebdbd58f02802d08f2f532618b2bf0e900f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcef9c61db37549772e9cb5ae8dcb606fcfe76e7369381a3f52fd18ece94d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e8dd333eb50eb8889a0e47a28d7314fc4e2c6596c0f56386a8a25939dd6982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f9618e3ffa188f7adbaa4dd5d93ab5ff1f9927ec56a09509400996ff74fa83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2724db6c01661868cf50bfc48adb2900326281080e57071e71f2cd212eb3207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a097bfac8c0ecbe1aa1e212ae03d24c39ecf2b8c205ff2bdfa275ccd049c24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa379d878912f9f601bc891c4fb58ef439db4a9155082e03bea16e6a0b8ffa0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5911059cd512e3645e2d7efb2e1a2c94ee1af4f8e6a96e607089709a6c69745a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e759764af10b7036715a8ad9137130cd47d3db6d0472cf99493e010d4b4a19(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_type: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_code_repositories: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_code_repository: typing.Optional[builtins.str] = None,
    direct_internet_access: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_metadata_service_configuration: typing.Optional[typing.Union[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    lifecycle_config_name: typing.Optional[builtins.str] = None,
    platform_identifier: typing.Optional[builtins.str] = None,
    root_access: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    volume_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19655080fdcfc6bb8dc2eb567c3b4d0e950449d7392a2d516930c79066fa0026(
    *,
    minimum_instance_metadata_service_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbe35adbf3f1a77a3b2493c9185f4f29839396c2ca48265097c50d6c9d83a50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18774ef3b784533841162ffb3de3ae87050f72adf47362138f4cf36514ce280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784997e3d8a3328beec98be319eec4fb31f1128eb776016b597342427f763d12(
    value: typing.Optional[SagemakerNotebookInstanceInstanceMetadataServiceConfiguration],
) -> None:
    """Type checking stubs"""
    pass
