# To STIX mapping Keywords

There are keywords which need to be specified in the to-stix mappings in order to perform specific operations on the datasource fields. There are two types of keywords:
1. Required
2. Optional 

Below table contains the keywords and their usages:

## Required Keywords

<table>
<tr>
<td> Keywords </td> <td> Type </td> <td> Descriptions </td> <td> Usage </td> <td> Example </td>
</tr>
<td> key </td> <td> String </td> <td> The STIX object and properties are defined in path like dotted notations.</td> <td> "key": "stix-object.stix_object_property.sub_property" </td>
<td>

```json
{
  "sha256hash": {
    "key": "file.hashes.SHA-256",
    "object": "fl"
  }
}
```
</td>
</tr>
<td> object </td> <td> String </td> <td> The name specified in the object is used to add properties of same object. </td> <td> "object": "src_ip" </td>
<td>

```json
{
  "sourceip": {
    "key": "ipv4-addr.value",
    "object": "src_ip"
  }
}
```
</td>
</tr>
</table>


## Optional Keywords

<table>
<tr>
<td> Keywords </td> <td> Type </td> <td> Descriptions </td> <td> Usage </td> <td> Example </td>
</tr>
<tr>
<td> unwrap </td> <td> Boolean </td> <td> Unwrap an array of stix values to separate stix objects if the keyword value is set to True </td> <td> "unwrap": true </td>
<td>

```json
{
  "intermediate_ips": {
      "key": "ipv4-addr.value",
      "object": "src_ipv4",
      "unwrap": true
    }
}
```
</td>
</tr>
<tr>
<td> group </td> <td> Boolean </td> <td> Combine the references into a list </td> <td> "group" : true </td>
<td>

```json
{
  "modload_name": [
    {
      "key": "file.name",
      "object": "service_file",
      "transformer": "ToFileName"
    },
    {
      "key": "process.extensions.windows-service-ext.service_dll_refs",
      "object": "process",
      "group": true,
      "references": ["service_file"]
    }
  ]
}
```
</td>
</tr>
<tr>
<td> group_ref </td> <td> Boolean </td> <td> This keyword needs to be used when there is a nested list of dictionaries and each dictionary item creates an object. This keyword groups together in a list and references are listed where the object is mapped. </td> <td> "group_ref": true </td>
<td>

```json
{
  "modload_name": [
    {
      "key": "file.name",
      "object": "service_file",
      "transformer": "ToFileName"
    },
    {
      "key": "process.extensions.windows-service-ext.service_dll_refs",
      "object": "process",
      "group": true,
      "references": ["service_file"]
    }
  ]
}
{
  "EbsVolumeDetails": {
    "ScannedVolumeDetails": {
      "DeviceName": {
        "key": "x-aws-ebs-volume-scanned.device_name",
        "object": "ebsvolume_scanned"
      },
      "GroupEbsVolumeScannedReferences": {
        "key": "x-aws-resource.ebs_volume.scanned_refs",
        "object": "resource",
        "references": [
          "ebsvolume_scanned"
        ],
        "group_ref": true
      }
    }
  }
}

```
</td>
</tr>
<tr>
<td> value </td> <td> Any </td> <td> Constant (literal) value for property </td> <td> "value": "test" </td>
<td>

```json
{
  "event": {
    "original": [
      {
        "key": "artifact.payload_bin",
        "transformer": "ToBase64",
        "object": "artifact"
      },
      {
        "key": "artifact.mime_type",
        "object": "artifact",
        "value" : "text/plain"
      }
    ]
  }
}
```
</td>
</tr>
<td> references </td> <td> String/List(string) </td> <td> Specify a named objects to reference in another object. </td> <td> "references": "src_ip" <br>"references": ["dst_mac"] </td>
<td>

```json
{
  "SourceIpV4": [
    {
      "key": "ipv4-addr.value",
      "object": "src_ip"
    },
    {
      "key": "network-traffic.src_ref",
      "object": "nt",
      "references": "src_ip"
    }
  ]
}
```
</td>
</tr>
<tr>
<td> transformer </td> <td> String </td> <td> Name of the function to apply on datasource value </td> <td> "transformer": "ToInteger" </td>
<td>

```json
{
  "destinationPort": {
      "key": "network-traffic.dst_port",
      "object": "nt",
      "transformer": "ToInteger"
    }
}
```
</td>
</tr>
<tr>
<td> ds_key </td> <td> String </td> <td> This keyword is used when datasource results are formatted to alter some field names. The value assigned to the keyword determines the mapping of a STIX objects. This keyword is only used in aws_athen and aws_cloud_watch_logs module to resolve nested dictionary mappings. You maynot need this keywrod since nested dictionary mappings are now handled by JSON to STIX translation utility. </td> <td> "ds_key": "resource_instancedetails_networkinterfaces_0_networkinterfaceid" </td>
<td>

```json
{
  "resource_instancedetails_networkinterfaces_0_ipv6addresses_0": [
    {
      "key": "ipv6-addr.value",
      "object": "nc_ipv6_ip"
    },
    {
      "key": "ipv6-addr.x_aws_interface_id",
      "object": "nc_ipv6_ip",
      "ds_key": "resource_instancedetails_networkinterfaces_0_networkinterfaceid"
    }
  ]
}
```
</td>
</tr>
</table>
