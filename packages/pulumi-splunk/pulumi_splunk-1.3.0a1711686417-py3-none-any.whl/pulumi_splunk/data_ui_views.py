# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['DataUiViewsArgs', 'DataUiViews']

@pulumi.input_type
class DataUiViewsArgs:
    def __init__(__self__, *,
                 eai_data: pulumi.Input[str],
                 acl: Optional[pulumi.Input['DataUiViewsAclArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataUiViews resource.
        :param pulumi.Input[str] eai_data: Dashboard XML definition.
        :param pulumi.Input[str] name: Dashboard name.
               * `eai:data` - (Required) Dashboard XML definition.
        """
        pulumi.set(__self__, "eai_data", eai_data)
        if acl is not None:
            pulumi.set(__self__, "acl", acl)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="eaiData")
    def eai_data(self) -> pulumi.Input[str]:
        """
        Dashboard XML definition.
        """
        return pulumi.get(self, "eai_data")

    @eai_data.setter
    def eai_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "eai_data", value)

    @property
    @pulumi.getter
    def acl(self) -> Optional[pulumi.Input['DataUiViewsAclArgs']]:
        return pulumi.get(self, "acl")

    @acl.setter
    def acl(self, value: Optional[pulumi.Input['DataUiViewsAclArgs']]):
        pulumi.set(self, "acl", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Dashboard name.
        * `eai:data` - (Required) Dashboard XML definition.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _DataUiViewsState:
    def __init__(__self__, *,
                 acl: Optional[pulumi.Input['DataUiViewsAclArgs']] = None,
                 eai_data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DataUiViews resources.
        :param pulumi.Input[str] eai_data: Dashboard XML definition.
        :param pulumi.Input[str] name: Dashboard name.
               * `eai:data` - (Required) Dashboard XML definition.
        """
        if acl is not None:
            pulumi.set(__self__, "acl", acl)
        if eai_data is not None:
            pulumi.set(__self__, "eai_data", eai_data)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def acl(self) -> Optional[pulumi.Input['DataUiViewsAclArgs']]:
        return pulumi.get(self, "acl")

    @acl.setter
    def acl(self, value: Optional[pulumi.Input['DataUiViewsAclArgs']]):
        pulumi.set(self, "acl", value)

    @property
    @pulumi.getter(name="eaiData")
    def eai_data(self) -> Optional[pulumi.Input[str]]:
        """
        Dashboard XML definition.
        """
        return pulumi.get(self, "eai_data")

    @eai_data.setter
    def eai_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eai_data", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Dashboard name.
        * `eai:data` - (Required) Dashboard XML definition.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class DataUiViews(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl: Optional[pulumi.Input[pulumi.InputType['DataUiViewsAclArgs']]] = None,
                 eai_data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## # Resource: DataUiViews

        Create and manage splunk dashboards/views.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_splunk as splunk

        dashboard = splunk.DataUiViews("dashboard",
            acl=splunk.DataUiViewsAclArgs(
                app="search",
                owner="admin",
            ),
            eai_data="<dashboard version=\\"1.1\\"><label>Terraform</label><description>Terraform operations</description><row><panel><chart><search><query>index=_internal sourcetype=splunkd_access useragent=\\"splunk-simple-go-client\\" | timechart fixedrange=f values(status) by uri_path</query><earliest>-24h@h</earliest><latest>now</latest><sampleRatio>1</sampleRatio></search><option name=\\"charting.axisLabelsX.majorLabelStyle.overflowMode\\">ellipsisNone</option><option name=\\"charting.axisLabelsX.majorLabelStyle.rotation\\">0</option><option name=\\"charting.axisTitleX.visibility\\">collapsed</option><option name=\\"charting.axisTitleY.text\\">HTTP status codes</option><option name=\\"charting.axisTitleY.visibility\\">visible</option><option name=\\"charting.axisTitleY2.visibility\\">visible</option><option name=\\"charting.axisX.abbreviation\\">none</option><option name=\\"charting.axisX.scale\\">linear</option><option name=\\"charting.axisY.abbreviation\\">none</option><option name=\\"charting.axisY.scale\\">linear</option><option name=\\"charting.axisY2.abbreviation\\">none</option><option name=\\"charting.axisY2.enabled\\">0</option><option name=\\"charting.axisY2.scale\\">inherit</option><option name=\\"charting.chart\\">column</option><option name=\\"charting.chart.bubbleMaximumSize\\">50</option><option name=\\"charting.chart.bubbleMinimumSize\\">10</option><option name=\\"charting.chart.bubbleSizeBy\\">area</option><option name=\\"charting.chart.nullValueMode\\">connect</option><option name=\\"charting.chart.showDataLabels\\">none</option><option name=\\"charting.chart.sliceCollapsingThreshold\\">0.01</option><option name=\\"charting.chart.stackMode\\">default</option><option name=\\"charting.chart.style\\">shiny</option><option name=\\"charting.drilldown\\">none</option><option name=\\"charting.layout.splitSeries\\">0</option><option name=\\"charting.layout.splitSeries.allowIndependentYRanges\\">0</option><option name=\\"charting.legend.labelStyle.overflowMode\\">ellipsisMiddle</option><option name=\\"charting.legend.mode\\">standard</option><option name=\\"charting.legend.placement\\">right</option><option name=\\"charting.lineWidth\\">2</option><option name=\\"trellis.enabled\\">0</option><option name=\\"trellis.scales.shared\\">1</option><option name=\\"trellis.size\\">small</option><option name=\\"trellis.splitBy\\">_aggregation</option></chart></panel></row></dashboard>")
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eai_data: Dashboard XML definition.
        :param pulumi.Input[str] name: Dashboard name.
               * `eai:data` - (Required) Dashboard XML definition.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataUiViewsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Resource: DataUiViews

        Create and manage splunk dashboards/views.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_splunk as splunk

        dashboard = splunk.DataUiViews("dashboard",
            acl=splunk.DataUiViewsAclArgs(
                app="search",
                owner="admin",
            ),
            eai_data="<dashboard version=\\"1.1\\"><label>Terraform</label><description>Terraform operations</description><row><panel><chart><search><query>index=_internal sourcetype=splunkd_access useragent=\\"splunk-simple-go-client\\" | timechart fixedrange=f values(status) by uri_path</query><earliest>-24h@h</earliest><latest>now</latest><sampleRatio>1</sampleRatio></search><option name=\\"charting.axisLabelsX.majorLabelStyle.overflowMode\\">ellipsisNone</option><option name=\\"charting.axisLabelsX.majorLabelStyle.rotation\\">0</option><option name=\\"charting.axisTitleX.visibility\\">collapsed</option><option name=\\"charting.axisTitleY.text\\">HTTP status codes</option><option name=\\"charting.axisTitleY.visibility\\">visible</option><option name=\\"charting.axisTitleY2.visibility\\">visible</option><option name=\\"charting.axisX.abbreviation\\">none</option><option name=\\"charting.axisX.scale\\">linear</option><option name=\\"charting.axisY.abbreviation\\">none</option><option name=\\"charting.axisY.scale\\">linear</option><option name=\\"charting.axisY2.abbreviation\\">none</option><option name=\\"charting.axisY2.enabled\\">0</option><option name=\\"charting.axisY2.scale\\">inherit</option><option name=\\"charting.chart\\">column</option><option name=\\"charting.chart.bubbleMaximumSize\\">50</option><option name=\\"charting.chart.bubbleMinimumSize\\">10</option><option name=\\"charting.chart.bubbleSizeBy\\">area</option><option name=\\"charting.chart.nullValueMode\\">connect</option><option name=\\"charting.chart.showDataLabels\\">none</option><option name=\\"charting.chart.sliceCollapsingThreshold\\">0.01</option><option name=\\"charting.chart.stackMode\\">default</option><option name=\\"charting.chart.style\\">shiny</option><option name=\\"charting.drilldown\\">none</option><option name=\\"charting.layout.splitSeries\\">0</option><option name=\\"charting.layout.splitSeries.allowIndependentYRanges\\">0</option><option name=\\"charting.legend.labelStyle.overflowMode\\">ellipsisMiddle</option><option name=\\"charting.legend.mode\\">standard</option><option name=\\"charting.legend.placement\\">right</option><option name=\\"charting.lineWidth\\">2</option><option name=\\"trellis.enabled\\">0</option><option name=\\"trellis.scales.shared\\">1</option><option name=\\"trellis.size\\">small</option><option name=\\"trellis.splitBy\\">_aggregation</option></chart></panel></row></dashboard>")
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param DataUiViewsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataUiViewsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl: Optional[pulumi.Input[pulumi.InputType['DataUiViewsAclArgs']]] = None,
                 eai_data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataUiViewsArgs.__new__(DataUiViewsArgs)

            __props__.__dict__["acl"] = acl
            if eai_data is None and not opts.urn:
                raise TypeError("Missing required property 'eai_data'")
            __props__.__dict__["eai_data"] = eai_data
            __props__.__dict__["name"] = name
        super(DataUiViews, __self__).__init__(
            'splunk:index/dataUiViews:DataUiViews',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acl: Optional[pulumi.Input[pulumi.InputType['DataUiViewsAclArgs']]] = None,
            eai_data: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'DataUiViews':
        """
        Get an existing DataUiViews resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eai_data: Dashboard XML definition.
        :param pulumi.Input[str] name: Dashboard name.
               * `eai:data` - (Required) Dashboard XML definition.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DataUiViewsState.__new__(_DataUiViewsState)

        __props__.__dict__["acl"] = acl
        __props__.__dict__["eai_data"] = eai_data
        __props__.__dict__["name"] = name
        return DataUiViews(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def acl(self) -> pulumi.Output['outputs.DataUiViewsAcl']:
        return pulumi.get(self, "acl")

    @property
    @pulumi.getter(name="eaiData")
    def eai_data(self) -> pulumi.Output[str]:
        """
        Dashboard XML definition.
        """
        return pulumi.get(self, "eai_data")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Dashboard name.
        * `eai:data` - (Required) Dashboard XML definition.
        """
        return pulumi.get(self, "name")

