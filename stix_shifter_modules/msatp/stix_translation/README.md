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
 
## Example STIX pattern for DirectoryPath query:

#### STIX patterns:

   1. `[directory:path LIKE 'C:\\ProgramData\\Symantec' OR process:name = 'conhost.exe'] START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'`
        (Note: Only LIKE operator is supported for STIX object with 'path' value)
#### Translated query:

   1. `(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime(2019-10-01T08:43:10.003Z) and EventTime < datetime(2019-10-30T10:43:10.003Z) | order by EventTime desc | where (FileName =~ "conhost.exe") or (FolderPath contains "C:\\ProgramData\\Symantec" or InitiatingProcessFolderPath contains "C:\\ProgramData\\Symantec"))`
   
## Example STIX pattern for Custom Attribute(x-msatp) query:

#### STIX patterns:

   1. `[x-msatp:computer_name = 'ds-win10' OR process:name = 'conhost.exe'] START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'`
   
#### Translated query:

   1. `(find withsource = TableName in (ProcessCreationEvents) where EventTime >= datetime(2019-10-01T08:43:10.003Z) and EventTime < datetime(2019-10-30T10:43:10.003Z) | order by EventTime desc | where (FileName =~ "conhost.exe") or (ComputerName =~ "ds-win10"))`
   
## Example STIX pattern for Combined Observation:

#### STIX patterns:

   1. `([file:name = 'AM_Delta_Patch_1.301.613.0.exe' AND file:hashes.'SHA-1' = 'c98dbe4cb8caad5a521915f6e3f82197d53030ee'] AND [file:name MATCHES 'mpas.*' AND file:hashes.'MD5' = 'b3b863d8c5c2f3605a5b25adec80f0de']) START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-25T10:43:10.003Z'"`

#### Translated query:

   1.  `union (find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (SHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee" or InitiatingProcessSHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee") and (FileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessFileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessParentFileName =~ "AM_Delta_Patch_1.301.613.0.exe")),(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-09-01T08:43:10.003Z) and EventTime < datetime(2019-10-25T10:43:10.003Z) | order by EventTime desc | where (MD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de" or InitiatingProcessMD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de") and (FileName matches regex"(mpas.*)" or InitiatingProcessFileName matches regex"(mpas.*)" or InitiatingProcessParentFileName matches regex"(mpas.*)"))`


## Translate, Transmit, Translate Result flow of a STIX pattern:

### Single observation expression:

#### STIX patterns:

```
[file:name = 'DismHost.exe'] START t'2019-10-01T08:43:10Z' STOP t'2019-10-30T10:43:10Z'
```

#### Translated query:

```
(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-10-01T08:43:10Z) and EventTime < datetime(2019-10-30T10:43:10Z) | order by EventTime desc | where FileName =~ "DismHost.exe" or InitiatingProcessFileName =~ "DismHost.exe" or InitiatingProcessParentFileName =~ "DismHost.exe")
```

#### Above translated query is passed as parameter to STIX transmission module

```
transmit msatp "{\"host\":\"xx.xx.xx.xx\",\"port\": \"xxxx\"}" 
"{\"auth\":{\"tenant\": \"xxxxx\", \"clientId\": \"xxxxx\", \"clientSecret\":\"xxxxxxxx\"}}" 
results 
"(find withsource = TableName in (FileCreationEvents) where EventTime >= datetime(2019-10-01T08:43:10Z) and EventTime < datetime(2019-10-30T10:43:10Z) | order by EventTime desc | where FileName =~ \"DismHost.exe\" or InitiatingProcessFileName =~ \"DismHost.exe\" or InitiatingProcessParentFileName =~ \"DismHost.exe\")" 0 2
```

#### MSATP query result (Result is formatted by STIX transmission result module):

```
[{'FileCreationEvents': {'EventTime': '2019-10-30T08:44:56.8059397Z', 'MachineId': 'babec47c12ad732b595e803c3320cc32aa26af33', 'ComputerName': 'lp-5cd84714zn.hclt.corp.hcl.in', 'ActionType': 'FileCreated', 'FileName': 'DismHost.exe', 'FolderPath': 'C:\\Users\\annishprashan.stevi\\AppData\\Local\\Temp\\44556507-AAE8-4AB2-B7C4-4519CC19443C\\DismHost.exe', 'SHA1': 'c34af1caf92b54737956e4940582bcce5cca2725', 'MD5': '2a1ee8df1dd0335605dcc5015c60ebc0', 'InitiatingProcessAccountDomain': 'hcltech', 'InitiatingProcessAccountName': 'annishprashan.stevi', 'InitiatingProcessAccountSid': 'S-1-5-21-333653013-2304839960-3876203932-1269283', 'InitiatingProcessMD5': '062ec57fe7f4463161d9e6ef400b2a3e', 'InitiatingProcessSHA1': '2eb39003998f0e518ad937db120b87e81d5a5893', 'InitiatingProcessFolderPath': 'c:\\windows\\system32\\cleanmgr.exe', 'InitiatingProcessFileName': 'cleanmgr.exe', 'InitiatingProcessId': 19224, 'InitiatingProcessCommandLine': 'cleanmgr.exe /autoclean /d C:', 'InitiatingProcessCreationTime': '2019-10-30T08:44:33.2836067Z', 'InitiatingProcessIntegrityLevel': 'High', 'InitiatingProcessTokenElevation': 'TokenElevationTypeFull', 'InitiatingProcessParentId': 2392, 'InitiatingProcessParentFileName': 'svchost.exe', 'InitiatingProcessParentCreationTime': '2019-10-28T18:44:18.1496667Z', 'RequestProtocol': 'Unknown', 'ReportId': 17363, 'rn': 1, 'event_count': '1'}}, {'FileCreationEvents': {'EventTime': '2019-10-30T08:40:53.6099192Z', 'MachineId': 'fc0842373e54e76f5c55830e47526f6f1c187be6', 'ComputerName': 'car-dev-win', 'ActionType': 'FileCreated', 'FileName': 'DismHost.exe', 'FolderPath': 'C:\\Windows\\Temp\\9C957DFF-D551-4542-9D22-556A347F3B5B\\DismHost.exe', 'SHA1': 'b01d428264a51ae803814644ea5ea43e7d7781d5', 'MD5': 'e8007eb8977e83d29f30a122771c09aa', 'InitiatingProcessAccountDomain': 'nt authority', 'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessMD5': '3cb2aa46bb2f56352ee7d39886db1160', 'InitiatingProcessSHA1': '68931a7ec5bdfb7f6b7a85d1273b100456ae9ae7', 'InitiatingProcessFolderPath': 'c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 48\\761\\mssenses.exe', 'InitiatingProcessFileName': 'MsSenseS.exe', 'InitiatingProcessId': 4956, 'InitiatingProcessCommandLine': '"MsSenseS.exe"', 'InitiatingProcessCreationTime': '2019-10-23T06:55:53.1651027Z', 'InitiatingProcessIntegrityLevel': 'System', 'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'InitiatingProcessParentId': 3540, 'InitiatingProcessParentFileName': 'MonitoringHost.exe', 'InitiatingProcessParentCreationTime': '2019-10-22T10:55:48.4451712Z', 'RequestProtocol': 'Unknown', 'ReportId': 462, 'rn': 2, 'event_count': '1'}}]
```

#### STIX observable output:

```
 {
    "type": "bundle",
    "id": "bundle--d75ea4fd-7f34-4eca-8a35-70b427329417",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "msatp",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--c7a04ed8-755f-468e-b9ec-41897182ea18",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-11-04T07:40:17.431Z",
            "modified": "2019-11-04T07:40:17.431Z",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "DismHost.exe",
                    "parent_directory_ref": "1",
                    "hashes": {
                        "SHA-1": "c34af1caf92b54737956e4940582bcce5cca2725",
                        "MD5": "2a1ee8df1dd0335605dcc5015c60ebc0"
                    }
                },
                "1": {
                    "type": "directory",
                    "path": "C:\\Users\\annishprashan.stevi\\AppData\\Local\\Temp\\44556507-AAE8-4AB2-B7C4-4519CC19443C"
                },
                "2": {
                    "type": "user-account",
                    "account_login": "annishprashan.stevi",
                    "user_id": "S-1-5-21-333653013-2304839960-3876203932-1269283"
                },
                "3": {
                    "type": "process",
                    "creator_user_ref": "2",
                    "binary_ref": "4",
                    "name": "cleanmgr.exe",
                    "pid": 19224,
                    "command_line": "cleanmgr.exe /autoclean /d C:",
                    "created": "2019-10-30T08:44:33.283Z",
                    "parent_ref": "6"
                },
                "4": {
                    "type": "file",
                    "hashes": {
                        "MD5": "062ec57fe7f4463161d9e6ef400b2a3e",
                        "SHA-1": "2eb39003998f0e518ad937db120b87e81d5a5893"
                    },
                    "parent_directory_ref": "5",
                    "name": "cleanmgr.exe"
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "6": {
                    "type": "process",
                    "pid": 2392,
                    "name": "svchost.exe",
                    "binary_ref": "7",
                    "created": "2019-10-28T18:44:18.149Z"
                },
                "7": {
                    "type": "file",
                    "name": "svchost.exe"
                }
            },
            "first_observed": "2019-10-30T08:44:56.805Z",
            "last_observed": "2019-10-30T08:44:56.805Z",
            "x_msatp": {
                "machine_id": "babec47c12ad732b595e803c3320cc32aa26af33",
                "computer_name": "lp-5cd84714zn.hclt.corp.hcl.in"
            },
            "number_observed": 1
        },
        {
            "id": "observed-data--f337a503-71b1-4592-bf5c-e1b43a91cf66",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-11-04T07:40:17.436Z",
            "modified": "2019-11-04T07:40:17.436Z",
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
                    "path": "C:\\Windows\\Temp\\9C957DFF-D551-4542-9D22-556A347F3B5B"
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
                    "pid": 4956,
                    "command_line": "\"MsSenseS.exe\"",
                    "created": "2019-10-23T06:55:53.165Z",
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
                    "path": "c:\\program files\\microsoft monitoring agent\\agent\\health service state\\monitoring host temporary files 48\\761"
                },
                "6": {
                    "type": "process",
                    "pid": 3540,
                    "name": "MonitoringHost.exe",
                    "binary_ref": "7",
                    "created": "2019-10-22T10:55:48.445Z"
                },
                "7": {
                    "type": "file",
                    "name": "MonitoringHost.exe"
                }
            },
            "first_observed": "2019-10-30T08:40:53.609Z",
            "last_observed": "2019-10-30T08:40:53.609Z",
            "x_msatp": {
                "machine_id": "fc0842373e54e76f5c55830e47526f6f1c187be6",
                "computer_name": "car-dev-win"
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
transmit msatp "{\"host\":\"xx.xx.xx.xx\",\"port\": \"xxxx\"}" 
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
            "x_msatp": {
                "machine_id": "6a55e432bd1d390e9080fa0930f4e45292b95bf8",
                "computer_name": "testmachine2"
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
            "x_msatp": {
                "machine_id": "77725e40c068f4649a772db7512dc6da80bd4214",
                "computer_name": "testmachine1"
            },
            "number_observed": 1
        }
    ]
}


```
