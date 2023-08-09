## Mapping Keywords

There are keywords which need to be specified in the `to-stix` mappings in order to perform specific operations on the datasource fields. There are two types of keywords:
1. Required
2. Optional 

The below table contains the keywords and their usages:
<table class="colwidths-auto table">
<thead>
  <tr>
    <th>Keywords</th>
    <th>Type</th>
    <th>Descriptions</th>
    <th>Usage</th>
    <th>Example</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>key</td>
    <td>String</td>
    <td>The STIX object and properties whose path is defined in dot notation.</td>
    <td>"key": "stix-object.stix_object_property.sub_property"</td>
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
  <tr>
    <td>object</td>
    <td>String</td>
    <td>The name specified in the object is used to add properties of same the object. </td>
    <td>"object": "src_ip" </td>
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
</tbody>
</table>


### Required Keywords

<table class="colwidths-auto table">
<tr>
<td> Keywords </td> <td> Type </td> <td> Descriptions </td> <td> Usage </td> <td> Example </td>
</tr>
<td><b> key </b></td> <td> String </td> <td> The STIX object and properties whose path is defined in dot notation.</td> <td> "key": "stix-object.stix_object_property.sub_property" </td>
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
<td><b> object </b></td> <td> String </td> <td> The name specified in the object is used to add properties of same the object. </td> <td> "object": "src_ip" </td>
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


### Optional Keywords

<table class="colwidths-auto table">
<tr>
<td> Keywords </td> <td> Type </td> <td> Descriptions </td> <td> Usage </td>
</tr>
<tr>
<td><b> references </b></td> <td> String/List(string) </td> <td> Specifies named objects to reference in another object. </td> <td> "references": "src_ip" <br>"references": ["dst_mac"] </td>
</tr>
<tr>
<td><b> transformer </b></td> <td> String </td> <td> The function applied to the datasource value when writting data to STIX.</td> <td> "transformer": "ToInteger" </td>
</tr>
<tr>
<td><b> value </b></td> <td> Any </td> <td> A constant (literal) value to assign to the target STIX property. </td> <td> "value": "test" </td>
</tr>
<tr>
<td><b> unwrap </b></td> <td> Boolean </td> <td> Unwrap an array of STIX values to separate STIX objects if the keyword value is set to True </td> <td> "unwrap": true </td>
</tr>
<tr>
<td><b> group </b></td> <td> Boolean </td> <td> Combine the references into a list </td> <td> "group" : true </td>
</tr>
<tr>
<td><b> group_ref </b></td> <td> Boolean </td> <td> This keyword needs to be used when there is a nested list of dictionaries and each dictionary item creates an object. This keyword groups together references in a list and sets where the object is mapped. </td> <td> "group_ref": true </td>
</tr>
<td><b> ds_key </b></td> <td> String </td> <td> This keyword is used when datasource results are formatted to modify some field names. The value assigned to the keyword determines the mapping of a STIX object. This keyword is only used in the aws_athena and aws_cloud_watch_logs modules to resolve nested dictionary mappings. <b>This keyword has been deprecated since nested dictionary mappings are now handled by the JSON to STIX translation utility.</b> </td> <td> "ds_key": "resource_instancedetails_networkinterfaces_0_networkinterfaceid" </td>
</tr>
</table>


### Examples of Optional keywords:

####  unwrap 

**Mapping:**

```{
  "resolved_ip": [
      {
        "key": "ipv4-addr.value",
        "object": "resolved_ip",
        "unwrap": true
      }
    ]
}
```

**Datasource Result:**
```
{
  "resolved_ip": [
    "40.116.120.16", "1.2.3.4"
  ]
}
```
**STIX Translation**

This STIX bundle contains two ipv4-addr objects which are created based on `unwrap` keyword:

```
{
    "type": "bundle",
    "id": "bundle--f3b77b73-f21f-49b8-be6b-6034b47f5b60",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "elastic_ecs",
            "identity_class": "events",
            "spec_version": "2.0",
            "created": "2022-03-23T14:15:56.519Z",
            "modified": "2022-03-23T14:15:56.519Z"
        },
        {
            "id": "observed-data--ad31fb85-7723-4923-bb68-fa52e101e9b9",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-07-20T14:36:18.711Z",
            "modified": "2023-07-20T14:36:18.711Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "40.116.120.16"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "1.2.3.4"
                }
            },
            "first_observed": "2019-04-21T11:05:07.000Z",
            "last_observed": "2019-04-21T11:05:07.000Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

<br>

####  group 

**Mapping:**

```
{
  "sourceip": [
    {
      "key": "ipv4-addr.value",
      "object": "host_ip"
    },
    {
      "key": "x-oca-asset.ip_refs",
      "object": "host",
      "references": ["host_ip"],
      "group": true
    }
  ],
  "identityip": [
    {
      "key": "ipv4-addr.value",
      "object": "host_ip_addr_v4"
    },
    {
      "key": "x-oca-asset.ip_refs",
      "object": "host",
      "references": ["host_ip"],
      "group": true
    }
  ]
}
```

**Datasource Result:**

```
{
    "identityip": "127.0.0.1",
    "sourceip": "10.10.10.10",
    "identityhostname": "host.com"
}
```

**STIX Translation**

`ip_refs` STIX property contains two reference objects which is grouped together in a list when `group` keyword is used:

```
{
    "type": "bundle",
    "id": "bundle--8d3b18d9-cbc4-4788-83e7-dd1e6a9026c9",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "qradar",
            "identity_class": "events",
            "spec_version": "2.0",
            "created": "2022-03-23T14:15:56.519Z",
            "modified": "2022-03-23T14:15:56.519Z"
        },
        {
            "id": "observed-data--9b7896ba-7a1a-4417-a61b-61b15b017721",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-07-20T18:06:32.907Z",
            "modified": "2023-07-20T18:06:32.907Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "1": {
                    "type": "x-oca-asset",
                    "ip_refs": [
                        "0",
                        "3"
                    ],
                    "hostname": "host.com"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "10.10.10.10"
                }
            },
            "first_observed": "2023-07-20T18:06:32.907Z",
            "last_observed": "2023-07-20T18:06:32.907Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

<br>

#### group_ref 

**Mapping:**

```
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

**Datasource Result:**

```
{
    "Resource": {
        "ResourceType": "Container",
        "EbsVolumeDetails": {
            "ScannedVolumeDetails": [
                {
                    "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/vol-09d5050dea915943d",
                    "VolumeType": "GeneratedScannedVolumeType",
                    "DeviceName": "GeneratedScannedDeviceName",
                    "VolumeSizeInGB": 8,
                    "EncryptionType": "UNENCRYPTED",
                    "SnapshotArn": "arn:aws:ec2:us-east-2:12345678910:snapshot/snap-12345678901234567",
                    "KmsKeyArn": 'null'
                }
            ]
        },
        "ContainerDetails": {
            "Id": "abcdefghijklmn",
            "Name": "GeneratedFindingContainerName",
            "Image": "GeneratedFindingContainerImage"
        }
     }
    }
```

**STIX Translation**

List of nested dictionary in datasource results are referenced in `scanned_refs` property when `group_ref` keyword is used in the mapping:


```
{
    "id": "observed-data--eebc6bb5-ee4c-4923-86d4-8223caa28d12",
    "type": "observed-data",
    "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "created": "2023-07-20T18:33:39.981Z",
    "modified": "2023-07-20T18:33:39.981Z",
    "objects": {
        "0": {
            "type": "x-aws-resource",
            "resource_type": "Container",
            "ebs_volume": {
                "scanned_refs": [
                    "2"
                ]
            },
            "standalone_container_ref": "3"
        },
        "2": {
            "type": "x-aws-ebs-volume-scanned",
            "volume_arn": "arn:aws:ec2:us-west-2:12345678910:volume/vol-09d5050dea915943d",
            "volume_type": "GeneratedScannedVolumeType",
            "device_name": "GeneratedScannedDeviceName",
            "volume_size": 8,
            "encryption_type": "UNENCRYPTED",
            "snapshot_key_arn": "arn:aws:ec2:us-east-2:12345678910:snapshot/snap-12345678901234567",
            "kms_key_arn": "null"
        },
        "3": {
            "type": "x-aws-container",
            "container_id": "abcdefghijklmn",
            "name": "GeneratedFindingContainerName",
            "image": "GeneratedFindingContainerImage"
        }
    },
    "first_observed": "2023-07-20T18:33:39.981Z",
    "last_observed": "2023-07-20T18:33:39.981Z",
    "number_observed": 1
}
```

<br>

#### value 

**Mapping:**

```
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

**Datasource Result:**

```
{
          "@timestamp": "2019-04-21T11:05:07.000Z",
          "event": {
            "original": "10.42.42.42 - - [07/Dec/2018:11:05:07 +0100] \"GET /blog HTTP/1.1\" 200 2571 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36\""
          }
}
```

**STIX Translation**

`mime_type` value has been set from the mapping `value` keyword:

```
{
    "id": "observed-data--fb592d78-942b-4829-9a3e-aacb14f9eb27",
    "type": "observed-data",
    "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "created": "2023-07-20T19:08:18.458Z",
    "modified": "2023-07-20T19:08:18.458Z",
    "objects": {
        "0": {
            "type": "artifact",
            "payload_bin": "MTAuNDIuNDIuNDIgLSAtIFswNy9EZWMvMjAxODoxMTowNTowNyArMDEwMF0gIkdFVCAvYmxvZyBIVFRQLzEuMSIgMjAwIDI1NzEgIi0iICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNF8wKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzAuMC4zNTM4LjEwMiBTYWZhcmkvNTM3LjM2Ig==",
            "mime_type": "text/plain"
        }
    },
    "first_observed": "2019-04-21T11:05:07.000Z",
    "last_observed": "2019-04-21T11:05:07.000Z",
    "number_observed": 1
}
```

<br>

#### references 

**Mapping:**

```
{
  "sourceip": [
    {
      "key": "ipv4-addr.value",
      "object": "src_ip"
    },
    {
      "key": "network-traffic.src_ref",
      "object": "nt",
      "references": "src_ip"
    }
  ],
  "protocol": {
    "key": "network-traffic.protocols",
    "object": "nt"
  }
}
```

**Datasource Result:**

```{
    "sourceip": "10.10.10.10",
    "protocol": "TCP"
}
```

**STIX Translation**

Source `ipv4-addr` object number is referenced in `network-traffic` object:

```
{
    "type": "bundle",
    "id": "bundle--7c70d70e-e6a1-4e31-8f21-78efee48737a",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "qradar",
            "identity_class": "events",
            "spec_version": "2.0",
            "created": "2022-03-23T14:15:56.519Z",
            "modified": "2022-03-23T14:15:56.519Z"
        },
        {
            "id": "observed-data--f353936e-ec99-4975-b0c3-498b22bf10fb",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-07-21T13:37:32.811Z",
            "modified": "2023-07-21T13:37:32.811Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "10.10.10.10"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "protocols": [
                        "tcp"
                    ]
                }
            },
            "first_observed": "2023-07-21T13:37:32.811Z",
            "last_observed": "2023-07-21T13:37:32.811Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

<br>

#### transformer  

**Mapping:**
```
{
  "sourceip": [
    {
      "key": "ipv4-addr.value",
      "object": "src_ip"
    },
    {
      "key": "network-traffic.src_ref",
      "object": "nt",
      "references": "src_ip"
    }
  ],
  "protocol": {
    "key": "network-traffic.protocols",
    "object": "nt"
  },
  "sourceport": {
    "key": "network-traffic.src_port",
    "object": "nt",
    "transformer": "ToInteger"
  }
}
```

**Datasource Result:**
```
{
    "sourceip": "10.10.10.10",
    "protocol": "TCP",
    "sourceport": "3000"
}
```

**STIX Translation**

Port value is transformed from string to integer when `ToInteger` transformer is set in the mapping:

```
{
    "type": "bundle",
    "id": "bundle--0aee4703-bf5b-4830-9a4a-de29c8b526fd",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "qradar",
            "identity_class": "events",
            "spec_version": "2.0",
            "created": "2022-03-23T14:15:56.519Z",
            "modified": "2022-03-23T14:15:56.519Z"
        },
        {
            "id": "observed-data--9d80b67b-b2df-49a7-b16a-5f197b98d437",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-07-21T13:54:25.088Z",
            "modified": "2023-07-21T13:54:25.088Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "10.10.10.10"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "protocols": [
                        "tcp"
                    ],
                    "src_port": 3000
                }
            },
            "first_observed": "2023-07-21T13:54:25.088Z",
            "last_observed": "2023-07-21T13:54:25.088Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```