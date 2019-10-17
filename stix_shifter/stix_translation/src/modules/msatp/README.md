# MSATP UDS Connector

## Example STIX pattern for file query:

#### STIX patterns:

   1. `[file:name = 'updater.exe']`
   2. `[file:name IN ('updater.exe','reg.exe')] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-01T10:43:10.003Z'`

#### Translated query(in the same order as STIX patterns):

   1. `(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-30T18:22:12.682690Z) and EventTime < datetime(2019-09-30T18:27:12.682690Z) | order by EventTime desc | where FileName =~ "updater.exe" or InitiatingProcessFileName =~ "updater.exe" or InitiatingProcessParentFileName =~ "updater.exe")`
   2. `(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-01T10:43:10.003Z) | order by EventTime desc | where FileName in~ ("updater.exe", "reg.exe") or InitiatingProcessFileName in~ ("updater.exe", "reg.exe") or InitiatingProcessParentFileName in~ ("updater.exe", "reg.exe"))`

## Example STIX pattern for process query:

#### STIX patterns:

   1.  `[process:name = 'find.exe']`
   2.  `[process:pid > '5804'] START t'2019-08-01T08:43:10.003Z' STOP t'2019-09-30T10:43:10.003Z'`

#### Translated query(in the same order as STIX patterns):

   1.  `(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime(2019-10-01T11:55:44.588517Z) and EventTime < datetime(2019-10-01T12:00:44.588517Z) | order by EventTime desc | where FileName =~ "find.exe")`
   2.  `(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime(2019-08-01T08:43:10.003Z) and EventTime < datetime(2019-09-30T10:43:10.003Z) | order by EventTime desc | where ProcessId > 5804)`

## Example STIX pattern for network query:

#### STIX patterns:

  1. `[network-traffic:src_port = '55099'] START t'2017-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'`

#### Translated query:

  1. `(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime(2017-01-10T08:43:10.003Z) and EventTime < datetime(2019-10-23T10:43:10.003Z) | order by EventTime desc | where tostring(LocalPort) =~ "55099")`
  
## Example STIX pattern for MAC query:

#### STIX patterns:

  1. `[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'`

#### Translated query:

  1. `(find withsource = TableName in (NetworkCommunicationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = bin(EventTime, 1m) | join kind= inner (MachineNetworkInfo | where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = bin(EventTime, 1m)| mvexpand parse_json(IPAddresses) | extend IP = IPAddresses.IPAddress | project EventTime ,MachineId , MacAddress, IP, FormattedTimeKey) on MachineId, $left.FormattedTimeKey == $right.FormattedTimeKey | where LocalIP == IP | where MacAddress =~ "484D7E9DBD97" | order by EventTime desc)`

## Example STIX pattern for RegistryEvents query:

#### STIX patterns:

  1. `[windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WindowsAdvancedThreatProtection'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'`
  
#### Translated query:

  1. `(find withsource = TableName in (RegistryEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-10T10:43:10.003Z) | order by EventTime desc | where RegistryKey =~ @"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WindowsAdvancedThreatProtection")`
  
## Example STIX pattern for Combined Observation:

#### STIX patterns:

   1. `([file:name = 'AM_Delta_Patch_1.301.613.0.exe' AND file:hashes.'SHA-1' = 'c98dbe4cb8caad5a521915f6e3f82197d53030ee'] AND [file:name MATCHES 'mpas.*' AND file:hashes.'MD5' = 'b3b863d8c5c2f3605a5b25adec80f0de']) START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-25T10:43:10.003Z'"`

#### Translated query:

   1.  `union (find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (SHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee" or InitiatingProcessSHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee") and (FileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessFileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessParentFileName =~ "AM_Delta_Patch_1.301.613.0.exe")),(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (MD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de" or InitiatingProcessMD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de") and (FileName matches regex"(mpas.*)" or InitiatingProcessFileName matches regex"(mpas.*)" or InitiatingProcessParentFileName matches regex"(mpas.*)"))`


## Translate, Transmit, Translate Result flow of a STIX pattern:

### Single observation expression:

#### STIX patterns:

```
[file:name = 'DismHost.exe'] START t'2019-01-10T08:43:10Z' STOP t'2019-11-23T10:43:10Z'
```

#### Translated query:

```
(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-01-10T08:43:10Z) and EventTime < datetime(2019-11-23T10:43:10Z) | order by EventTime desc | where FileName =~ "DismHost.exe" or InitiatingProcessFileName =~ "DismHost.exe" or InitiatingProcessParentFileName =~ "DismHost.exe")
```

#### Above translated query is passed as parameter to STIX transmission module

```
transmit msatp "{\"host\":\"xx.xx.xx.xx\",\"port\": \"xxxx\",\"cert_verify\":\"True\" }" 
"{\"auth\":{\"tenant\": \"xxxxx\", \"clientId\": \"xxxxx\", \"clientSecret\":\"xxxxxxxx\"}}" 
results 
"(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-01-10T08:43:10Z) and EventTime < datetime(2019-11-23T10:43:10Z) | order by EventTime desc | where FileName =~ \"DismHost.exe\" or InitiatingProcessFileName =~ \"DismHost.exe\" or InitiatingProcessParentFileName =~ \"DismHost.exe\")" 0 2
```

#### MSATP query result (Result is formatted by STIX transmission result module):

```
[{'FileCreationEvents': {'EventTime': '2019-10-14T05:43:58.4387812Z', 'MachineId': 'fc0842373e54e76f5c55830e47526f6f1c187be6', 'ComputerName': 'car-dev-win', 'ActionType': 'FileCreated', 'FileName': 'DismHost.exe', 'FolderPath': 'C:\\Windows\\Temp\\549F4E8C-950E-413A-BB73-860DD0B52459\\DismHost.exe', 'SHA1': 'b01d428264a51ae803814644ea5ea43e7d7781d5', 'MD5': 'e8007eb8977e83d29f30a122771c09aa', 'InitiatingProcessAccountDomain': 'nt authority', 'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessMD5': '3cb2aa46bb2f56352ee7d39886db1160', 'InitiatingProcessSHA1': '68931a7ec5bdfb7f6b7a85d1273b100456ae9ae7', 'InitiatingProcessFolderPath': 'c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 30\\11\\mssenses.exe', 'InitiatingProcessFileName': 'MsSenseS.exe', 'InitiatingProcessId': 3840, 'InitiatingProcessCommandLine': '"MsSenseS.exe"', 'InitiatingProcessCreationTime': '2019-10-09T04:28:56.6541694Z', 'InitiatingProcessIntegrityLevel': 'System', 'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'InitiatingProcessParentId': 3308, 'InitiatingProcessParentFileName': 'MonitoringHost.exe', 'InitiatingProcessParentCreationTime': '2019-10-09T04:28:19.7702213Z', 'RequestProtocol': 'Unknown', 'ReportId': 466, 'rn': 1, 'event_count': '1'}}, {'FileCreationEvents': {'EventTime': '2019-10-13T05:28:58.4320739Z', 'MachineId': 'fc0842373e54e76f5c55830e47526f6f1c187be6', 'ComputerName': 'car-dev-win', 'ActionType': 'FileCreated', 'FileName': 'DismHost.exe', 'FolderPath': 'C:\\Windows\\Temp\\CA881E76-B9FB-444D-BF80-0DC52BB98B58\\DismHost.exe', 'SHA1': 'b01d428264a51ae803814644ea5ea43e7d7781d5', 'MD5': 'e8007eb8977e83d29f30a122771c09aa', 'InitiatingProcessAccountDomain': 'nt authority', 'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessMD5': '3cb2aa46bb2f56352ee7d39886db1160', 'InitiatingProcessSHA1': '68931a7ec5bdfb7f6b7a85d1273b100456ae9ae7', 'InitiatingProcessFolderPath': 'c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 30\\11\\mssenses.exe', 'InitiatingProcessFileName': 'MsSenseS.exe', 'InitiatingProcessId': 3840, 'InitiatingProcessCommandLine': '"MsSenseS.exe"', 'InitiatingProcessCreationTime': '2019-10-09T04:28:56.6541694Z', 'InitiatingProcessIntegrityLevel': 'System', 'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'InitiatingProcessParentId': 3308, 'InitiatingProcessParentFileName': 'MonitoringHost.exe', 'InitiatingProcessParentCreationTime': '2019-10-09T04:28:19.7702213Z', 'RequestProtocol': 'Unknown', 'ReportId': 389, 'rn': 2, 'event_count': '1'}}]
```

#### STIX observable output:

```
 {
    "type": "bundle",
    "id": "bundle--95d3b8bf-accb-43e3-8b6d-f73078e2d1af",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "msatp",
            "identity_class": "events"
        },
        {
            "id": "observed-data--7736a80e-955f-4abc-9355-7989148670cc",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-10-14T06:19:02.183Z",
            "modified": "2019-10-14T06:19:02.183Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "DismHost.exe",
                    "parent_directory_ref": "1",
                    "hashes": {
                        "SHA-1": "b01d428264a51ae803814644ea5ea43e7d7781d5",
                        "MD5": "e8007eb8977e83d29f30a122771c09aa"
                    }
                },
                "1": {
                    "type": "directory",
                    "path": "C:\\Windows\\Temp\\549F4E8C-950E-413A-BB73-860DD0B52459"
                },
                "2": {
                    "type": "user-account",
                    "account_login": "system",
                    "user_id": "S-1-5-18"
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "binary_ref": "4",
                    "name": "MsSenseS.exe",
                    "pid": 3840,
                    "command_line": "\"MsSenseS.exe\"",
                    "created": "2019-10-09T04:28:56.654Z",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "MD5": "3cb2aa46bb2f56352ee7d39886db1160",
                        "SHA-1": "68931a7ec5bdfb7f6b7a85d1273b100456ae9ae7"
                    },
                    "parent_directory_ref": "5",
                    "name": "MsSenseS.exe"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 30\\11"
                },
                "6": {
                    "type": "process",
                    "pid": 3308,
                    "name": "MonitoringHost.exe",
                    "binary_ref": "7",
                    "created": "2019-10-09T04:28:19.770Z"
                },
                "7": {
                    "type": "file",
                    "name": "MonitoringHost.exe"
                }
            },
            "first_observed": "2019-10-14T05:43:58.438Z",
            "last_observed": "2019-10-14T05:43:58.438Z",
            "x_com_msatp": {
                "computer_identity": "car-dev-win"
            },
            "number_observed": 1
        },
        {
            "id": "observed-data--851577c9-3d1e-4f24-9d24-adf79daf73d1",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-10-14T06:19:03.023Z",
            "modified": "2019-10-14T06:19:03.023Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "DismHost.exe",
                    "parent_directory_ref": "1",
                    "hashes": {
                        "SHA-1": "b01d428264a51ae803814644ea5ea43e7d7781d5",
                        "MD5": "e8007eb8977e83d29f30a122771c09aa"
                    }
                },
                "1": {
                    "type": "directory",
                    "path": "C:\\Windows\\Temp\\CA881E76-B9FB-444D-BF80-0DC52BB98B58"
                },
                "2": {
                    "type": "user-account",
                    "account_login": "system",
                    "user_id": "S-1-5-18"
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "binary_ref": "4",
                    "name": "MsSenseS.exe",
                    "pid": 3840,
                    "command_line": "\"MsSenseS.exe\"",
                    "created": "2019-10-09T04:28:56.654Z",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "MD5": "3cb2aa46bb2f56352ee7d39886db1160",
                        "SHA-1": "68931a7ec5bdfb7f6b7a85d1273b100456ae9ae7"
                    },
                    "parent_directory_ref": "5",
                    "name": "MsSenseS.exe"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 30\\11"
                },
                "6": {
                    "type": "process",
                    "pid": 3308,
                    "name": "MonitoringHost.exe",
                    "binary_ref": "7",
                    "created": "2019-10-09T04:28:19.770Z"
                },
                "7": {
                    "type": "file",
                    "name": "MonitoringHost.exe"
                }
            },
            "first_observed": "2019-10-13T05:28:58.432Z",
            "last_observed": "2019-10-13T05:28:58.432Z",
            "x_com_msatp": {
                "computer_identity": "car-dev-win"
            },
            "number_observed": 1
        }
    ]
}

```

### Combined observation expression:

#### STIX patterns:

```
([file:name = 'AM_Delta_Patch_1.301.613.0.exe' AND file:hashes.'SHA-1' = 'c98dbe4cb8caad5a521915f6e3f82197d53030ee'] AND [file:name MATCHES 'mpas.*' AND file:hashes.'MD5' = 'b3b863d8c5c2f3605a5b25adec80f0de']) START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-25T10:43:10.003Z'
```

#### Translated query:

```
union (find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (SHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee" or InitiatingProcessSHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee") and (FileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessFileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessParentFileName =~ "AM_Delta_Patch_1.301.613.0.exe")),(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (MD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de" or InitiatingProcessMD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de") and (FileName matches regex"(mpas.*)" or InitiatingProcessFileName matches regex"(mpas.*)" or InitiatingProcessParentFileName matches regex"(mpas.*)"))
```

#### Above translated query is passed as parameter to STIX transmission module

```
transmit msatp "{\"host\":\"xx.xx.xx.xx\",\"port\": \"xxxx\",\"cert_verify\":\"True\" }" 
"{\"auth\":{\"tenant\": \"xxxxx\", \"clientId\": \"xxxxx\", \"clientSecret\":\"xxxxxxxx\"}}" 
results 
"union (find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (SHA1 =~ \"c98dbe4cb8caad5a521915f6e3f82197d53030ee\" or InitiatingProcessSHA1 =~ \"c98dbe4cb8caad5a521915f6e3f82197d53030ee\") and (FileName =~ \"AM_Delta_Patch_1.301.613.0.exe\" or InitiatingProcessFileName =~ \"AM_Delta_Patch_1.301.613.0.exe\" or InitiatingProcessParentFileName =~ \"AM_Delta_Patch_1.301.613.0.exe\")),(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (MD5 =~ \"b3b863d8c5c2f3605a5b25adec80f0de\" or InitiatingProcessMD5 =~ \"b3b863d8c5c2f3605a5b25adec80f0de\") and (FileName matches regex\"(mpas.*)\" or InitiatingProcessFileName matches regex\"(mpas.*)\" or InitiatingProcessParentFileName matches regex\"(mpas.*)\"))" 0 2
```

#### MSATP query result (Result is formatted by STIX transmission result module):

```
[{'FileCreationEvents': {'EventTime': '2019-09-05T23:01:31.7318577Z', 'MachineId': '6a55e432bd1d390e9080fa0930f4e45292b95bf8', 'ComputerName': 'testmachine2', 'ActionType': 'FileCreated', 'FileName': 'AM_Delta_Patch_1.301.613.0.exe', 'FolderPath': 'C:\\Windows\\SoftwareDistribution\\Download\\Install\\AM_Delta_Patch_1.301.613.0.exe', 'SHA1': 'c98dbe4cb8caad5a521915f6e3f82197d53030ee', 'MD5': 'c59babc2f0acfb68a2f2d51657387a3b', 'InitiatingProcessAccountDomain': 'nt authority', 'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessMD5': '9520a99e77d6196d0d09833146424113', 'InitiatingProcessSHA1': '75c5a97f521f760e32a4a9639a653eed862e9c61', 'InitiatingProcessFolderPath': 'c:\\windows\\system32\\svchost.exe', 'InitiatingProcessFileName': 'svchost.exe', 'InitiatingProcessId': 8876, 'InitiatingProcessCommandLine': 'svchost.exe -k netsvcs -p -s wuauserv', 'InitiatingProcessCreationTime': '2019-09-05T00:01:00.3681956Z', 'InitiatingProcessIntegrityLevel': 'System', 'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'InitiatingProcessParentId': 772, 'InitiatingProcessParentFileName': 'services.exe', 'InitiatingProcessParentCreationTime': '2019-09-04T09:22:24.2724516Z', 'RequestProtocol': 'Unknown', 'ReportId': 10583, 'rn': 1, 'event_count': '1'}}, {'FileCreationEvents': {'EventTime': '2019-09-05T23:00:19.8520589Z', 'MachineId': '77725e40c068f4649a772db7512dc6da80bd4214', 'ComputerName': 'testmachine1', 'ActionType': 'FileCreated', 'FileName': 'AM_Delta_Patch_1.301.613.0.exe', 'FolderPath': 'C:\\Windows\\SoftwareDistribution\\Download\\Install\\AM_Delta_Patch_1.301.613.0.exe', 'SHA1': 'c98dbe4cb8caad5a521915f6e3f82197d53030ee', 'MD5': 'c59babc2f0acfb68a2f2d51657387a3b', 'InitiatingProcessAccountDomain': 'nt authority', 'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessMD5': '9520a99e77d6196d0d09833146424113', 'InitiatingProcessSHA1': '75c5a97f521f760e32a4a9639a653eed862e9c61', 'InitiatingProcessFolderPath': 'c:\\windows\\system32\\svchost.exe', 'InitiatingProcessFileName': 'svchost.exe', 'InitiatingProcessId': 9952, 'InitiatingProcessCommandLine': 'svchost.exe -k netsvcs -p -s wuauserv', 'InitiatingProcessCreationTime': '2019-09-05T00:21:00.1715094Z', 'InitiatingProcessIntegrityLevel': 'System', 'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'InitiatingProcessParentId': 776, 'InitiatingProcessParentFileName': 'services.exe', 'InitiatingProcessParentCreationTime': '2019-09-04T09:06:09.0434386Z', 'RequestProtocol': 'Unknown', 'ReportId': 11638, 'rn': 2, 'event_count': '1'}}]
```

#### STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--a6674df5-feed-422e-8b5b-4725409d8f7e",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "msatp",
            "identity_class": "events"
        },
        {
            "id": "observed-data--c9e9a101-9e96-4fe4-aba7-42ee3b958cd8",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-10-01T06:08:39.245Z",
            "modified": "2019-10-01T06:08:39.245Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "AM_Delta_Patch_1.301.613.0.exe",
                    "parent_directory_ref": "1",
                    "hashes": {
                        "SHA-1": "c98dbe4cb8caad5a521915f6e3f82197d53030ee",
                        "MD5": "c59babc2f0acfb68a2f2d51657387a3b"
                    }
                },
                "1": {
                    "type": "directory",
                    "path": "C:\\Windows\\SoftwareDistribution\\Download\\Install"
                },
                "2": {
                    "type": "user-account",
                    "account_login": "system",
                    "user_id": "S-1-5-18"
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "binary_ref": "4",
                    "name": "svchost.exe",
                    "pid": 8876,
                    "command_line": "svchost.exe -k netsvcs -p -s wuauserv",
                    "created": "2019-09-05T00:01:00.368Z",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "MD5": "9520a99e77d6196d0d09833146424113",
                        "SHA-1": "75c5a97f521f760e32a4a9639a653eed862e9c61"
                    },
                    "parent_directory_ref": "5",
                    "name": "svchost.exe"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "6": {
                    "type": "process",
                    "pid": 772,
                    "name": "services.exe",
                    "binary_ref": "7",
                    "created": "2019-09-04T09:22:24.272Z"
                },
                "7": {
                    "type": "file",
                    "name": "services.exe"
                }
            },
            "first_observed": "2019-09-05T23:01:31.731Z",
            "last_observed": "2019-09-05T23:01:31.731Z",
            "x_com_msatp": {
                "computer_identity": "testmachine2"
            },
            "number_observed": 1
        },
        {
            "id": "observed-data--324d9ed3-2be5-4e59-8e5b-ec252651aa1b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-10-01T06:08:39.245Z",
            "modified": "2019-10-01T06:08:39.245Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "AM_Delta_Patch_1.301.613.0.exe",
                    "parent_directory_ref": "1",
                    "hashes": {
                        "SHA-1": "c98dbe4cb8caad5a521915f6e3f82197d53030ee",
                        "MD5": "c59babc2f0acfb68a2f2d51657387a3b"
                    }
                },
                "1": {
                    "type": "directory",
                    "path": "C:\\Windows\\SoftwareDistribution\\Download\\Install"
                },
                "2": {
                    "type": "user-account",
                    "account_login": "system",
                    "user_id": "S-1-5-18"
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "binary_ref": "4",
                    "name": "svchost.exe",
                    "pid": 9952,
                    "command_line": "svchost.exe -k netsvcs -p -s wuauserv",
                    "created": "2019-09-05T00:21:00.171Z",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "MD5": "9520a99e77d6196d0d09833146424113",
                        "SHA-1": "75c5a97f521f760e32a4a9639a653eed862e9c61"
                    },
                    "parent_directory_ref": "5",
                    "name": "svchost.exe"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "6": {
                    "type": "process",
                    "pid": 776,
                    "name": "services.exe",
                    "binary_ref": "7",
                    "created": "2019-09-04T09:06:09.043Z"
                },
                "7": {
                    "type": "file",
                    "name": "services.exe"
                }
            },
            "first_observed": "2019-09-05T23:00:19.852Z",
            "last_observed": "2019-09-05T23:00:19.852Z",
            "x_com_msatp": {
                "computer_identity": "testmachine1"
            },
            "number_observed": 1
        }
    ]
}


```
