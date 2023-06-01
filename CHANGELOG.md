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

## 5.3.0 (2023-05-15)

### Breaking changes:

### Deprecations:

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

### Deprecations:

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

### Breaking changes:

### Deprecations:

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

### Breaking changes:

### Deprecations:

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

### Breaking changes:

### Deprecations:

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

### Breaking changes:

### Deprecations:

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

### Breaking changes:

### Deprecations:

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

### Dependency update:


--------------------------------------


## 4.2.0 (2022-06-29)
### Breaking changes:

### Deprecations:

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
### Breaking changes:

### Deprecations:

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
### Breaking changes:
### Deprecations:
### Changes:
* CrowdStrike connector mapping update [#823](https://github.com/opencybersecurityalliance/stix-shifter/pull/823)

### Fixes:
### Dependency update:
* Downgrade pyopenssl from 22.0.0 to 21.0.0

--------------------------------------

## 4.0.0 (2022-02-23)
### Breaking changes:

* Handling unmapped operators in stix pattern
* Optimization of results translation 

### Deprecations:

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
