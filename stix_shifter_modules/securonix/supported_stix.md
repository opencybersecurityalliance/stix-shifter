# Securonix

## Supported STIX Mappings

### Results STIX Domain Objects

*   Identity
*   Observed Data

### Supported STIX Operators

| STIX Operator    | Data Source Operator |
|------------------|----------------------|
| AND (Comparison) | AND                  |
| OR (Comparison)  | OR                   |
| =                | =                    |
| !=               | !=                   |
| >                | >                    |
| >=               | >=                   |
| <                | <                    |
| <=               | <=                   |
| IN               | IN                   |

### Searchable STIX objects and properties

| STIX Object and Property               | Mapped Data Source Fields |
|----------------------------------------|---------------------------|
| **x-oca-event**:action                 | action                    |
| **x-oca-event**:description            | description               |
| **x-oca-event**:category               | category                  |
| **x-oca-event**:severity               | severity                  |
| **x-oca-event**:created                | eventtime                 |
| **x-oca-event**:user_ref.account_login | username                  |
| **ipv4-addr**:value                    | sourceip, destinationip   |
| **x-oca-event**:timeline_by_month      | timeline_by_month         |
| **x-oca-event**:rg_timezoneoffset      | rg_timezoneoffset         |
| **x-oca-event**:resourcegroupname      | resourcegroupname         |
| **x-oca-event**:eventid                | eventid                   |
| **x-oca-event**:ipaddress              | ipaddress                 |
| **x-oca-event**:week                   | week                      |
| **x-oca-event**:year                   | year                      |
| **x-oca-event**:accountresourcekey     | accountresourcekey        |
| **x-oca-event**:resourcehostname       | resourcehostname          |
| **x-oca-event**:sourceprocessname      | sourceprocessname         |
| **x-oca-event**:rg_functionality       | rg_functionality          |
| **x-oca-event**:userid                 | userid                    |
| **x-oca-event**:customfield2           | customfield2              |
| **x-oca-event**:dayofmonth             | dayofmonth                |
| **x-oca-event**:jobid                  | jobid                     |
| **x-oca-event**:resourcegroupid        | resourcegroupid           |
| **x-oca-event**:datetime               | datetime                  |
| **x-oca-event**:timeline_by_hour       | timeline_by_hour          |
| **x-oca-event**:collectiontimestamp    | collectiontimestamp       |
| **x-oca-event**:hour                   | hour                      |
| **x-oca-event**:accountname            | accountname               |
| **x-oca-event**:tenantid               | tenantid                  |
| **x-oca-event**:id                     | id                        |
| **x-oca-event**:rg_resourcetypeid      | rg_resourcetypeid         |
| **x-oca-event**:_indexed_at_tdt        | _indexed_at_tdt           |
| **x-oca-event**:timeline_by_minute     | timeline_by_minute        |
| **x-oca-event**:routekey               | routekey                  |
| **x-oca-event**:collectionmethod       | collectionmethod          |
| **x-oca-event**:receivedtime           | receivedtime              |
| **x-oca-event**:publishedtime          | publishedtime             |
| **x-oca-event**:categorizedtime        | categorizedtime           |
| **x-oca-event**:jobstarttime           | jobstarttime              |
| **x-oca-event**:dayofyear              | dayofyear                 |
| **x-oca-event**:minute                 | minute                    |
| **x-oca-event**:categoryseverity       | categoryseverity          |
| **x-oca-event**:rg_vendor              | rg_vendor                 |
| **x-oca-event**:month                  | month                     |
| **x-oca-event**:version                | version                   |
| **x-oca-event**:timeline               | timeline                  |
| **x-oca-event**:dayofweek              | dayofweek                 |
| **x-oca-event**:timeline_by_week       | timeline_by_week          |
| **x-oca-event**:tenantname             | tenantname                |
| **x-oca-event**:resourcename           | resourcename              |
| **x-oca-event**:ingestionnodeid        | ingestionnodeid           |

### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property       | Data Source Field   |
|-------------|---------------------|---------------------|
| x-oca-event | action              | action              |
| x-oca-event | description         | description         |
| x-oca-event | category            | category            |
| x-oca-event | severity            | severity            |
| x-oca-event | created             | eventtime           |
| x-oca-event | user_ref            | username            |
| ipv4-addr   | value               | sourceip            |
| ipv4-addr   | value               | destinationip       |
| x-oca-event | timeline_by_month   | timeline_by_month   |
| x-oca-event | rg_timezoneoffset   | rg_timezoneoffset   |
| x-oca-event | resourcegroupname   | resourcegroupname   |
| x-oca-event | eventid             | eventid             |
| x-oca-event | ipaddress           | ipaddress           |
| x-oca-event | week                | week                |
| x-oca-event | year                | year                |
| x-oca-event | accountresourcekey  | accountresourcekey  |
| x-oca-event | resourcehostname    | resourcehostname    |
| x-oca-event | sourceprocessname   | sourceprocessname   |
| x-oca-event | rg_functionality    | rg_functionality    |
| x-oca-event | userid              | userid              |
| x-oca-event | customfield2        | customfield2        |
| x-oca-event | dayofmonth          | dayofmonth          |
| x-oca-event | jobid               | jobid               |
| x-oca-event | resourcegroupid     | resourcegroupid     |
| x-oca-event | datetime            | datetime            |
| x-oca-event | timeline_by_hour    | timeline_by_hour    |
| x-oca-event | collectiontimestamp | collectiontimestamp |
| x-oca-event | hour                | hour                |
| x-oca-event | accountname         | accountname         |
| x-oca-event | tenantid            | tenantid            |
| x-oca-event | id                  | id                  |
| x-oca-event | rg_resourcetypeid   | rg_resourcetypeid   |
| x-oca-event | _indexed_at_tdt     | _indexed_at_tdt     |
| x-oca-event | timeline_by_minute  | timeline_by_minute  |
| x-oca-event | routekey            | routekey            |
| x-oca-event | collectionmethod    | collectionmethod    |
| x-oca-event | receivedtime        | receivedtime        |
| x-oca-event | publishedtime       | publishedtime       |
| x-oca-event | categorizedtime     | categorizedtime     |
| x-oca-event | jobstarttime        | jobstarttime        |
| x-oca-event | dayofyear           | dayofyear           |
| x-oca-event | minute              | minute              |
| x-oca-event | categoryseverity    | categoryseverity    |
| x-oca-event | rg_vendor           | rg_vendor           |
| x-oca-event | month               | month               |
| x-oca-event | version             | version             |
| x-oca-event | timeline            | timeline            |
| x-oca-event | dayofweek           | dayofweek           |
| x-oca-event | timeline_by_week    | timeline_by_week    |
| x-oca-event | tenantname          | tenantname          |
| x-oca-event | resourcename        | resourcename        |
| x-oca-event | ingestionnodeid     | ingestionnodeid     |