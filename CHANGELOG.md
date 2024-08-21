# CHANGELOG

We have started this changelogs from version 4.0.0. So, changes on previously released versions can be found in tag branches. Please follow the below format to update add changelogs for new tag version.

## <Tag_Version> (Date)
### Breaking changes:
*List the breaking changes in this section. Breaking changes is anything that either changes the input or output of stix-shifter, or a change that breaks the compatibility between a connector and the core stix-shifter functions.*
### Deprecations:
*List the Deprecated functions, input and output.*
### Changes:
*List the newly added functions, input and output.*
### Fixes:
*List the bug fixes.*
### Dependency update:
*List the dependecy upgrade or downgrade.*

--------------------------------------

## 7.0.12 (2024-08-20)

### Breaking changes:

### Deprecations:

### Changes:

*  Updating urllib3 to 1.26.19 [#1725](https://github.com/opencybersecurityalliance/stix-shifter/pull/1725)
*  Resolved Tanium Connector errors [#1722](https://github.com/opencybersecurityalliance/stix-shifter/pull/1722) 
                                    [#1721](https://github.com/opencybersecurityalliance/stix-shifter/pull/1721)
                                    [#1693](https://github.com/opencybersecurityalliance/stix-shifter/pull/1693)
*  Added contrast scans [#1719](https://github.com/opencybersecurityalliance/stix-shifter/pull/1719)
                        [#1718](https://github.com/opencybersecurityalliance/stix-shifter/pull/1718)
                        [#1717](https://github.com/opencybersecurityalliance/stix-shifter/pull/1717)
                        [#1715](https://github.com/opencybersecurityalliance/stix-shifter/pull/1715)
*  Added an AUTHORS.MD file [#1713](https://github.com/opencybersecurityalliance/stix-shifter/pull/1713)
                            [#1712](https://github.com/opencybersecurityalliance/stix-shifter/pull/1712)


### Fixes:

*  Removed the unused request toolbelt dependency [#1723](https://github.com/opencybersecurityalliance/stix-shifter/pull/1723)

### Dependency update:

--------------------------------------
## 7.0.11 (2024-07-11)

### Breaking changes:

### Deprecations:

### Changes:

*  Allowing_Tenant_To_Be_Optional [#1708](https://github.com/opencybersecurityalliance/stix-shifter/pull/1708)

### Fixes:

### Dependency update:

--------------------------------------

## 7.0.10 (2024-07-04)

### Breaking changes:

### Deprecations:

### Changes:

*  Trellix Endpoint Security HX Connector [#1695](https://github.com/opencybersecurityalliance/stix-shifter/pull/1695)
*  Symantec Endpoint Security UDI connector [#1694](https://github.com/opencybersecurityalliance/stix-shifter/pull/1694)
*  Update e2eStixBundle01.json [#1702](https://github.com/opencybersecurityalliance/stix-shifter/pull/1702)
*  Update e2eStixBundle01.json [#1698](https://github.com/opencybersecurityalliance/stix-shifter/pull/1698)
*  Update e2eStixBundle01.json [#1697](https://github.com/opencybersecurityalliance/stix-shifter/pull/1697)
*  Create e2eStixBundle01.json [#1696](https://github.com/opencybersecurityalliance/stix-shifter/pull/1696)
*  SumoLogics readme and supported_stix docs update [#1691](https://github.com/opencybersecurityalliance/stix-shifter/pull/1691)


### Fixes:

*  Fixing the unit test failing. [#1706](https://github.com/opencybersecurityalliance/stix-shifter/pull/1706)


### Dependency update:

--------------------------------------
## 7.0.9 (2024-05-23)

### Breaking changes:

### Deprecations:

### Changes:

*  Modified the ping endpoint [#1692](https://github.com/opencybersecurityalliance/stix-shifter/pull/1692)
*  Hided the API page size parameter view in console [#1690](https://github.com/opencybersecurityalliance/stix-shifter/pull/1690)
*  Added dialects from cloud siem Sumologic [#1686](https://github.com/opencybersecurityalliance/stix-shifter/pull/1686)


### Fixes:
*  Reaqta various mapping fixes [#1688](https://github.com/opencybersecurityalliance/stix-shifter/pull/1688)

### Dependency update:

--------------------------------------
## 7.0.7 (2024-05-07)

### Breaking changes:

### Deprecations:

### Changes:

*  CrowdStrike Logscale UDI Connector [#1631](https://github.com/opencybersecurityalliance/stix-shifter/pull/1631)
*  Nozomi UDI connector [#1656](https://github.com/opencybersecurityalliance/stix-shifter/pull/1656)
*  add feature to disable pagination and simplify API [#1676](https://github.com/opencybersecurityalliance/stix-shifter/pull/1676)
*  remove non-standard powershell fields for ECS [#1684](https://github.com/opencybersecurityalliance/stix-shifter/pull/1684)
*  Update code-coverage with new version of Codecov CLI  and token[#1682](https://github.com/opencybersecurityalliance/stix-shifter/pull/1682)

### Fixes:

*  Reaqta various mapping fixes [#1683](https://github.com/opencybersecurityalliance/stix-shifter/pull/1683)

### Dependency update:

--------------------------------------
## 7.0.6 (2024-04-16)

### Breaking changes:

### Deprecations:

### Changes:

*  adding support for LIKE operator in SumoLogic Module [#1670](https://github.com/opencybersecurityalliance/stix-shifter/pull/1670)
*  Infoblox connector source changes [#1660](https://github.com/opencybersecurityalliance/stix-shifter/pull/1660)
*  sumologic: use milliseconds since epoch for timestamps [#1668](https://github.com/opencybersecurityalliance/stix-shifter/pull/1668)
*  sumologic: add support for != [#1658](https://github.com/opencybersecurityalliance/stix-shifter/pull/1658)
*  map validator: additional checks for single quotes and extensions properties [#1667](https://github.com/opencybersecurityalliance/stix-shifter/pull/1667)


### Fixes:
*  Amazon athena resolve column not found exception [#1673](https://github.com/opencybersecurityalliance/stix-shifter/pull/1673)
*  Updated requirements and changed SSL purpose [#1664](https://github.com/opencybersecurityalliance/stix-shifter/pull/1664)

### Dependency update:
*  Bump json-fix from 0.5.2 to 1.0.0 in /stix_shifter [#1672](https://github.com/opencybersecurityalliance/stix-shifter/pull/1672)
*  Bump colorlog from 6.8.0 to 6.8.2 in /stix_shifter [#1671](https://github.com/opencybersecurityalliance/stix-shifter/pull/1671)
*  Bump regex from 2023.10.3 to 2023.12.25 in /stix_shifter [#1663](https://github.com/opencybersecurityalliance/stix-shifter/pull/1663)

--------------------------------------
## 7.0.4 (2024-03-14)

### Breaking changes:

### Deprecations:

### Changes:
*  Aligning config and lang en values to match a standard. [#1653](https://github.com/opencybersecurityalliance/stix-shifter/pull/1653)
*  Update to events mapping after content pack CEP changes [#1651](https://github.com/opencybersecurityalliance/stix-shifter/pull/1651)
*  Update README.md [#1652](https://github.com/opencybersecurityalliance/stix-shifter/pull/1652)
*  Sysdig exception handling updated [#1648](https://github.com/opencybersecurityalliance/stix-shifter/pull/1648)
*  Aligning the Amazon and Microsoft display names. [#1646](https://github.com/opencybersecurityalliance/stix-shifter/pull/1646)
*  Added sysdig bundle  [#1647](https://github.com/opencybersecurityalliance/stix-shifter/pull/1647)


### Fixes:
*  Remove default value from cert_verify parameters [#1654](https://github.com/opencybersecurityalliance/stix-shifter/pull/1654)

### Dependency update:
*  Bump aioboto3 from 12.0.0 to 12.1.0 in /stix_shifter [#1628](https://github.com/opencybersecurityalliance/stix-shifter/pull/1628)
*  update pyOpenSSL dependency to 24.1.0 [#1661](https://github.com/opencybersecurityalliance/stix-shifter/pull/1661)

--------------------------------------

## 7.0.2 (2024-01-25)

### Breaking changes:

### Deprecations:

### Changes:

*  Graph Security: Add login_host for national cloud authentication endpoint [#1641](https://github.com/opencybersecurityalliance/stix-shifter/pull/1641)
*  AWS Athena: Make access ids optional and remove verify false from boto client [#1629](https://github.com/opencybersecurityalliance/stix-shifter/pull/1629)
*  Add query batchsize(length) in common config.json [#1637](https://github.com/opencybersecurityalliance/stix-shifter/pull/1637)
*  QRadar: change START / STOP regex to include <= year 2000 [#1640](https://github.com/opencybersecurityalliance/stix-shifter/pull/1640)
*  Update machine ID field in QRadar module [#1634](https://github.com/opencybersecurityalliance/stix-shifter/pull/1634)
*  New Sysdig connector [#1630](https://github.com/opencybersecurityalliance/stix-shifter/pull/1630)
*  second half of email.* mapping for elastic_ecs [#1632](https://github.com/opencybersecurityalliance/stix-shifter/pull/1632)

### Fixes:

*  GCP: remove delete in result connector for chronicle [#1638](https://github.com/opencybersecurityalliance/stix-shifter/pull/1638)

### Dependency update:

--------------------------------------

## 7.0.1 (2023-12-11)

### Changes:

*  Replace docker with podman since it is still free to use [#1625](https://github.com/opencybersecurityalliance/stix-shifter/pull/1625)
*  Update group_ref keyword documenation [#1622](https://github.com/opencybersecurityalliance/stix-shifter/pull/1622)
*  add email-message translation to ecs [#1621](https://github.com/opencybersecurityalliance/stix-shifter/pull/1621)

### Fixes:

*  Add missing group param to connector configs, fix CrowdStrike spelling [#1626](https://github.com/opencybersecurityalliance/stix-shifter/pull/1626)

### Dependency update:

*  Bump colorlog from 6.7.0 to 6.8.0 in /stix_shifter [#1624](https://github.com/opencybersecurityalliance/stix-shifter/pull/1624)

--------------------------------------

## 7.0.0 (2023-11-27)

### Deprecations:

*  Make sure certificate is verified when required by RestApiClientAsync and deprecate selfSignedCert:false by-pass [#1620](https://github.com/opencybersecurityalliance/stix-shifter/pull/1620)

### Changes:

*  Cisco secure email added readme detailed file. [#1615](https://github.com/opencybersecurityalliance/stix-shifter/pull/1615)

### Fixes:

*  Remove future timestamp qualifier conditions [#1619](https://github.com/opencybersecurityalliance/stix-shifter/pull/1619)
*  Fix parameter assignment in error handling function [#1616](https://github.com/opencybersecurityalliance/stix-shifter/pull/1616)

--------------------------------------

## 6.3.0 (2023-11-02)

### Changes:

*  table of mapping script update for to-stix dialects [#1609](https://github.com/opencybersecurityalliance/stix-shifter/pull/1609)
*  cisco secure email connector [#1579](https://github.com/opencybersecurityalliance/stix-shifter/pull/1579)
*  add from stix mapping of OS in ECS [#1597](https://github.com/opencybersecurityalliance/stix-shifter/pull/1597)

### Fixes:

*  Fix Azure log analytics results translation. [#1612](https://github.com/opencybersecurityalliance/stix-shifter/pull/1612)
*  Vectra config changes [#1581](https://github.com/opencybersecurityalliance/stix-shifter/pull/1581)

### Dependency update:

*  Bump flatten-json from 0.1.13 to 0.1.14 in /stix_shifter [#1613](https://github.com/opencybersecurityalliance/stix-shifter/pull/1613)
*  Bump azure-identity from 1.14.1 to 1.15.0 in /stix_shifter [#1614](https://github.com/opencybersecurityalliance/stix-shifter/pull/1614)
*  Bump pyopenssl from 23.2.0 to 23.3.0 in /stix_shifter [#1610](https://github.com/opencybersecurityalliance/stix-shifter/pull/1610)
*  Bump aioboto3 from 11.3.1 to 12.0.0 in /stix_shifter [#1611](https://github.com/opencybersecurityalliance/stix-shifter/pull/1611)
*  Bump aioboto3 from 11.3.0 to 11.3.1 in /stix_shifter [#1607](https://github.com/opencybersecurityalliance/stix-shifter/pull/1607)
*  Bump flask from 2.3.3 to 3.0.0 in /stix_shifter [#1600](https://github.com/opencybersecurityalliance/stix-shifter/pull/1600)
*  Bump azure-identity from 1.12.0 to 1.14.1 in /stix_shifter [#1599](https://github.com/opencybersecurityalliance/stix-shifter/pull/1599)
*  Bump attrs from 22.2.0 to 23.1.0 in /stix_shifter [#1595](https://github.com/opencybersecurityalliance/stix-shifter/pull/1595)
*  Bump regex from 2023.8.8 to 2023.10.3 in /stix_shifter [#1598](https://github.com/opencybersecurityalliance/stix-shifter/pull/1598)
*  Upgrade urllib3 version in dependency [#1594](https://github.com/opencybersecurityalliance/stix-shifter/pull/1594)

--------------------------------------

## 6.2.2 (2023-10-03)

### Changes:

*  include connector type in logger error [#1585](https://github.com/opencybersecurityalliance/stix-shifter/pull/1585)
*  Add new screen shots to CLI Lab [#1576](https://github.com/opencybersecurityalliance/stix-shifter/pull/1576)

### Fixes:

*  Update Azure Log Analytics stix transmission to use BaseJsonSyncConnector [#1584](https://github.com/opencybersecurityalliance/stix-shifter/pull/1584)
*  Fixing authentication token handling [#1583](https://github.com/opencybersecurityalliance/stix-shifter/pull/1583)
*  allow host address input in MS Graph configuration [#1582](https://github.com/opencybersecurityalliance/stix-shifter/pull/1582)
*  fix coding lab [#1578](https://github.com/opencybersecurityalliance/stix-shifter/pull/1578)
*  Fix and update coding lab [#1577](https://github.com/opencybersecurityalliance/stix-shifter/pull/1577)

### Dependency update:

*  Bump aioboto3 from 11.2.0 to 11.3.0 in /stix_shifter [#1575](https://github.com/opencybersecurityalliance/stix-shifter/pull/1575)

--------------------------------------

## 6.2.1 (2023-09-07)

### Changes:

*  Update coding lab [#1566](https://github.com/opencybersecurityalliance/stix-shifter/pull/1566)
*  Vectra UDI connector [#1530](https://github.com/opencybersecurityalliance/stix-shifter/pull/1530)
*  add operator mapping example in CLI lab [#1564](https://github.com/opencybersecurityalliance/stix-shifter/pull/1564)
*  Lab landing page [#1563](https://github.com/opencybersecurityalliance/stix-shifter/pull/1563)
*  Update overview doc [#1561](https://github.com/opencybersecurityalliance/stix-shifter/pull/1561)

### Fixes:

*  resolve case insensitive regex in elastic ECS connector #1569 [#1573](https://github.com/opencybersecurityalliance/stix-shifter/pull/1573)
*  Fix readthedocs reference links [#1574](https://github.com/opencybersecurityalliance/stix-shifter/pull/1574)
*  Temporary fix for dialect not found map file [#1572](https://github.com/opencybersecurityalliance/stix-shifter/pull/1572)
*  Fix: skip empty list and string in stix objects [#1568](https://github.com/opencybersecurityalliance/stix-shifter/pull/1568)
*  Performance improvement of regex validation [#1565](https://github.com/opencybersecurityalliance/stix-shifter/pull/1565)
*  Fix ECS range queries with x-oca-event:start/end [#1559](https://github.com/opencybersecurityalliance/stix-shifter/pull/1559)

### Dependency update:

*  Bump jsonmerge from 1.9.0 to 1.9.2 in /stix_shifter [#1570](https://github.com/opencybersecurityalliance/stix-shifter/pull/1570)
*  Bump flask from 2.3.2 to 2.3.3 in /stix_shifter [#1567](https://github.com/opencybersecurityalliance/stix-shifter/pull/1567)
*  Bump aioboto3 from 11.1.0 to 11.2.0 in /stix_shifter [#1562](https://github.com/opencybersecurityalliance/stix-shifter/pull/1562)

--------------------------------------

## 6.1.1 (2023-08-15)

### Deprecations:

*  CLI lab updates and STIX validator removal [#1555](https://github.com/opencybersecurityalliance/stix-shifter/pull/1555)

### Changes:

*  Add readthedocs configurations [#1547](https://github.com/opencybersecurityalliance/stix-shifter/pull/1547)
*  Update connector coding lab [#1557](https://github.com/opencybersecurityalliance/stix-shifter/pull/1557)
*  Add docs folder [#1551](https://github.com/opencybersecurityalliance/stix-shifter/pull/1551)

### Fixes:

*  cli lab instruction fixes [#1558](https://github.com/opencybersecurityalliance/stix-shifter/pull/1558)
*  Fix variable assignment error with ECS event.start/end [#1556](https://github.com/opencybersecurityalliance/stix-shifter/pull/1556)
*  Mysql connector timeout fix [#1552](https://github.com/opencybersecurityalliance/stix-shifter/pull/1552)
*  fix cursor call in mysql API client [#1550](https://github.com/opencybersecurityalliance/stix-shifter/pull/1550)
*  Mapping Fixes for AWS GuardDuty [#1543](https://github.com/opencybersecurityalliance/stix-shifter/pull/1543)

--------------------------------------

## 6.0.3 (2023-07-27)

### Fixes:

*  Fix stix_bundle connector results translation [#1545](https://github.com/opencybersecurityalliance/stix-shifter/pull/1545)

--------------------------------------

## 6.0.2 (2023-07-26)

### Fixes:

*  map_validator: make sure 'object' name is a str [#1540](https://github.com/opencybersecurityalliance/stix-shifter/pull/1540)

### Dependency update:

*  update stix2-validator library to 3.1.4 [#1542](https://github.com/opencybersecurityalliance/stix-shifter/pull/1542)

--------------------------------------

## 6.0.1 (2023-07-24)

### Changes:

*  To-STIX mapping keyword documentation [#1529](https://github.com/opencybersecurityalliance/stix-shifter/pull/1529)

### Fixes:

*  Setup fix for installing libraries from commit hash [#1539](https://github.com/opencybersecurityalliance/stix-shifter/pull/1539)

--------------------------------------

## 6.0.0 (2023-07-21)

### Breaking changes:

*  Adding to stix dialect feature [#1231](https://github.com/opencybersecurityalliance/stix-shifter/pull/1231)

### Deprecations:

* Removed various unfinished and abandoned connectors [#1537](https://github.com/opencybersecurityalliance/stix-shifter/pull/1537)

### Changes:

*  AWS GuardDuty UDI Connector [#1525](https://github.com/opencybersecurityalliance/stix-shifter/pull/1525)
*  Framework Changes for Handling Nested List of Dictionaries [#1516](https://github.com/opencybersecurityalliance/stix-shifter/pull/1516)
*  Move results processing to transmission results [#1519](https://github.com/opencybersecurityalliance/stix-shifter/pull/1519)
*  to-STIX dialects documentation added [#1515](https://github.com/opencybersecurityalliance/stix-shifter/pull/1515)
*  Splunk UDI Connector -Upgrade [#1479](https://github.com/opencybersecurityalliance/stix-shifter/pull/1479)
*  Azure log analytics mapping improvements [#1496](https://github.com/opencybersecurityalliance/stix-shifter/pull/1496)
*  Update CLA link in CONTRIBUTING.md [#1517](https://github.com/opencybersecurityalliance/stix-shifter/pull/1517)
*  Reaqta name change [#1514](https://github.com/opencybersecurityalliance/stix-shifter/pull/1514)

### Fixes:

*  ibm_security_verify: fixes [#1522](https://github.com/opencybersecurityalliance/stix-shifter/pull/1522)
*  LIKE operator only added for events queries [#1521](https://github.com/opencybersecurityalliance/stix-shifter/pull/1521)

### Dependency update:

*  Attrs dependency fix and connector cleanup [#1537](https://github.com/opencybersecurityalliance/stix-shifter/pull/1537)
*  fix #1533 with type import update [#1534](https://github.com/opencybersecurityalliance/stix-shifter/pull/1534)
*  Remove ancient 'uuid==1.30' from requirements.txt [#1524](https://github.com/opencybersecurityalliance/stix-shifter/pull/1524)

--------------------------------------

## 5.3.1 (2023-06-15)

### Deprecations:

*  remove SNI from authentication options [#1498](https://github.com/opencybersecurityalliance/stix-shifter/pull/1498)

### Changes:

*  Error messaging update [#1503](https://github.com/opencybersecurityalliance/stix-shifter/pull/1503)

*  Remove cybox checks from map validator [#1504](https://github.com/opencybersecurityalliance/stix-shifter/pull/1504)
*  remove cybox false flag for observed-data properties [#1502](https://github.com/opencybersecurityalliance/stix-shifter/pull/1502)
*  Async support in Datadog connector [#1492](https://github.com/opencybersecurityalliance/stix-shifter/pull/1492)
*  ReaQta Use TTP Custom Object [#1473](https://github.com/opencybersecurityalliance/stix-shifter/pull/1473)
*  default translator support [#1491](https://github.com/opencybersecurityalliance/stix-shifter/pull/1491)
*  Add description to stix-bundle connector README [#1497](https://github.com/opencybersecurityalliance/stix-shifter/pull/1497)
*  minor code cleanup [#1494](https://github.com/opencybersecurityalliance/stix-shifter/pull/1494)
*  Better error reporting for bad certificate [#1490](https://github.com/opencybersecurityalliance/stix-shifter/pull/1490)
*  timeout max -> 1 hour; result limit -> 10 million [#1487](https://github.com/opencybersecurityalliance/stix-shifter/pull/1487)

### Fixes:

*  Patch elastic mappings [#1501](https://github.com/opencybersecurityalliance/stix-shifter/pull/1501)
*  elastic_ecs: fix email-addr:value mappings in 'from' maps [#1508](https://github.com/opencybersecurityalliance/stix-shifter/pull/1508)
*  x-oca-event.code switch from int to str [#1499](https://github.com/opencybersecurityalliance/stix-shifter/pull/1499)
*  fix mapping references in elastic-ecs connector [#1471](https://github.com/opencybersecurityalliance/stix-shifter/pull/1471)

--------------------------------------

## 5.3.0 (2023-05-15)

### Changes:

*  SDO connector cleanup and table of mappings [#1484](https://github.com/opencybersecurityalliance/stix-shifter/pull/1484)
*  error_test 2queries [#1483](https://github.com/opencybersecurityalliance/stix-shifter/pull/1483)
*  DShield connector [#1443](https://github.com/opencybersecurityalliance/stix-shifter/pull/1443)
*  RecordedFuture connector [#1462](https://github.com/opencybersecurityalliance/stix-shifter/pull/1462)
*  Cisco Secure Malware Analytics (formerly Threat Grid) Connector [#1460](https://github.com/opencybersecurityalliance/stix-shifter/pull/1460)
*  Virus total connector [#1458](https://github.com/opencybersecurityalliance/stix-shifter/pull/1458)
*  ThreatQ connector [#1461](https://github.com/opencybersecurityalliance/stix-shifter/pull/1461)
*  Add Intezer connector [#1457](https://github.com/opencybersecurityalliance/stix-shifter/pull/1457)
*  to_stix_map validator [#1469](https://github.com/opencybersecurityalliance/stix-shifter/pull/1469)
*  Alienvault OpenThreatExchange connector [#1442](https://github.com/opencybersecurityalliance/stix-shifter/pull/1442)
*  Adding new graph alert resource support in Graph security module [#1439](https://github.com/opencybersecurityalliance/stix-shifter/pull/1439)
opencybersecurityalliance/stix-shifter/pull/1448)
*  Add AbuseIPDB Connector [#1441](https://github.com/opencybersecurityalliance/stix-shifter/pull/1441)

### Fixes:

*  set alert options default value to false [#1481](https://github.com/opencybersecurityalliance/stix-shifter/pull/1481)
*  Updated Config changes for GCP Chronicle for develop branch [#1476](https://github.com/opencybersecurityalliance/stix-shifter/pull/1476)
*  QRadar - Remove Zero Values from IP and Mac Results [#1468](https://github.com/opencybersecurityalliance/stix-shifter/pull/1468)
*  Update stix2.1 mapping files in azure sentinel module [#1472](https://github.com/opencybersecurityalliance/stix-shifter/pull/1472)
*  Elastic-ecs: update dialect attributes with `.keyword` [#1474](https://github.com/opencybersecurityalliance/stix-shifter/pull/1474)
*  fix error_test transform_query [#1470](https://github.com/opencybersecurityalliance/stix-shifter/pull/1470)
*  mapping fixes for Microsoft Graph Security [#1420](https://github.com/opencybersecurityalliance/stix-shifter/pull/1420)
*  Added timeout for API client calls [#1459](https://github.com/opencybersecurityalliance/stix-shifter/pull/1459)
*  Elastic-ecs mapping: consolidate `x-ecs-container` attributes into the `x-oca-asset` object [#1448](https://github.com/
*  Elastic-ecs: Patch observer mapping to `x-oca-asset` object [#1464](https://github.com/opencybersecurityalliance/stix-shifter/pull/1464)
*  enable observer data in transmit [#1453](https://github.com/opencybersecurityalliance/stix-shifter/pull/1453)
*  Fix proxy create_results_connection method [#1463](https://github.com/opencybersecurityalliance/stix-shifter/pull/1463)
*  Elastic-ecs: consolidate asset identifier [#1477](https://github.com/opencybersecurityalliance/stix-shifter/pull/1477)

### Dependency update:

*  Added urllib3 1.26.15 to connector requirements [#1482](https://github.com/opencybersecurityalliance/stix-shifter/pull/1482)
*  Bump flask from 2.3.1 to 2.3.2 in /stix_shifter [#1454](https://github.com/opencybersecurityalliance/stix-shifter/pull/1454)

--------------------------------------

## 5.2.1 (2023-05-01)

### Dependency update:

*  set urllib3 library requirement [#1449](https://github.com/opencybersecurityalliance/stix-shifter/pull/1449)

--------------------------------------

## 5.2.0 (2023-04-28)

### Breaking changes:

*  Change QRadar domain name mapping [#1342](https://github.com/opencybersecurityalliance/stix-shifter/pull/1342)

### Changes:

*  update table of mappings for MS Graph, Elastic ECS, Microsoft Defender [#1445](https://github.com/opencybersecurityalliance/stix-shifter/pull/1445)
*  Elastic-ecs mapping improvements for network traffic attributes [#1410](https://github.com/opencybersecurityalliance/stix-shifter/pull/1410)
*  Update Reversinglabs connector [#1436](https://github.com/opencybersecurityalliance/stix-shifter/pull/1436)
*  Documentation updates [#1435](https://github.com/opencybersecurityalliance/stix-shifter/pull/1435)
*  Correct network-traffic mappings for elastic_ecs [#1430](https://github.com/opencybersecurityalliance/stix-shifter/pull/1430)
*  Msatp with alerts refactor [#1404](https://github.com/opencybersecurityalliance/stix-shifter/pull/1404)
*  MSATP async token, removed ADAL lib [#1428](https://github.com/opencybersecurityalliance/stix-shifter/pull/1428)
*  Cleaning up from requests lib [#1429](https://github.com/opencybersecurityalliance/stix-shifter/pull/1429)
*  IBM Verify Privilege Vault api path changes [#1424](https://github.com/opencybersecurityalliance/stix-shifter/pull/1424)
*  Added async to Azure sentinal [#1419](https://github.com/opencybersecurityalliance/stix-shifter/pull/1419)
*  Change config labels to sentence case [#1417](https://github.com/opencybersecurityalliance/stix-shifter/pull/1417)
*  Update README for IBM Verify Privilege Vault (Secret Server) connector  [#1402](https://github.com/opencybersecurityalliance/stix-shifter/pull/1402)
*  hard coded base uri in microsoft graph security connector [#1406](https://github.com/opencybersecurityalliance/stix-shifter/pull/1406)
*  Add metadata CLI and documenations [#1396](https://github.com/opencybersecurityalliance/stix-shifter/pull/1396)
*  Pagination handled for azure_log_analytics [#1398](https://github.com/opencybersecurityalliance/stix-shifter/pull/1398)
*  Elastic ecs module readme [#1400](https://github.com/opencybersecurityalliance/stix-shifter/pull/1400)

### Fixes:

*  fix url value property in azure mapping [#1444](https://github.com/opencybersecurityalliance/stix-shifter/pull/1444)
*  Okta Error Code Mapping Changes for develop Branch [#1434](https://github.com/opencybersecurityalliance/stix-shifter/pull/1434)
*  Fix: Graph API fails if used without lamda operators on collection type properties [#1421](https://github.com/opencybersecurityalliance/stix-shifter/pull/1421)
*  Fix for Athena error handling, error log printing in tranlsation [#1415](https://github.com/opencybersecurityalliance/stix-shifter/pull/1415)
*  Fixed error handling for darktrace on raw html response [#1416](https://github.com/opencybersecurityalliance/stix-shifter/pull/1416)

### Dependency update:

*  Bump flask from 2.2.3 to 2.3.1 in /stix_shifter [#1440](https://github.com/opencybersecurityalliance/stix-shifter/pull/1440)
*  Bump json-fix from 0.5.1 to 0.5.2 in /stix_shifter [#1426](https://github.com/opencybersecurityalliance/stix-shifter/pull/1426)
*  Bump aioboto3 from 11.0.1 to 11.1.0 in /stix_shifter [#1411](https://github.com/opencybersecurityalliance/stix-shifter/pull/1411)
*  Bump pyopenssl from 23.1.0 to 23.1.1 in /stix_shifter [#1405](https://github.com/opencybersecurityalliance/stix-shifter/pull/1405)
*  Bump pyopenssl from 23.0.0 to 23.1.0 in /stix_shifter [#1401](https://github.com/opencybersecurityalliance/stix-shifter/pull/1401)

--------------------------------------

## 5.1.1 (2023-03-21)

### Changes:

* Added process:x_unique_id property to Splunk [#1389](https://github.com/opencybersecurityalliance/stix-shifter/pull/1389)
* get configs [#1392](https://github.com/opencybersecurityalliance/stix-shifter/pull/1392)
* GitHub action update [#1385](https://github.com/opencybersecurityalliance/stix-shifter/pull/1385)

### Fixes:

* Added metadata changes for GCP Chronicle [#1393](https://github.com/opencybersecurityalliance/stix-shifter/pull/1393)
* Splunk: Fix MAC address to display in proper STIX format [#1386](https://github.com/opencybersecurityalliance/stix-shifter/pull/1386)
* Updated custom properties mapping in Okta with 'x_' prefix [#1387](https://github.com/opencybersecurityalliance/stix-shifter/pull/1387)
* Await async fixes [#1391](https://github.com/opencybersecurityalliance/stix-shifter/pull/1391)
* fix json loads of data arg in stix-shifter CLI [#1394](https://github.com/opencybersecurityalliance/stix-shifter/pull/1394)

### Dependency update:

* Bump aiohttp-retry from 2.4.0 to 2.8.3 in /stix_shifter [#1374](https://github.com/opencybersecurityalliance/stix-shifter/pull/1374)
* Consolidate `network-traffic`, `user-account`, `file` objects in the elastic_ecs connector mapping [#1378](https://github.com/opencybersecurityalliance/stix-shifter/pull/1378)
* Fix #1375, optimize get_pagesize() function call, and add testcases  [#1384](https://github.com/opencybersecurityalliance/stix-shifter/pull/1384)
* Async changes for Okta UDI connector [#1383](https://github.com/opencybersecurityalliance/stix-shifter/pull/1383)

--------------------------------------

## 5.1.0 (2023-03-08)

### Breaking changes:

* Support for asynchronous API calls in transmission modules [#1038](https://github.com/opencybersecurityalliance/stix-shifter/pull/1038)

### Deprecations:

* Removed boto3 dependency in favor of aioboto3

### Changes:

* Add Okta table of mappings and update elastic ECS [#1372](https://github.com/opencybersecurityalliance/stix-shifter/pull/1372)
* Okta connector [#1323](https://github.com/opencybersecurityalliance/stix-shifter/pull/1323)
* support large query with elastic search_after pagination [#1299](https://github.com/opencybersecurityalliance/stix-shifter/pull/1299)
* cybereason quick ping [#1350](https://github.com/opencybersecurityalliance/stix-shifter/pull/1350)
* aiogoogle module used for async changes in gcp_chronicle [#1331](https://github.com/opencybersecurityalliance/stix-shifter/pull/1331)
* base release5.0.x - Cookies are handled for cybereason asynchronous c… [#1313](https://github.com/opencybersecurityalliance/stix-shifter/pull/1313)
* Paloalto - changes done to map process.x_unique_id with data source field actor_process_instance_id [#1318](https://github.com/opencybersecurityalliance/stix-shifter/pull/1318)
* Added cookie support [#1310](https://github.com/opencybersecurityalliance/stix-shifter/pull/1310)
* Removed language common fields [#984](https://github.com/opencybersecurityalliance/stix-shifter/pull/984)
* Updated RHACS connector to support self signed certificate authentication [#1174](https://github.com/opencybersecurityalliance/stix-shifter/pull/1174)

### Fixes:

* QRadarEpochToTimestamp for exponential notation [#1352](https://github.com/opencybersecurityalliance/stix-shifter/pull/1352)
* Remove the x-ecs-process and x-ecs-file entities from elastic_ecs mapping [#1335](https://github.com/opencybersecurityalliance/stix-shifter/pull/1335)
* azure_log_analytics: fix translation of IN operator [#1355](https://github.com/opencybersecurityalliance/stix-shifter/pull/1355)
* Build warnings fix [#1347](https://github.com/opencybersecurityalliance/stix-shifter/pull/1347)
* Updating file hash mapping for Athena OCSF support [#1345](https://github.com/opencybersecurityalliance/stix-shifter/pull/1345)
* upddate mapping for Reaqta [#1326](https://github.com/opencybersecurityalliance/stix-shifter/pull/1326)
* update mapping tables to show both comparision and observation AND OR operators [#1348](https://github.com/opencybersecurityalliance/stix-shifter/pull/1348)
* Update OCSF network traffic mappings [#1332](https://github.com/opencybersecurityalliance/stix-shifter/pull/1332)
* fix mapping error [#1320](https://github.com/opencybersecurityalliance/stix-shifter/pull/1320)
* Fix Reqata SITX 2.1 mappings for image_ref [#1291](https://github.com/opencybersecurityalliance/stix-shifter/pull/1291)
* elastic_ecs: remove unneeded ValueToList transformer from event.category mapping [#1305](https://github.com/opencybersecurityalliance/stix-shifter/pull/1305)
* elastic_ecs: fix STIX 2.1 results translation [#1306](https://github.com/opencybersecurityalliance/stix-shifter/pull/1306)
* Added aiohttp ssl certificate proper handling [#1308](https://github.com/opencybersecurityalliance/stix-shifter/pull/1308)
* Auth header serialize fix, response wraper fixes [#1298](https://github.com/opencybersecurityalliance/stix-shifter/pull/1298)

### Dependency update:

* Bump aioboto3 from 10.4.0 to 11.0.1 in /stix_shifter [#1368](https://github.com/opencybersecurityalliance/stix-shifter/pull/1368)
* Bump aiomysql from 0.0.21 to 0.1.1 in /stix_shifter [#1369](https://github.com/opencybersecurityalliance/stix-shifter/pull/1369)
* Bump boto3 from 1.26.78 to 1.26.84 in /stix_shifter [#1363](https://github.com/opencybersecurityalliance/stix-shifter/pull/1363)
* Bump boto3 from 1.26.74 to 1.26.78 in /stix_shifter [#1344](https://github.com/opencybersecurityalliance/stix-shifter/pull/1344)
* Bump boto3 from 1.26.64 to 1.26.74 in /stix_shifter [#1337](https://github.com/opencybersecurityalliance/stix-shifter/pull/1337)
* Bump boto3 from 1.26.55 to 1.26.64 in /stix_shifter [#1317](https://github.com/opencybersecurityalliance/stix-shifter/pull/1317)

--------------------------------------

## 4.6.0 (2023-01-24)

### Changes:

* Instructions for the usage of custom mappings [#1274](https://github.com/opencybersecurityalliance/stix-shifter/pull/1274)
* Add log analytics API support to azure sentinel connector [#1214](https://github.com/opencybersecurityalliance/stix-shifter/pull/1214)
* Update OCSF schema in Athena mappings [#1245](https://github.com/opencybersecurityalliance/stix-shifter/pull/1245)
* splunk: allow multiple, comma-separated index names in the index option [#1271](https://github.com/opencybersecurityalliance/stix-shifter/pull/1271)
* Rename azure sentinel to Microsoft Graph Security Connector [#1212](https://github.com/opencybersecurityalliance/stix-shifter/pull/1212)
* elastic_ecs: add beats dialect [#1208](https://github.com/opencybersecurityalliance/stix-shifter/pull/1208)
* update script to create sql database [#1228](https://github.com/opencybersecurityalliance/stix-shifter/pull/1228)
* Test for START STOP timestamp format [#1218](https://github.com/opencybersecurityalliance/stix-shifter/pull/1218)
* Updated RHACS connector to support self signed certificate authentication [#1174](https://github.com/opencybersecurityalliance/stix-shifter/pull/1174)

### Fixes:

* Mapping updates for Guardium STIX 2.1 [#1102](https://github.com/opencybersecurityalliance/stix-shifter/pull/1102)
* Add default time range to STIX Bundle connector [#1288](https://github.com/opencybersecurityalliance/stix-shifter/pull/1288)
* Updated code to handle maximum query length limitation in darktrace.  [#1259](https://github.com/opencybersecurityalliance/stix-shifter/pull/1259)
* Use raw strings for regex [#1276](https://github.com/opencybersecurityalliance/stix-shifter/pull/1276)
* Updated changes for the issue #1270 [#1272](https://github.com/opencybersecurityalliance/stix-shifter/pull/1272)
* change all two lettered property names [#1251](https://github.com/opencybersecurityalliance/stix-shifter/pull/1251)
* mapping fixes for splunk [#1239](https://github.com/opencybersecurityalliance/stix-shifter/pull/1239)
* splunk: use like, cidrmatch SPL functions for LIKE, ISSUBSET operators [#1244](https://github.com/opencybersecurityalliance/stix-shifter/pull/1244)
* Fix supported property exporter to handle from-STIX fields not wrapped in a list [#1236](https://github.com/opencybersecurityalliance/stix-shifter/pull/1236)
* fix domain_ioc mapping (removal of network_traffic ref) [#1226](https://github.com/opencybersecurityalliance/stix-shifter/pull/1226)
* Updated cybereason code to fix the issue #1215 [#1224](https://github.com/opencybersecurityalliance/stix-shifter/pull/1224)
* Darktrace timeout exception handled [#1210](https://github.com/opencybersecurityalliance/stix-shifter/pull/1210)
* Aws athena ocsf fixes [#1182](https://github.com/opencybersecurityalliance/stix-shifter/pull/1182)
* elastic_ecs: more fixes for LIKE and MATCHES [#1195](https://github.com/opencybersecurityalliance/stix-shifter/pull/1195)

### Dependency update:

* Bump boto3 from 1.26.41 to 1.26.55 in /stix_shifter [#1293](https://github.com/opencybersecurityalliance/stix-shifter/pull/1293)
* Bump json-fix from 0.5.0 to 0.5.1 in /stix_shifter [#1196](https://github.com/opencybersecurityalliance/stix-shifter/pull/1196)
* Bump pyopenssl from 22.1.0 to 23.0.0 in /stix_shifter [#1264](https://github.com/opencybersecurityalliance/stix-shifter/pull/1264)
* Bump boto3 from 1.26.10 to 1.26.41 in /stix_shifter [#1263](https://github.com/opencybersecurityalliance/stix-shifter/pull/1263)

-------------------------------------

## 4.5.2 (2022-11-21)

### Changes:

* AWS Athena, added external id support [#1187](https://github.com/opencybersecurityalliance/stix-shifter/pull/1187)
* Update aws athena supported attribute [#1184](https://github.com/opencybersecurityalliance/stix-shifter/pull/1184)
* Update AWS Athena for OCSF schema support [#1178](https://github.com/opencybersecurityalliance/stix-shifter/pull/1178)
* Upgrade pytests version for dev environment [#1170](https://github.com/opencybersecurityalliance/stix-shifter/pull/1170)
* ocsf schema support in aws Athena [#1134](https://github.com/opencybersecurityalliance/stix-shifter/pull/1134)
* Add RHACS and Google Chronicle group params [#1150](https://github.com/opencybersecurityalliance/stix-shifter/pull/1150)
* return proxy translation error [#1130](https://github.com/opencybersecurityalliance/stix-shifter/pull/1130)
* Updated the readme mappings for GCP Chronicle [#1146](https://github.com/opencybersecurityalliance/stix-shifter/pull/1146)

### Fixes:

* Updated to support query without milliseconds in darktrace connector [#1199](https://github.com/opencybersecurityalliance/stix-shifter/pull/1199)
* fix formatting of commit list generated by changelog script [#1200](https://github.com/opencybersecurityalliance/stix-shifter/pull/1200)
* fixed timestamp issue for start and end filter and mapping correction [#1142](https://github.com/opencybersecurityalliance/stix-shifter/pull/1142)
* Fixed pagination and meta files delete for aws athena [#1176](https://github.com/opencybersecurityalliance/stix-shifter/pull/1176)
* gcp chronicle: removed an invalid unittest [#1166](https://github.com/opencybersecurityalliance/stix-shifter/pull/1166)
* Remove optional word from indices label [#1157](https://github.com/opencybersecurityalliance/stix-shifter/pull/1157)
* Fixed deployment script with --platform linux/amd64 [#1154](https://github.com/opencybersecurityalliance/stix-shifter/pull/1154)
* Updated connector.py file for the bug fix #1103 [#1104](https://github.com/opencybersecurityalliance/stix-shifter/pull/1104)

### Dependency update:

* Bump flask from 2.0.3 to 2.2.2 in /stix_shifter [#1072](https://github.com/opencybersecurityalliance/stix-shifter/pull/1072)
* Bump requests-toolbelt from 0.9.1 to 0.10.1 in /stix_shifter [#1180](https://github.com/opencybersecurityalliance/stix-shifter/pull/1180)
* Bump jsonmerge from 1.8.0 to 1.9.0 in /stix_shifter [#1194](https://github.com/opencybersecurityalliance/stix-shifter/pull/1194)
* Bump boto3 from 1.26.5 to 1.26.10 in /stix_shifter [#1193](https://github.com/opencybersecurityalliance/stix-shifter/pull/1193)
* Bump boto3 from 1.21.21 to 1.26.1 in /stix_shifter [#1175](https://github.com/opencybersecurityalliance/stix-shifter/pull/1175)
* Bump pyopenssl from 21.0.0 to 22.1.0 in /stix_shifter [#1144](https://github.com/opencybersecurityalliance/stix-shifter/pull/1144)

--------------------------------------

## 4.4.0 (2022-10-06)

### Changes:

* Add optional group parameter to connector configs [#1094](https://github.com/opencybersecurityalliance/stix-shifter/pull/1094)
* Adding GCP Chronicle UDI Connector [#1075](https://github.com/opencybersecurityalliance/stix-shifter/pull/1075)
* Update Secretserver mappings [#1092](https://github.com/opencybersecurityalliance/stix-shifter/pull/1092)
* Connector template for lab [#1117](https://github.com/opencybersecurityalliance/stix-shifter/pull/1117)

### Fixes:

* Get rid of StixObjectIdEncoder [#1124](https://github.com/opencybersecurityalliance/stix-shifter/pull/1124)
* Fixed IBM Security Verify config file [#1125](https://github.com/opencybersecurityalliance/stix-shifter/pull/1125)
* edits to coding lab [#1120](https://github.com/opencybersecurityalliance/stix-shifter/pull/1120)
* Update epoch time to 10 digits for demo data [#1119](https://github.com/opencybersecurityalliance/stix-shifter/pull/1119)
* update coding lab [#1114](https://github.com/opencybersecurityalliance/stix-shifter/pull/1114)
* Lab fixes [#1116](https://github.com/opencybersecurityalliance/stix-shifter/pull/1116)

### Dependency update:

* Bump colorlog from 6.6.0 to 6.7.0 in /stix_shifter [#1095](https://github.com/opencybersecurityalliance/stix-shifter/pull/1095)

--------------------------------------

## 4.3.0 (2022-09-09)

### Changes:

* CLI and coding tutorials [#1105](https://github.com/opencybersecurityalliance/stix-shifter/pull/1105)
* Adding RHACS(StackRox) UDI connector [#1055](https://github.com/opencybersecurityalliance/stix-shifter/pull/1055)
* Added Utility for normalization of connectors [#1078](https://github.com/opencybersecurityalliance/stix-shifter/pull/1078)
* CrowdStrike: Added User-Agent string to API Client for tracking [#1064](https://github.com/opencybersecurityalliance/stix-shifter/pull/1064)
* Process unique ID [#1051](https://github.com/opencybersecurityalliance/stix-shifter/pull/1051)
* Added matcher lib support for 2.1 [#960](https://github.com/opencybersecurityalliance/stix-shifter/pull/960)
* In query Enhancement [#1022](https://github.com/opencybersecurityalliance/stix-shifter/pull/1022)
* Infoblox add docstrings for module [#719](https://github.com/opencybersecurityalliance/stix-shifter/pull/719)
* Release/3.3.x json to stix [#598](https://github.com/opencybersecurityalliance/stix-shifter/pull/598)

### Fixes:

* Id contributing properties from json to py [#1093](https://github.com/opencybersecurityalliance/stix-shifter/pull/1093)
* splunk: fix STIX timestamp processing [#1084](https://github.com/opencybersecurityalliance/stix-shifter/pull/1084)
* Fixing absolute path for id_contributing_properties.json [#1079](https://github.com/opencybersecurityalliance/stix-shifter/pull/1079)
* Fix mapping and added hex to int transformer [#1068](https://github.com/opencybersecurityalliance/stix-shifter/pull/1068)
* Downgrade boto3 version to 1.21.21 [#1036](https://github.com/opencybersecurityalliance/stix-shifter/pull/1036)
* Fix the length of the results of Qradar connector [#1034](https://github.com/opencybersecurityalliance/stix-shifter/pull/1034)
* Revert "Change certificate parameter type for consistency" [#1031](https://github.com/opencybersecurityalliance/stix-shifter/pull/1031)
* reaqta: enable certification authentication [#1028](https://github.com/opencybersecurityalliance/stix-shifter/pull/1028)
* fix configuration in proofpoint and sumologic [#745](https://github.com/opencybersecurityalliance/stix-shifter/pull/745)
* Validator review code change for Proofpoint [#739](https://github.com/opencybersecurityalliance/stix-shifter/pull/739)

--------------------------------------

## 4.2.0 (2022-06-29)

### Changes:

* Added reaqta from_stix generate script [#977](https://github.com/opencybersecurityalliance/stix-shifter/pull/977)
* Change certificate parameter type [#1000](https://github.com/opencybersecurityalliance/stix-shifter/pull/1000)
* splunk: add index to options [#993](https://github.com/opencybersecurityalliance/stix-shifter/pull/993)
* Best practices document for connector development [#986](https://github.com/opencybersecurityalliance/stix-shifter/pull/986)
* Update supported attributes and overview readme [#976](https://github.com/opencybersecurityalliance/stix-shifter/pull/976)
* Guardium rel 1.10 [#958](https://github.com/opencybersecurityalliance/stix-shifter/pull/958)
* Updated the readme mappings for darktrace. [#942](https://github.com/opencybersecurityalliance/stix-shifter/pull/942)
* Added Darktrace UDI connector. [#896](https://github.com/opencybersecurityalliance/stix-shifter/pull/896)
* Update table of mappings for ReaQta and IN operator support [#937](https://github.com/opencybersecurityalliance/stix-shifter/pull/937)
* Updated the Readme mapping files [#932](https://github.com/opencybersecurityalliance/stix-shifter/pull/932)
* Adding SentinelOne UDI connector [#888](https://github.com/opencybersecurityalliance/stix-shifter/pull/888)
* Reaqta connector [#879](https://github.com/opencybersecurityalliance/stix-shifter/pull/879)

### Fixes:

* Fixed unique_cybox_objects storing [#1005](https://github.com/opencybersecurityalliance/stix-shifter/pull/1005)
* fallback to random UUID if STIX object contains no defined id contributing properties [#990](https://github.com/opencybersecurityalliance/stix-shifter/pull/990)
* error_test timeouts on translate and status [#987](https://github.com/opencybersecurityalliance/stix-shifter/pull/987)
* fix two deprecation warnings [#940](https://github.com/opencybersecurityalliance/stix-shifter/pull/940)
* splunk: fix mapping of process command line [#918] [#971](https://github.com/opencybersecurityalliance/stix-shifter/pull/971)
* splunk: fix incorrect dst_ref.value mapping [#919] [#970](https://github.com/opencybersecurityalliance/stix-shifter/pull/970)
* splunk: fix translation of IN, LIKE, and MATCHES [#789] [#969](https://github.com/opencybersecurityalliance/stix-shifter/pull/969)
* fix eventType mapping for reaqta connector [#967](https://github.com/opencybersecurityalliance/stix-shifter/pull/967)
* Reaqta: Fix network traffic for inbound and mapping update [#952](https://github.com/opencybersecurityalliance/stix-shifter/pull/952)
* Remove deprecated SourceImage field from aql search [#950](https://github.com/opencybersecurityalliance/stix-shifter/pull/950)
* Reaqta: implemented grater/less fields translation, fixed from_stix fields sorting, fixed unittests [#938](https://github.com/opencybersecurityalliance/stix-shifter/pull/938)
* Reaqta Connector:Update mapping and unittest [#964](https://github.com/opencybersecurityalliance/stix-shifter/pull/964)
* Fixed stix parsing with setvalue types [#907](https://github.com/opencybersecurityalliance/stix-shifter/pull/907)

### Dependency update:

* Bump boto3 from 1.21.5 to 1.22.10 [#935](https://github.com/opencybersecurityalliance/stix-shifter/pull/935)
* Bump xmltodict from 0.12.0 to 0.13.0 [#934](https://github.com/opencybersecurityalliance/stix-shifter/pull/934)
* Bump stix2-matcher from 2.0.1 to 2.0.2 [#915](https://github.com/opencybersecurityalliance/stix-shifter/pull/915)

--------------------------------------

## 4.1.0 (2022-04-12)

### Changes:

* Updated mappings for PaloAlto readme [#890](https://github.com/opencybersecurityalliance/stix-shifter/pull/890)
* Added Palo Alto Cortext XDR UDI Connector [#858](https://github.com/opencybersecurityalliance/stix-shifter/pull/858)
* package utils/normalization [#882](https://github.com/opencybersecurityalliance/stix-shifter/pull/882)
* add sample transformer to template modules [#870](https://github.com/opencybersecurityalliance/stix-shifter/pull/870)
* Added IN operator for Vision One UDI connector [#861](https://github.com/opencybersecurityalliance/stix-shifter/pull/861)
* Update arcsight custom attributes [#865](https://github.com/opencybersecurityalliance/stix-shifter/pull/865)
* results metadata support [#813](https://github.com/opencybersecurityalliance/stix-shifter/pull/813)
* Template projects rename [#854](https://github.com/opencybersecurityalliance/stix-shifter/pull/854)
* doc update for operators and custom transformers [#846](https://github.com/opencybersecurityalliance/stix-shifter/pull/846)
* Adding BaseNormalization Class [#820](https://github.com/opencybersecurityalliance/stix-shifter/pull/820)
* Add IN operator for sumologic connector [#845](https://github.com/opencybersecurityalliance/stix-shifter/pull/845)
* Adding IN operator support to CB connector [#835](https://github.com/opencybersecurityalliance/stix-shifter/pull/835)
* Stix validator update [#838](https://github.com/opencybersecurityalliance/stix-shifter/pull/838)
* CrowdStrike: Adding IN operator support [#842](https://github.com/opencybersecurityalliance/stix-shifter/pull/842)
* Adding changelog [#833](https://github.com/opencybersecurityalliance/stix-shifter/pull/833)
* New UDI connector module for IBM Security Verify [#802](https://github.com/opencybersecurityalliance/stix-shifter/pull/802)
* Adding connector name in the error responses [#824](https://github.com/opencybersecurityalliance/stix-shifter/pull/824)

### Fixes:

* use simple setup for mysql endpoints [#885](https://github.com/opencybersecurityalliance/stix-shifter/pull/885)
* Mysql tablename fix [#868](https://github.com/opencybersecurityalliance/stix-shifter/pull/868)
* RestApiClient in stix-shifter using https mount call [#864](https://github.com/opencybersecurityalliance/stix-shifter/pull/864)
* Fixed StixObjectId conversion to string [#863](https://github.com/opencybersecurityalliance/stix-shifter/pull/863)
* Fixed stix-validator 3.0.2 usage in translator [#851](https://github.com/opencybersecurityalliance/stix-shifter/pull/851)
* remove process_user field mapping from windows-registry-key stix object [#850](https://github.com/opencybersecurityalliance/stix-shifter/pull/850)
* Secret server 1.9 [#836](https://github.com/opencybersecurityalliance/stix-shifter/pull/836)
* Fixed calculating and updating deterministic IDs and the… [#826](https://github.com/opencybersecurityalliance/stix-shifter/pull/826)

--------------------------------------

## 4.0.1 (2022-03-01)

### Changes:

* CrowdStrike connector mapping update [#823](https://github.com/opencybersecurityalliance/stix-shifter/pull/823)

### Dependency update:

* Downgrade pyopenssl from 22.0.0 to 21.0.0

--------------------------------------

## 4.0.0 (2022-02-23)

### Breaking changes:

* Handling unmapped operators in stix pattern
* Optimization of results translation 

### Changes:

* Added New connector: Cybereason
* Added Stix 2.1 ids and mapping update in [#731](https://github.com/opencybersecurityalliance/stix-shifter/pull/731) [#721](https://github.com/opencybersecurityalliance/stix-shifter/pull/721)
* Added stix-shifter CLI parameters to configure max returned results and saving to a file in [#730](https://github.com/opencybersecurityalliance/stix-shifter/pull/730)
* Azure Sentinel Mapping update in [710](https://github.com/opencybersecurityalliance/stix-shifter/pull/710)
* Handling unmapped operators in stix pattern in [#744](https://github.com/opencybersecurityalliance/stix-shifter/pull/744)
* Placeholder for datadog certificate in [#782](https://github.com/opencybersecurityalliance/stix-shifter/pull/782)
* Proofpoint: Update labels in configuration in [792](https://github.com/opencybersecurityalliance/stix-shifter/pull/792)
* Added Operator list in adapter guide in [#804](https://github.com/opencybersecurityalliance/stix-shifter/pull/804)
* Splunk mapping update in [#797](https://github.com/opencybersecurityalliance/stix-shifter/pull/797)
* Keep both helper description and the link description in [818](https://github.com/opencybersecurityalliance/stix-shifter/pull/818)
* Optimization of results translation in [#718](https://github.com/opencybersecurityalliance/stix-shifter/pull/718)
* QRadar mapping update in [#751](https://github.com/opencybersecurityalliance/stix-shifter/pull/751)

### Fixes
* Datadog ssl cert fix.[#758](https://github.com/opencybersecurityalliance/stix-shifter/pull/758)
* cbcloud: fix ipv4 stix pattern translation [#761](https://github.com/opencybersecurityalliance/stix-shifter/pull/761)
* fix configuration in proofpoint and sumologic [#745](https://github.com/opencybersecurityalliance/stix-shifter/pull/745)
* Crowdstrike unittest fix [#775](https://github.com/opencybersecurityalliance/stix-shifter/pull/775)
* Fix error reponse of ms defender connector [#747](https://github.com/opencybersecurityalliance/stix-shifter/pull/747)
* fix: handling zero and non-zero values for the transformers [#774](https://github.com/opencybersecurityalliance/stix-shifter/pull/774)
* Fix Proofpoint: avoid mapping error for standard STIX Pattern translation [#786](https://github.com/opencybersecurityalliance/stix-shifter/pull/786)
* Proofpoint results connection fix [#739](https://github.com/opencybersecurityalliance/stix-shifter/pull/739)
* Fix local build and install [#779](https://github.com/opencybersecurityalliance/stix-shifter/pull/779)
* fix collections.abc warning [#793](https://github.com/opencybersecurityalliance/stix-shifter/pull/793)
* fix instances of reserved STIX 2.1 id property [#819](https://github.com/opencybersecurityalliance/stix-shifter/pull/819)
* Fix category in ecs to be list type [#734](https://github.com/opencybersecurityalliance/stix-shifter/pull/734)
* fix debug cli param [#735](https://github.com/opencybersecurityalliance/stix-shifter/pull/735)
* fix azure sentinel: Incorrect string conversion of datasource values [#771](https://github.com/opencybersecurityalliance/stix-shifter/pull/771)

### Dependency update
* Bump stix2-patterns from 1.3.0 to 1.3.2 
* Bump flatten-json from 0.1.7 to 0.1.13
* Bump flask from 1.1.2 to 2.0.3
* Bump python-dateutil from 2.8.1 to 2.8.2
* Bump jsonmerge from 1.7.0 to 1.8.0
* Bump colorlog from 4.1.0 to 6.6.0
* Bump adal from 1.2.2 to 1.2.7
* Bump pyopenssl from 20.0.1 to 22.0.0
* Bump stix2-validator from 1.1.2 to 3.0.2
* Bump boto3 from 1.17.20 to 1.21.5## 4.0.0 (2022-02-23)
