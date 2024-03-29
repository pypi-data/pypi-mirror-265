'''
# `data_databricks_spark_version`

Refer to the Terraform Registry for docs: [`data_databricks_spark_version`](https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version).
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


class DataDatabricksSparkVersion(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksSparkVersion.DataDatabricksSparkVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version databricks_spark_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        beta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        genomics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        graviton: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        long_term_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ml: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        photon: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scala: typing.Optional[builtins.str] = None,
        spark_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version databricks_spark_version} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param beta: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#beta DataDatabricksSparkVersion#beta}.
        :param genomics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#genomics DataDatabricksSparkVersion#genomics}.
        :param gpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#gpu DataDatabricksSparkVersion#gpu}.
        :param graviton: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#graviton DataDatabricksSparkVersion#graviton}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#id DataDatabricksSparkVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#latest DataDatabricksSparkVersion#latest}.
        :param long_term_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#long_term_support DataDatabricksSparkVersion#long_term_support}.
        :param ml: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#ml DataDatabricksSparkVersion#ml}.
        :param photon: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#photon DataDatabricksSparkVersion#photon}.
        :param scala: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#scala DataDatabricksSparkVersion#scala}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#spark_version DataDatabricksSparkVersion#spark_version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0181c5a45a5659d7fbf3b2b58446fc9013cc16e7920b8f32fb436a6ff33e95c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataDatabricksSparkVersionConfig(
            beta=beta,
            genomics=genomics,
            gpu=gpu,
            graviton=graviton,
            id=id,
            latest=latest,
            long_term_support=long_term_support,
            ml=ml,
            photon=photon,
            scala=scala,
            spark_version=spark_version,
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
        '''Generates CDKTF code for importing a DataDatabricksSparkVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatabricksSparkVersion to import.
        :param import_from_id: The id of the existing DataDatabricksSparkVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatabricksSparkVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beab5dca685c348679869c38e302dcb2c15faf257f1533c0df817b09d1c3c086)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBeta")
    def reset_beta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeta", []))

    @jsii.member(jsii_name="resetGenomics")
    def reset_genomics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenomics", []))

    @jsii.member(jsii_name="resetGpu")
    def reset_gpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpu", []))

    @jsii.member(jsii_name="resetGraviton")
    def reset_graviton(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraviton", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLatest")
    def reset_latest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatest", []))

    @jsii.member(jsii_name="resetLongTermSupport")
    def reset_long_term_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongTermSupport", []))

    @jsii.member(jsii_name="resetMl")
    def reset_ml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMl", []))

    @jsii.member(jsii_name="resetPhoton")
    def reset_photon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoton", []))

    @jsii.member(jsii_name="resetScala")
    def reset_scala(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScala", []))

    @jsii.member(jsii_name="resetSparkVersion")
    def reset_spark_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkVersion", []))

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
    @jsii.member(jsii_name="betaInput")
    def beta_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "betaInput"))

    @builtins.property
    @jsii.member(jsii_name="genomicsInput")
    def genomics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "genomicsInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuInput")
    def gpu_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gpuInput"))

    @builtins.property
    @jsii.member(jsii_name="gravitonInput")
    def graviton_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gravitonInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="latestInput")
    def latest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "latestInput"))

    @builtins.property
    @jsii.member(jsii_name="longTermSupportInput")
    def long_term_support_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "longTermSupportInput"))

    @builtins.property
    @jsii.member(jsii_name="mlInput")
    def ml_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mlInput"))

    @builtins.property
    @jsii.member(jsii_name="photonInput")
    def photon_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "photonInput"))

    @builtins.property
    @jsii.member(jsii_name="scalaInput")
    def scala_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalaInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkVersionInput")
    def spark_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="beta")
    def beta(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "beta"))

    @beta.setter
    def beta(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcab29d0fc1841f3271037f7ed5ce946893dc2e0dfb521b914353d6db33235ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beta", value)

    @builtins.property
    @jsii.member(jsii_name="genomics")
    def genomics(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "genomics"))

    @genomics.setter
    def genomics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bebb9aa82168eb7e07f9a5408cdc556acb0142d9f4de2a20ac8949dcebcc51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "genomics", value)

    @builtins.property
    @jsii.member(jsii_name="gpu")
    def gpu(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gpu"))

    @gpu.setter
    def gpu(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aded48bad9d2fba03f4ba62976a4542b1d08703df7e2bea848b9b0732de64060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpu", value)

    @builtins.property
    @jsii.member(jsii_name="graviton")
    def graviton(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "graviton"))

    @graviton.setter
    def graviton(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21058913707a86f77cae647fd760ec1b219a38771cac89952ded9ea45e2dc7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graviton", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba622e2e533d2f3bb7bb45bcf174d949234631727a92908cb45cfde636b074e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="latest")
    def latest(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "latest"))

    @latest.setter
    def latest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edab619cf2dd0acbefd4347b986298d947cc07737ec4be8a477aea1a79ea80b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latest", value)

    @builtins.property
    @jsii.member(jsii_name="longTermSupport")
    def long_term_support(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "longTermSupport"))

    @long_term_support.setter
    def long_term_support(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890e4149578f83715f11a1379ffbdf287dff7b272cb007edecc94a9bde29b9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longTermSupport", value)

    @builtins.property
    @jsii.member(jsii_name="ml")
    def ml(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ml"))

    @ml.setter
    def ml(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b47b2cb242f37e0103eaefd951d1c0a430c031365f170f5474d948bef4b510f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ml", value)

    @builtins.property
    @jsii.member(jsii_name="photon")
    def photon(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "photon"))

    @photon.setter
    def photon(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2f7b815c942bcdfb0109eb08b8e3fc2364499a40f02ea95c203b8c8fdcffe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "photon", value)

    @builtins.property
    @jsii.member(jsii_name="scala")
    def scala(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scala"))

    @scala.setter
    def scala(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef4c9a7c6b599529fdb9e83977b4990e27f426cbf38df82479862c9fec36567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scala", value)

    @builtins.property
    @jsii.member(jsii_name="sparkVersion")
    def spark_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkVersion"))

    @spark_version.setter
    def spark_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e2ab2cfcb8b1d7162c9e62818aa863ac01737422300913542c3d29ca9d98f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkVersion", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksSparkVersion.DataDatabricksSparkVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "beta": "beta",
        "genomics": "genomics",
        "gpu": "gpu",
        "graviton": "graviton",
        "id": "id",
        "latest": "latest",
        "long_term_support": "longTermSupport",
        "ml": "ml",
        "photon": "photon",
        "scala": "scala",
        "spark_version": "sparkVersion",
    },
)
class DataDatabricksSparkVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        beta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        genomics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        graviton: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        long_term_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ml: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        photon: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scala: typing.Optional[builtins.str] = None,
        spark_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param beta: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#beta DataDatabricksSparkVersion#beta}.
        :param genomics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#genomics DataDatabricksSparkVersion#genomics}.
        :param gpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#gpu DataDatabricksSparkVersion#gpu}.
        :param graviton: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#graviton DataDatabricksSparkVersion#graviton}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#id DataDatabricksSparkVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#latest DataDatabricksSparkVersion#latest}.
        :param long_term_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#long_term_support DataDatabricksSparkVersion#long_term_support}.
        :param ml: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#ml DataDatabricksSparkVersion#ml}.
        :param photon: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#photon DataDatabricksSparkVersion#photon}.
        :param scala: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#scala DataDatabricksSparkVersion#scala}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#spark_version DataDatabricksSparkVersion#spark_version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8e67ff00f2bc9c0eb2318699b5489049ac5d6b43ff04257d0a47ef7ae651ab)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument beta", value=beta, expected_type=type_hints["beta"])
            check_type(argname="argument genomics", value=genomics, expected_type=type_hints["genomics"])
            check_type(argname="argument gpu", value=gpu, expected_type=type_hints["gpu"])
            check_type(argname="argument graviton", value=graviton, expected_type=type_hints["graviton"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument latest", value=latest, expected_type=type_hints["latest"])
            check_type(argname="argument long_term_support", value=long_term_support, expected_type=type_hints["long_term_support"])
            check_type(argname="argument ml", value=ml, expected_type=type_hints["ml"])
            check_type(argname="argument photon", value=photon, expected_type=type_hints["photon"])
            check_type(argname="argument scala", value=scala, expected_type=type_hints["scala"])
            check_type(argname="argument spark_version", value=spark_version, expected_type=type_hints["spark_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if beta is not None:
            self._values["beta"] = beta
        if genomics is not None:
            self._values["genomics"] = genomics
        if gpu is not None:
            self._values["gpu"] = gpu
        if graviton is not None:
            self._values["graviton"] = graviton
        if id is not None:
            self._values["id"] = id
        if latest is not None:
            self._values["latest"] = latest
        if long_term_support is not None:
            self._values["long_term_support"] = long_term_support
        if ml is not None:
            self._values["ml"] = ml
        if photon is not None:
            self._values["photon"] = photon
        if scala is not None:
            self._values["scala"] = scala
        if spark_version is not None:
            self._values["spark_version"] = spark_version

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
    def beta(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#beta DataDatabricksSparkVersion#beta}.'''
        result = self._values.get("beta")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def genomics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#genomics DataDatabricksSparkVersion#genomics}.'''
        result = self._values.get("genomics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gpu(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#gpu DataDatabricksSparkVersion#gpu}.'''
        result = self._values.get("gpu")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def graviton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#graviton DataDatabricksSparkVersion#graviton}.'''
        result = self._values.get("graviton")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#id DataDatabricksSparkVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#latest DataDatabricksSparkVersion#latest}.'''
        result = self._values.get("latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def long_term_support(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#long_term_support DataDatabricksSparkVersion#long_term_support}.'''
        result = self._values.get("long_term_support")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ml(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#ml DataDatabricksSparkVersion#ml}.'''
        result = self._values.get("ml")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def photon(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#photon DataDatabricksSparkVersion#photon}.'''
        result = self._values.get("photon")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scala(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#scala DataDatabricksSparkVersion#scala}.'''
        result = self._values.get("scala")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.39.0/docs/data-sources/spark_version#spark_version DataDatabricksSparkVersion#spark_version}.'''
        result = self._values.get("spark_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksSparkVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataDatabricksSparkVersion",
    "DataDatabricksSparkVersionConfig",
]

publication.publish()

def _typecheckingstub__0181c5a45a5659d7fbf3b2b58446fc9013cc16e7920b8f32fb436a6ff33e95c4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    beta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    genomics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    graviton: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    long_term_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ml: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    photon: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scala: typing.Optional[builtins.str] = None,
    spark_version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__beab5dca685c348679869c38e302dcb2c15faf257f1533c0df817b09d1c3c086(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcab29d0fc1841f3271037f7ed5ce946893dc2e0dfb521b914353d6db33235ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bebb9aa82168eb7e07f9a5408cdc556acb0142d9f4de2a20ac8949dcebcc51b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aded48bad9d2fba03f4ba62976a4542b1d08703df7e2bea848b9b0732de64060(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21058913707a86f77cae647fd760ec1b219a38771cac89952ded9ea45e2dc7a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba622e2e533d2f3bb7bb45bcf174d949234631727a92908cb45cfde636b074e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edab619cf2dd0acbefd4347b986298d947cc07737ec4be8a477aea1a79ea80b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890e4149578f83715f11a1379ffbdf287dff7b272cb007edecc94a9bde29b9cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b47b2cb242f37e0103eaefd951d1c0a430c031365f170f5474d948bef4b510f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2f7b815c942bcdfb0109eb08b8e3fc2364499a40f02ea95c203b8c8fdcffe8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef4c9a7c6b599529fdb9e83977b4990e27f426cbf38df82479862c9fec36567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e2ab2cfcb8b1d7162c9e62818aa863ac01737422300913542c3d29ca9d98f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8e67ff00f2bc9c0eb2318699b5489049ac5d6b43ff04257d0a47ef7ae651ab(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    beta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    genomics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    graviton: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    long_term_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ml: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    photon: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scala: typing.Optional[builtins.str] = None,
    spark_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
