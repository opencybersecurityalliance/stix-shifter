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

-------------------------------------

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
