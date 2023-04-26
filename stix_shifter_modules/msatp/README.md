# Microsoft Defender for Endpoint

## Supported STIX Mappings

See the [table of mappings](msatp_supported_stix.md) for the STIX objects and operators supported by this connector.

# MSATP - Microsoft Defender for Endpoint module
This module uses KQL to query the EDR API.

Queries are constructed as unions for all the relevant event tables based on the queried fields.
The potential tables are `DeviceProcessEvents`, `DeviceNetworkEvents`, 
`DeviceRegistryEvents`, `DeviceFileEvents`, `DeviceImageLoadEvents` and `DeviceEvents`

## Connection options:

There are 4 connection options (default to `false`):
### `includeNetworkInfo`:
If true, every query is joined with `DeviceNetworkInfo` table in order to get the active network adapters from the relevant time of\
the event (IP and mac addresses).

### `includeHostOs`:
If true, every query is also joined with `DeviceInfo` table to get the host operating system.

### `includeAlerts`:
If true, queries are joined with `DeviceAlertEvents` to look for relevant alerts. An alert is joined based on
the `Timestamp` of the event, `DeviceId` and `ReportId`. Relevant alerts will be mapped to `x-ibm-finding` 
with their relevant TTP's.
Searching for an alert field (for example `x-ibm-finding:alert_id`) will search the alerts table first
and then join it with the relevant events that are correlated to it.

### `retain_original`:
If true, the original json result from the EDR is encoded in base64 and is included as `artifact` in the observed data
and referenced from `x-oca-event` as `original_ref`.  
This is useful if some of the fields in the original output are missing and the analyst would like to see the raw 
output before the translation.

## Tips for successful hunting
Be concise with what you are looking for. For example searching for a file property will be
very wide as it will look at relevant file events but also at all the binary files of
processes in the initiating process of each event and its parent process.
If you wish to look for a specific process don't query for a file, instead query the process.
For example the query `[process:pid=123]` will only look at the initiating process id.
If you want to search for a process which its parent is called `foo`look for 
`[process:parent_ref.name='foo']`. This will bring all the relevant events from processes which
their parent process is `foo` only.

If you wish to search for a file from the device file events 
(a file that has been created, modified etc.) but not search the process binary fields from all
other event tables query for:
`[x-oca-event:file_ref.name='foo']`

You can query for specific event types by querying the `action` field of `x-oca-event`.
For example if I wish to search for all `RegistryValueSet` events I will query:
`[x-oca-event:action = 'RegistryValueSet' ]`

If you want to query events on a specific host, provide its hostname as such:
`[x-oca-asset:hostname = 'host.example.com' ]`

Searching for an IP address `[ipv4-addr:value = '9.9.9.9' ]` is more general as it will search both source and 
destination ip fields. If you know the IP usage it is better to narrow the query.   
For example for a remote IP use: `[network-traffic:dst_ref.value = '9.9.9.9' ]`.  
For a local IP use `[network-traffic:src_ref.value = '9.9.9.1' ]`

## Examples
Here are a few examples for results from different tables and how to interpret them:

### DeviceProcessEvents

In this example all connection options are set to `true`.  
The main starting point to look at will be `x-oca-event:action` which tells us the 
event is a process create event.

the `process_ref` will lead us to the process that was created and its `parent_ref` 
to the process which created it.

`host_ref` leads us to `x-oca-asset` which shows information on the host on which this 
event occurred: its name, unique device id, and the ip addresses and mac addresses 
that were observed on the device.

`created` shows us the timestamp when this event was observed.

`user_ref` shows us the user account that was performing the event. `account_login` is mapped
to the user UPN which is resolved by msatp from the active directory. `user_id` is mapped 
to the account name. 

`external_ref` is a link to the msatp web console that will show us the timeline of this device
one second before and after the event occurred.

`original_ref` is the original json output from the msatp api response encoded in base64.
If there are fields you are interested to check but are not mapped to stix you can find them
there.
```json
{
    "0":
    {
        "type": "x-msatp",
        "ReportId": 1234
    },
    "1":
    {
        "type": "x-oca-asset",
        "hostname": "host.test.com",
        "device_id": "deviceid",
        "mac_refs": ["13"],
        "ip_refs": ["14"],
        "architecture": "64-bit",
        "os_name": "Windows10",
        "os_version": "10.0"
    },
    "2":
    {
        "type": "x-oca-event",
        "host_ref": "1",
        "created": "2023-03-17T20:23:03.7116107Z",
        "action": "ProcessCreated",
        "process_ref": "4",
        "user_ref": "7",
        "provider": "Microsoft Defender for Endpoint",
        "external_ref": "15",
        "original_ref": "16"
    },
    "3":
    {
        "type": "file",
        "name": "msedge.exe",
        "parent_directory_ref": "6",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed",
            "SHA-256": "470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75",
            "MD5": "e180c9a532c45eba99eefd01601f5c41"
        }
    },
    "4":
    {
        "type": "process",
        "name": "msedge.exe",
        "binary_ref": "3",
        "pid": 37384,
        "command_line": "\"msedge.exe\" --type=gpu-process",
        "created": "2023-03-17T20:23:03.702Z",
        "creator_user_ref": "7",
        "parent_ref": "5"
    },
    "5":
    {
        "type": "process",
        "child_refs": ["4"],
        "creator_user_ref": "8",
        "binary_ref": "9",
        "name": "msedge.exe",
        "pid": 400,
        "command_line": "\"msedge.exe\" -- \"https://test.com/login/login.asp\"",
        "created": "2023-03-17T20:23:03.441Z",
        "parent_ref": "11"
    },
    "6":
    {
        "type": "directory",
        "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application"
    },
    "7":
    {
        "type": "user-account",
        "user_id": "username",
        "account_login": "username@test.com"
    },
    "8":
    {
        "type": "user-account",
        "user_id": "username",
        "account_login": "username@test.com"
    },
    "9":
    {
        "type": "file",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed",
            "SHA-256": "470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75",
            "MD5": "e180c9a532c45eba99eefd01601f5c41"
        },
        "name": "msedge.exe",
        "parent_directory_ref": "10"
    },
    "10":
    {
        "type": "directory",
        "path": "c:\\program files (x86)\\microsoft\\edge\\application"
    },
    "11":
    {
        "type": "process",
        "pid": 30972,
        "name": "iexplore.exe",
        "binary_ref": "12",
        "created": "2023-03-17T20:23:03.169Z"
    },
    "12":
    {
        "type": "file",
        "name": "iexplore.exe"
    },
    "13":
    {
        "type": "mac-addr",
        "value": "11:22:33:44:55:66"
    },
    "14":
    {
        "type": "ipv4-addr",
        "value": "9.9.9.1"
    },
    "15":
    {
        "type": "external-reference",
        "url": "https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-17T20:23:02.000Z&to=2023-03-17T20:23:04.000Z"
    },
    "16":
    {
    	"type": "artifact",
    	"payload_bin": "base64 encoded json output from msatp api response before translation"
    }
}
```

This same event with all connection options set to `false` will be missing the host ip and mac addresses, the host OS details and the `original_ref` in `x-oca-event`:
```json
{
    "0":
    {
        "type": "x-msatp",
        "ReportId": 1234
    },
    "1":
    {
        "type": "x-oca-asset",
        "hostname": "host.test.com",
        "device_id": "deviceid"
    },
    "2":
    {
        "type": "x-oca-event",
        "host_ref": "1",
        "created": "2023-03-17T20:23:03.7116107Z",
        "action": "ProcessCreated",
        "process_ref": "4",
        "user_ref": "7",
        "provider": "Microsoft Defender for Endpoint",
        "external_ref": "13"
    },
    "3":
    {
        "type": "file",
        "name": "msedge.exe",
        "parent_directory_ref": "6",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed",
            "SHA-256": "470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75",
            "MD5": "e180c9a532c45eba99eefd01601f5c41"
        }
    },
    "4":
    {
        "type": "process",
        "name": "msedge.exe",
        "binary_ref": "3",
        "pid": 37384,
        "command_line": "\"msedge.exe\" --type=gpu-process",
        "created": "2023-03-17T20:23:03.702Z",
        "creator_user_ref": "7",
        "parent_ref": "5"
    },
    "5":
    {
        "type": "process",
        "child_refs": ["4"],
        "creator_user_ref": "8",
        "binary_ref": "9",
        "name": "msedge.exe",
        "pid": 400,
        "command_line": "\"msedge.exe\" -- \"https://test.com/login/login.asp\"",
        "created": "2023-03-17T20:23:03.441Z",
        "parent_ref": "11"
    },
    "6":
    {
        "type": "directory",
        "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application"
    },
    "7":
    {
        "type": "user-account",
        "user_id": "username",
        "account_login": "username@test.com"
    },
    "8":
    {
        "type": "user-account",
        "user_id": "username",
        "account_login": "username@test.com"
    },
    "9":
    {
        "type": "file",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed",
            "SHA-256": "470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75",
            "MD5": "e180c9a532c45eba99eefd01601f5c41"
        },
        "name": "msedge.exe",
        "parent_directory_ref": "10"
    },
    "10":
    {
        "type": "directory",
        "path": "c:\\program files (x86)\\microsoft\\edge\\application"
    },
    "11":
    {
        "type": "process",
        "pid": 30972,
        "name": "iexplore.exe",
        "binary_ref": "12",
        "created": "2023-03-17T20:23:03.169Z"
    },
    "12":
    {
        "type": "file",
        "name": "iexplore.exe"
    },
    "13":
    {
        "type": "external-reference",
        "url": "https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-17T20:23:02.000Z&to=2023-03-17T20:23:04.000Z"
    }
}
```


### DeviceNetworkEvents with associated alert

In this example all connection options are set to `true`.  
An example including a network event to an url. 
Query example: `[domain-name:value='malicious.com']`

`url_ref` points us to the url visited. 
`domain_ref` to the domain parsed from the url. 
It is possible that only one of these will be populated depending on the data provided.

`network_ref` will show us the source and destination ip addresses and ports. Mind you that
the destination ip address is the one resolved from the domain name 
referenced by `domain_ref` in the `x-oca-event`.

`finding_refs` indicates that there are associated alerts with this event. These will be
of type `x-ibm-finding`. The event is a connection success event, and the associated alert
title is `Connection to adversary-in-the-middle (AiTM) phishing site`.

`severity` is translated from `high` (99) `medium` (66) and `low` (33).

`alert_id` is the unique alert identifier from msatp.

`ttp_tagging_refs` shows us the relevant TTP's. These will be of type `x-ibm-ttp-tagging`.  
Tactics will be mapped to `kill_chain_phases` which might be mapped to the 
mitre attack framework or a proprietary Microsoft phase - not all phases are mapped to 
mitre attack.  
Techniques will be mapped to the `mitre-attack-ext` extension and will describe the name and
id of the mitre attack technique.

```json
{
    "0":
    {
        "type": "x-oca-event",
        "created": "2023-03-17T20:19:46.6337905Z",
        "host_ref": "1",
        "process_ref": "4",
        "action": "ConnectionSuccess",
        "network_ref": "7",
        "domain_ref": "9",
        "url_ref": "8",
        "provider": "Microsoft Defender for Endpoint",
        "external_ref": "17",
        "finding_refs": ["18"],
        "original_ref": "20",
        "file_ref": "2"
    },
    "1":
    {
        "type": "x-oca-asset",
        "device_id": "deviceid",
        "hostname": "host.example.com",
        "ip_refs": ["10"],
        "mac_refs": ["16"],
        "architecture": "64-bit",
        "os_name": "Windows10",
        "os_version": "10.0"
    },
    "2":
    {
        "type": "file",
        "name": "msedge.exe",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed"
        }
    },
    "4":
    {
        "type": "process",
        "child_refs": ["3"],
        "binary_ref": "11",
        "name": "msedge.exe",
        "pid": 3052,
        "command_line": "\"msedge.exe\" --type=utility",
        "created": "2023-03-13T14:22:44.860Z",
        "parent_ref": "14",
        "creator_user_ref": "15"
    },
    "5":
    {
        "type": "x-msatp",
        "ReportId": 1234,
        "Table": "DeviceEvents"
    },
    "6":
    {
        "type": "ipv4-addr",
        "value": "9.9.9.9"
    },
    "7":
    {
        "type": "network-traffic",
        "dst_ref": "6",
        "dst_port": 443,
        "src_ref": "10",
        "src_port": 58993
    },
    "8":
    {
        "type": "url",
        "value": "https://malicious.com"
    },
    "9":
    {
        "type": "domain-name",
        "value": "malicious.com"
    },
    "10":
    {
        "type": "ipv4-addr",
        "value": "9.9.9.1"
    },
    "11":
    {
        "type": "file",
        "hashes":
        {
            "SHA-1": "c737742b81292c764ac2a7e419a37ed7fdf4a1ed",
            "SHA-256": "470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75",
            "MD5": "e180c9a532c45eba99eefd01601f5c41"
        },
        "name": "msedge.exe",
        "parent_directory_ref": "12"
    },
    "12":
    {
        "type": "directory",
        "path": "c:\\program files (x86)\\microsoft\\edge\\application"
    },
    "13":
    {
        "type": "file",
        "name": "msedge.exe"
    },
    "14":
    {
        "type": "process",
        "name": "msedge.exe",
        "binary_ref": "13",
        "pid": 9952,
        "created": "2023-03-13T14:22:44.508Z"
    },
    "15":
    {
        "type": "user-account",
        "user_id": "username",
        "account_login": "username@test.com"
    },
    "16":
    {
        "type": "mac-addr",
        "value": "11:22:33:44:55:66"
    },
    "17":
    {
        "type": "external-reference",
        "url": "https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-17T20:19:45.000Z&to=2023-03-17T20:19:47.000Z"
    },
    "18":
    {
        "type": "x-ibm-finding",
        "alert_id": "1234567890-1234-1234-1234-123456789012_1",
        "severity": 99,
        "name": "Connection to adversary-in-the-middle (AiTM) phishing site",
        "ttp_tagging_refs": ["19","21"]
    },
    "19":
    {
        "type": "x-ibm-ttp-tagging",
        "kill_chain_phases": [
        {
            "phase_name": "Credential Access",
            "kill_chain_name": "mitre-attack"
        }]
    },
    "20":
    {
        "type": "artifact",
        "payload_bin": "base64 encoded json from the msatp api before translation"
    },
    "21":
    {
      "type": "x-ibm-ttp-tagging", 
      "extensions": 
      {
        "mitre-attack-ext": 
        {
          "technique_name": "Spearphishing Link", 
          "technique_id": "T1566.002"
        }
      }
    }
}
```

### March 2023 changes
Changes made from previous version:  
- `DeviceEvents` and `DeviceImageLoadEvents` tables where added to the search query.  
Prior they were not being searched.  
- `DeviceAlertEvents` is being queried in correlation with the events.
- `DeviceNetworkInfo` is being queried to extract the device network addresses at the time of the event
- `DeviceInfo` is queried to extract the device OS details
- `domain-name` was mapped to `DeviceName` causing a mismatch between looking for events on a specific host and looking for domains in network events. The mapping to device name was removed. use `x-oca-asset:hostname` instead to search for a specific device.
- `process` fields such as `name` and `pid` were looking at both the process and its parent. This causes an overload of results. Say I searched for all events by process pid 123 - I would receive also all events of its child processes. This was removed. now searching a process property will not look at the parent process fields. To search for events where the parent  process is X search for `process:parent_ref.X`
- `user-account:account_login` was mapped to `AccountName` which is the local account name - which is now mapped to `user-account:user_id`. The `AccountUpn` which is the more meaningful field since it is resolved from active directory and usually contains for users full email is now mapped to `account_login`. The `AccountSid` (in the form of S-1-5- etc.) which was mapped to `user_id` is no longer mapped to any stix field.
- `x-msatp` `computer_name` and `machine_id` are removed as they map to `x-oca-asset` now.
- `x-oca-asset:ip` was switched to `x-oca-asset:ip_refs` array as per the official spec and now support multiple ip addresses for one host.
- `DeviceFileEvents.FileOriginUrl` and `DeviceFileEvents.FileOriginReferrerUrl` were added to the mappings - they were not mapped before.
- `x-oca-event:provider` will always state 'Microsoft Defender for Endpoint' to indicate the source of the event
- `x-oca-event:external_ref` was added and provides a link to the msatp web console filtered one second before and after the event. This is handy in case the analyst would like to look at the source data directly in the msatp console.
- event name was mapped to `x-oca-event:action`
- `x-oca-event:original_ref` was added and includes the raw json output of the msatp api encoded in base64. This is handy to find details that are not mapped to stix.
- `x-msatp:AdditionalFields` was added as this field usually contains important information.


## Example STIX pattern for file query:

#### STIX patterns:

   1. `[file:name = 'updater.exe']`
   2. `[file:name IN ('updater.exe','reg.exe')] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-01T10:43:10.003Z'`

#### Translated query(in the same order as STIX patterns):

   1. `(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-09-30T18:22:12.682690Z) and Timestamp < datetime(2019-09-30T18:27:12.682690Z) | order by Timestamp desc | where FileName =~ "updater.exe" or InitiatingProcessFileName =~ "updater.exe" or InitiatingProcessParentFileName =~ "updater.exe")`
   2. `(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-01T10:43:10.003Z) | order by Timestamp desc | where FileName in~ ("updater.exe", "reg.exe") or InitiatingProcessFileName in~ ("updater.exe", "reg.exe") or InitiatingProcessParentFileName in~ ("updater.exe", "reg.exe"))`

## Example STIX pattern for process query:

#### STIX patterns:

   1.  `[process:name = 'find.exe']`
   2.  `[process:pid > '5804'] START t'2019-08-01T08:43:10.003Z' STOP t'2019-09-30T10:43:10.003Z'`

#### Translated query(in the same order as STIX patterns):

   1.  `(find withsource = TableName in (DeviceProcessEvents) where Timestamp >= datetime(2019-10-01T11:55:44.588517Z) and Timestamp < datetime(2019-10-01T12:00:44.588517Z) | order by Timestamp desc | where FileName =~ "find.exe")`
   2.  `(find withsource = TableName in (DeviceProcessEvents) where Timestamp >= datetime(2019-08-01T08:43:10.003Z) and Timestamp < datetime(2019-09-30T10:43:10.003Z) | order by Timestamp desc | where ProcessId > 5804)`

## Example STIX pattern for network query:

#### STIX patterns:

  1. `[network-traffic:src_port = '55099'] START t'2017-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'`

#### Translated query:

  1. `(find withsource = TableName in (DeviceNetworkEvents) where Timestamp >= datetime(2017-01-10T08:43:10.003Z) and Timestamp < datetime(2019-10-23T10:43:10.003Z) | order by Timestamp desc | where tostring(LocalPort) =~ "55099")`
  
## Example STIX pattern for MAC query:

#### STIX patterns:

  1. `[mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'`

#### Translated query:

  1. `(find withsource = TableName in (DeviceNetworkEvents) where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = bin(Timestamp, 1m) | join kind= inner (DeviceNetworkInfo | where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z) | extend FormattedTimeKey = bin(Timestamp, 1m)| mvexpand parse_json(IPAddresses) | extend IP = IPAddresses.IPAddress | project Timestamp ,DeviceId , MacAddress, IP, FormattedTimeKey) on DeviceId, $left.FormattedTimeKey == $right.FormattedTimeKey | where LocalIP == IP | where MacAddress =~ "484D7E9DBD97" | order by Timestamp desc)`

## Example STIX pattern for RegistryEvents query:

#### STIX patterns:

  1. `[windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WindowsAdvancedThreatProtection'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'`
  
#### Translated query:

  1. `(find withsource = TableName in (DeviceRegistryEvents) where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-10T10:43:10.003Z) | order by Timestamp desc | where RegistryKey =~ @"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WindowsAdvancedThreatProtection")`
 
## Example STIX pattern for DirectoryPath query:

#### STIX patterns:

   1. `[directory:path LIKE 'C:\\ProgramData\\Symantec' OR process:name = 'conhost.exe'] START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'`
        (Note: Only LIKE operator is supported for STIX object with 'path' value)
#### Translated query:

   1. `(find withsource = TableName in (DeviceProcessEvents) where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z) | order by Timestamp desc | where (FileName =~ "conhost.exe") or (FolderPath contains "C:\\ProgramData\\Symantec" or InitiatingProcessFolderPath contains "C:\\ProgramData\\Symantec"))`
   
## Example STIX pattern for device and event query:

#### STIX patterns:

   1. `[x-oca-asset:hostname = 'ds-win10' OR x-oca-event:action = 'ConnectionSuccess'] START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-30T10:43:10.003Z'`
   
#### Translated query:

   1. `'union (find withsource = TableName in (DeviceProcessEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceNetworkEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceRegistryEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceFileEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceImageLoadEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10") or (ActionType =~ "ConnectionSuccess")),(find withsource = TableName in (DeviceLogonEvents)  where Timestamp >= datetime(2019-10-01T08:43:10.003Z) and Timestamp < datetime(2019-10-30T10:43:10.003Z)  | order by Timestamp desc | where (DeviceName =~ "ds-win10"))'`
   
## Example STIX pattern for Combined Observation:

#### STIX patterns:

   1. `([file:name = 'AM_Delta_Patch_1.301.613.0.exe' AND file:hashes.'SHA-1' = 'c98dbe4cb8caad5a521915f6e3f82197d53030ee'] AND [file:name MATCHES 'mpas.*' AND file:hashes.'MD5' = 'b3b863d8c5c2f3605a5b25adec80f0de']) START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-25T10:43:10.003Z'"`

#### Translated query:

   1.  `union (find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-25T10:43:10.003Z) | order by Timestamp desc | where (SHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee" or InitiatingProcessSHA1 =~ "c98dbe4cb8caad5a521915f6e3f82197d53030ee") and (FileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessFileName =~ "AM_Delta_Patch_1.301.613.0.exe" or InitiatingProcessParentFileName =~ "AM_Delta_Patch_1.301.613.0.exe")),(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-09-01T08:43:10.003Z) and Timestamp < datetime(2019-10-25T10:43:10.003Z) | order by Timestamp desc | where (MD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de" or InitiatingProcessMD5 =~ "b3b863d8c5c2f3605a5b25adec80f0de") and (FileName matches regex"(mpas.*)" or InitiatingProcessFileName matches regex"(mpas.*)" or InitiatingProcessParentFileName matches regex"(mpas.*)"))`


## Translate, Transmit, Translate Result flow of a STIX pattern:

### Single observation expression:

#### STIX patterns:

```
[file:name = 'DismHost.exe'] START t'2019-10-01T08:43:10Z' STOP t'2019-10-30T10:43:10Z'
```

#### Translated query:

```
(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-10-01T08:43:10Z) and Timestamp < datetime(2019-10-30T10:43:10Z) | order by Timestamp desc | where FileName =~ "DismHost.exe" or InitiatingProcessFileName =~ "DismHost.exe" or InitiatingProcessParentFileName =~ "DismHost.exe")
```

#### Above translated query is passed as parameter to STIX transmission module

```
transmit msatp "{\"host\":\"xx.xx.xx.xx\",\"port\": \"xxxx\"}" 
"{\"auth\":{\"tenant\": \"xxxxx\", \"clientId\": \"xxxxx\", \"clientSecret\":\"xxxxxxxx\"}}" 
results 
"(find withsource = TableName in (DeviceFileEvents) where Timestamp >= datetime(2019-10-01T08:43:10Z) and Timestamp < datetime(2019-10-30T10:43:10Z) | order by Timestamp desc | where FileName =~ \"DismHost.exe\" or InitiatingProcessFileName =~ \"DismHost.exe\" or InitiatingProcessParentFileName =~ \"DismHost.exe\")" 0 2
```

#### MSATP query result (Result is formatted by STIX transmission result module):

```
[{
    'DeviceFileEvents':
    {
    	'TableName': 'DeviceFileEvents'
        'Timestamp': '2019-10-30T08:44:56.8059397Z',
        'DeviceId': 'babec47c12ad732b595e803c3320cc32aa26af33',
        'DeviceName': 'lp-5cd84714zn.hclt.corp.hcl.in',
        'ActionType': 'FileCreated',
        'FileName': 'DismHost.exe',
        'FolderPath': 'C:\\Users\\annishprashan.stevi\\AppData\\Local\\Temp\\44556507-AAE8-4AB2-B7C4-4519CC19443C\\DismHost.exe',
        'SHA1': 'c34af1caf92b54737956e4940582bcce5cca2725',
        'MD5': '2a1ee8df1dd0335605dcc5015c60ebc0',
        'InitiatingProcessAccountDomain': 'hcltech',
        'InitiatingProcessAccountName': 'annishprashan.stevi',
        'InitiatingProcessAccountUpn': 'annishprashan.stevi@example.com',
        'InitiatingProcessAccountSid': 'S-1-5-21-333653013-2304839960-3876203932-1269283',
        'InitiatingProcessMD5': '062ec57fe7f4463161d9e6ef400b2a3e',
        'InitiatingProcessSHA1': '2eb39003998f0e518ad937db120b87e81d5a5893',
        'InitiatingProcessFolderPath': 'c:\\windows\\system32\\cleanmgr.exe',
        'InitiatingProcessFileName': 'cleanmgr.exe',
        'InitiatingProcessId': 19224,
        'InitiatingProcessCommandLine': 'cleanmgr.exe /autoclean /d C:',
        'InitiatingProcessCreationTime': '2019-10-30T08:44:33.2836067Z',
        'InitiatingProcessIntegrityLevel': 'High',
        'InitiatingProcessTokenElevation': 'TokenElevationTypeFull',
        'InitiatingProcessParentId': 2392,
        'InitiatingProcessParentFileName': 'svchost.exe',
        'InitiatingProcessParentCreationTime': '2019-10-28T18:44:18.1496667Z',
        'RequestProtocol': 'Unknown',
        'ReportId': 17363,
        'AdditionalFields': ''
        'rn': 1,
        'event_count': '1'
    }
}]
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
                    "account_login": "annishprashan.stevi@example.com",
                    "user_id": "annishprashan.stevi"
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
                },
                "8": {
                    "type": "x-oca-event",
                    "action": "FileCreated",
                    "created": "2019-10-30T08:44:56.8059397Z"
                    "provider": "Microsoft Defender for Endpoint",
                    "external_ref": "11",
                    "host_ref": "9",
                    "file_ref": "0",
                    "process_ref": "3",
                    "user_ref": "2"
                },
                "9": {
                    "type": "x-oca-asset",
                    "hostname": "lp-5cd84714zn.hclt.corp.hcl.in",
                    "device_id": "babec47c12ad732b595e803c3320cc32aa26af33"
                },
                "10": {
                    "type": "x-msatp",
                    "Table": "DeviceFileEvents",
                    "ReportId": 1234 
                },
                "11": {
                    "type": "external-reference",
                    "url": "https://security.microsoft.com/machines/babec47c12ad732b595e803c3320cc32aa26af33/timeline?from=2019-10-30T08:40:52.000Z&to=2019-10-30T08:40:54.000Z'
                }
            },
            "first_observed": "2019-10-30T08:40:53.609Z",
            "last_observed": "2019-10-30T08:40:53.609Z",
            "number_observed": 1
        }
    ]
}
```
