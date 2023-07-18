# To STIX mapping Keywords

There are few keywords that can be specified in the to-stix mappings in order to perform specific operations on the datasource fields. Below table contains the keywords and their usages:


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
</table>
