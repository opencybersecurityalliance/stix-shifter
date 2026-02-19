# CrowdStrike Falcon

The CrowdStrike connector is set for deprecation and will no longer be supported. To continue receiving data, use the CrowdStrike Alerts connector instead.
The CrowdStrike Alerts connector will collect the same data as this one, except it uses the newer alerts endpoint instead of the detections endpoint. 

## Supported STIX Mappings

See the [table of mappings](crowdstrike_supported_stix.md) for the STIX objects and operators supported by this connector.

## Incident and detection monitoring APIs



### Find detections -
Find and get info about detections in order to learn more about activity in your environment.


STEP 1: GET /detects/queries/detects/v1

Query Parameter:
* >  $filter, $sort, $limit

STEP 2: POST /detects/entities/summaries/GET/v1

Query Parameter:
* > -d '{"ids": ["XXX", "XXX", "XXX", ......, "XXX"]}'




## CrowdStrike Supported STIX Pattern values (Querying):

The supported query values are defined in the mapping file from_stix_map.json. An example output object can be found here and is defined in to_stix_map.json.

```bash
* ipv4-addr:value
* ipv6-addr:value
* mac-addr:value
* directory:path
* file:name
* file:hashes.MD5
* file:hashes.SHA-256   
* user-account:user_id
* user-account:account_login
* process:name
* process:command_line
* process:created
* process:parent_ref.command_line
* domain-name:value
* url:value
```

### Execute a STIX pattern on a CrowdStrike instance

```bash
$ python3 main.py execute crowdstrike crowdstrike "<data_source>" "<connection>" "<configuration>" "<query>"
```


```bash
$ python3 main.py execute crowdstrike crowdstrike '{"id": "asdf"}' '{"host":"example.crowdstrike.io"}' '{"auth":{"client_id":"0000000000000000000000000000000000000000", "client_secret":"00000000000000000000"}}' "[process:name = 'cmd.exe']"
```

Note in this example some logging is omitted.

Translated CrowdStrike query and parsed STIX expression:

```bash
$ python3 main.py translate crowdstrike query '{}' "[process:name = 'cmd.exe']"

['process_name:cmd.exe']
{'queries': ["((behaviors.filename: 'cmd.exe') + behaviors.timestamp:> '2021-06-09T11:17:10.076846')"]}
```

## Example I - Converting from STIX patterns to FQL queries (STIX attributes)

STIX to sentinel field mapping is defined in from_stix_map.json

This example input pattern:

```bash
translate crowdstrike query ‘{}’ "[process:name = 'cmd.exe']"
```

Returns the following native query:

```bash
{'queries': ["((behaviors.filename: 'cmd.exe') + behaviors.timestamp:> '2021-06-09T11:17:10.076846')"]}
```


## Example - Converting from CrowdStrike alerts to STIX (STIX attributes)

Sentinel data to STIX mapping is defined in to_stix_map.json

Sample data:

CrowdStrike data to Stix mapping is defined in to_stix_map.json which is located in the crowdstrike module.

```bash
python main.py translate crowdstrike results '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "Splunk", "identity_class": "events"}' '[{"timestamp": "2021-05-11T21:28:50Z", "template_instance_id": "10", "behavior_id": "3295", "filename": "sbsimulation.exe", "filepath": "\\Device\\HarddiskVolume2\\Program Files\\SafeBreach\\SafeBreach Endpoint Simulator\\app\\21.2.1\\simulation\\sbsimulation.exe", "alleged_filetype": "exe", "cmdline": ""C:\\Program Files\\SafeBreach\\SafeBreach Endpoint Simulator\\app\\21.2.1\\simulation\\sbsimulation.exe" 65004 7414603171744480658 sb_263322286_bs", "scenario": "known_malware", "objective": "Falcon Detection Method", "tactic": "Machine Learning", "tactic_id": "CSTA0004", "technique": "Cloud-based ML", "technique_id": "CST0008", "description": "This process wrote a suspicious file to disk. That associated file meets the ML algorithms high-confidence malware detection threshold. Review the associated file.", "severity": 30, "confidence": 70, "ioc_description": "\\Device\\HarddiskVolume2\\Windows\\Temp\\sb-sim-temp-rf79zfee\\sb_263322286_bs_l_0oisvl\\llac.exe", "user_name": "QOX-WIN-CLIENT1$", "user_id": "S-1-5-18", "control_graph_id": "ctg:83e1e031801a43b898008da4d1b1baf3:128963684909", "triggering_process_graph_id": "pid:83e1e031801a43b898008da4d1b1baf3:225799450645", "sha256": "a8db37d3f6af5fd3546ac6fc65788ea58c0590fac011cc60c3d894241bfd9423", "md5": "e1ee778a5160599133860e2d4848d7ed", "parent_sha256": "2ab83a29c2da4a83b3498d33da3ff694aac746c76938e2a7c16497247b6e3ad2", "parent_md5": "4246f14c6cc7216e1a67c5777eb5382d", "parent_cmdline": "C:\\Program Files\\SafeBreach\\SafeBreach Endpoint Simulator\\app\\21.2.1\\simulator\\sbsimulator.exe", "parent_process_graph_id": "pid:83e1e031801a43b898008da4d1b1baf3:225210004032", "cid": "cfa41c5832b1435eb0a3a8df154d2ec8", "created_timestamp": "2021-05-11T21:29:38.061171754Z", "detection_id": "ldt:83e1e031801a43b898008da4d1b1baf3:128963684909", "email_sent": False, "first_behavior": "2021-05-11T21:28:50Z", "last_behavior": "2021-05-11T21:28:53Z", "max_confidence": 80, "max_severity": 70, "max_severity_displayname": "High", "show_in_ui": True, "status": "normal", "seconds_to_triaged": 0, "seconds_to_resolved": 0, "behaviors_processed": ["pid:83e1e031801a43b898008da4d1b1baf3:225802755151:10146", "pid:83e1e031801a43b898008da4d1b1baf3:225799450645:3265", "pid:83e1e031801a43b898008da4d1b1baf3:225799450645:3295", "pid:83e1e031801a43b898008da4d1b1baf3:225799450645:3250", "pid:83e1e031801a43b898008da4d1b1baf3:225799450645:3273"], "agent_load_flags": "0", "agent_local_time": "2021-05-06T15:15:07.901Z", "agent_version": "6.22.13607.0", "bios_manufacturer": "Phoenix Technologies LTD", "bios_version": "6.00", "config_id_base": "65994753", "config_id_build": "13607", "config_id_platform": "3", "external_ip": "198.23.124.3", "hostname": "QOX-WIN-CLIENT1", "first_seen": "2020-09-30T12:36:41Z", "last_seen": "2021-05-11T21:27:41Z", "local_ip": "172.16.100.11", "mac_address": "00-0c-29-b8-18-6a", "machine_domain": "baneandox.org", "major_version": "10", "minor_version": "0", "os_version": "Windows 10", "ou": ["QoX employees"], "platform_id": "0", "platform_name": "Windows", "product_type": "1", "product_type_desc": "Workstation", "site_name": "Default-First-Site-Name", "system_manufacturer": "VMware, Inc.", "system_product_name": "VMware Virtual Platform", "groups": ["3b5eae36d09f48b59d83293e47967dbe"], "modified_timestamp": "2021-05-11T21:27:44Z", "active_directory_dn_display": ["QoX employees"], "sha256_ioc": "8b1c149c6bc445730979d1aedb0a6925819b1b8c95d28c833fbf94cf0229f40f", "display_name": "file write", "provider": "CrowdStrike"}]'
```
Will return the following valid STIX Cyber Observable Object:

```bash
{
  "type": "bundle",
  "id": "bundle--5a42a7a2-0e3e-4832-80b1-c117a0824d4b",
  "spec_version": "2.0",
  "objects": [
    {
      "type": "identity",
      "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "name": "crowdstrike",
      "identity_class": "events"
    },
    {
      "id": "observed-data--b1c27e35-17d0-4c26-b082-f630aeccb5d4",
      "type": "observed-data",
      "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "created": "2021-06-09T09:05:51.954Z",
      "modified": "2021-06-09T09:05:51.954Z",
      "objects": {
        "0": {
          "type": "x-oca-event",
          "created": "2021-04-21T14:13:52Z",
          "process_ref": "2",
          "action": "RegistryPersistEdit",
          "outcome": "A process made a suspicious change to the registry that might indicate a malicious persistence mechanism. Investigate the registry key.",
          "severity": 70,
          "parent_process_ref": "7",
          "host_ref": "9",
          "provider": "CrowdStrike"
        },
        "1": {
          "type": "file",
          "name": "cmd.exe",
          "parent_directory_ref": "3",
          "hashes": {
            "SHA-256": "9023f8aaeda4a1da45ac477a81b5bbe4128e413f19a0abfa3715465ad66ed5cd",
            "MD5": "0d088f5bcfa8f086fba163647cd80cab"
          }
        },
        "2": {
          "type": "process",
          "binary_ref": "1",
          "name": "cmd.exe",
          "command_line": "C:\\Windows\\system32\\cmd.exe /c \"C:\\Python27\\python.exe C:\\Users\\Redlab-Admin\\Desktop\\RTA\\red_ttp\\office_application_startup.py\"",
          "creator_user_ref ": "5",
          "pid": "17459059532",
          "parent_ref": "7"
        },
        "3": {
          "type": "directory",
          "path": "\\Device\\HarddiskVolume4\\Windows\\System32\\cmd.exe"
        },
        "4": {
          "type": "x-crowdstrike",
          "scenario": "establish_persistence",
          "tactic": "Persistence",
          "tactic_id": "TA0003",
          "technique": "Registry Run Keys / Startup Folder",
          "technique_id": "T1547.001",
          "confidence": 80,
          "detection_id": "ldt:0c1b0f2a78e94d14ab284b28f7565bc2:17191307238",
          "agent_local_time": "2021-04-21T15:00:10.699Z",
          "agent_version": "6.21.13510.0",
          "ioc_value": "VMware, Inc.",
          "first_seen": "2021-01-12T18:59:10Z",
          "last_seen": "2021-04-21T14:00:27Z"
        },
        "5": {
          "type": "user-account",
          "account_login": "Redlab-Admin",
          "user_id": "S-1-5-21-2511178278-3265722015-4177099367-1001"
        },
        "6": {
          "type": "file",
          "hashes": {
            "SHA-256": "9856aeb5a4cfcd3e768ae183cbb330bfdcf1a2fe4c9634bb1a59ba53047f43a4",
            "MD5": "9767f3103c55c66cc2c9eb39d56db594"
          }
        },
        "7": {
          "type": "process",
          "binary_ref": "6",
          "command_line": "\"C:\\Python27\\python.exe\" .\\run_all.py",
          "pid": "17273889498"
        },
        "8": {
          "type": "ipv4-addr",
          "value": "12.166.224.2"
        },
        "9": {
          "type": "x-oca-asset",
          "ip_refs": [
            "8",
            "10"
          ],
          "hostname": "REDLAB-VULN2-MO",
          "mac_refs": [
            "11"
          ],
          "os_version": "Windows 10",
          "os_platform": "Windows"
        },
        "10": {
          "type": "ipv4-addr",
          "value": "10.239.15.205"
        },
        "11": {
          "type": "mac-addr",
          "value": "00-0c-29-09-85-47"
        }
      },
      "first_observed": "2021-04-21T14:13:52Z",
      "last_observed": "2021-04-21T14:13:52Z",
      "number_observed": 1
    }
  ]
}
```

## Operator Support (Data Source)



    !: not equal to

    >: greater than

    >=: greater than or equal to

    <: less than

    <=: less than or equal to

  

  ## Exclusions

FQL does not supports the following operators:

* LIKE 
* In 
* Matches

We cannot query the following STIX objects/fields:

* > netwrok-traffic:XXX (for any network-traffic field)

* > process:pid







