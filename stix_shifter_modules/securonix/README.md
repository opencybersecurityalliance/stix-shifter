# Securonix Connector

## Supported STIX Mappings

The Securonix connector supports translation between STIX patterns and Securonix queries, with mappings for the following STIX objects and properties:

### Network & Communication Objects
- ipv4-addr:value → sourceip, destinationip
- mac-addr:value → sourcemacaddress, destinationmacaddress
- network-traffic:src_port → sourceport
- network-traffic:dst_port → destinationport
- network-traffic:protocols → transportprotocol

### Asset & Resource Objects
- x-oca-asset:hostname → hostname, devicehostname
- x-oca-asset:name → resourcename, resourcegroupname
- x-oca-asset:type → resourcetype

### Process Objects
- process:name → processname, sourceprocessname
- process:pid → processid
- process:command_line → commandline

### User Objects
- user-account:user_id → username, accountname
- user-account:display_name → username

### Event Objects
- x-oca-event:action → action
- x-oca-event:category → category
- x-oca-event:description → description
- x-oca-event:severity → severity, categoryseverity
- x-oca-event:category_id → categoryid
- x-oca-event:resource_group_id → resourcegroupid
- x-oca-event:tenant_id → tenantid
- x-oca-event:tenant_name → tenantname

### Securonix Specific Objects
- x-securonix:resourcename → resourcename
- x-securonix:resourcetype → resourcetype
- x-securonix:resourcegroupid → resourcegroupid
- x-securonix:categoryseverity → categoryseverity
- x-securonix:categoryid → categoryid
- x-securonix:rg_vendor → rg_vendor
- x-securonix:rg_functionality → rg_functionality
- x-securonix:tenantname → tenantname
- x-securonix:tenantid → tenantid

## Query Examples

### Translating STIX Pattern to Securonix Query.

```bash
python3 main.py translate securonix query '{}' "[ipv4-addr:value = '192.168.107.252' AND x-oca-asset:name = 'TCC_MERAKI_FIREWALL'] START t'2025-01-06T06:58:54.000Z' STOP t'2025-01-06T07:48:40.000Z'"
```

#### Translation
```json
{
    "queries": [
        "sourceaddress = '192.168.107.252' AND resourcegroupname = 'TCC_MERAKI_FIREWALL'"
    ]
}
```

### Converting Securonix Events (Activity Logs) to STIX Objects.
```bash
python3 main.py translate securonix results '{"type": "identity", "id":"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff", "name": "Securonix", "identity_class": "events"}' '[{"eventtime": "2024-01-06T06:58:54.000Z", "sourceaddress": "192.168.107.252", "resourcegroupname": "TCC_MERAKI_FIREWALL", "categoryseverity": "high"}]'
```

#### Response
```json
{
    "type": "bundle",
    "id": "bundle--unique-id",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "Securonix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--unique-id",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.107.252"
                },
                "1": {
                    "type": "x-oca-asset",
                    "name": "TCC_MERAKI_FIREWALL"
                }
            },
            "x-securonix": {
                "categoryseverity": "high"
            }
        }
    ]
}
```


