# Introduction to STIX-Shifter

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data by using these patterns, STIX-Shifter also _transforms the output_ into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, mostly looks and behaves the same.

::::

---

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`markdown;1.5em;sd-mr-1` Overview
:link:  OVERVIEW.md
:link-type: ref

For general information about STIX, this project, and the command line utilities, see the STIX-shifter Overview.

+++
[Learn more »](OVERVIEW.md)
:::

:::{grid-item-card} {octicon}`tools;1.5em;sd-mr-1` Developer Guide
:link: adapter-guide/develop-stix-adapter.md
:link-type: ref

Follow the developer guide to learn about developing a new STIX-Shifter connector.
+++
[Learn more »](adapter-guide/develop-stix-adapter.md)
:::

::::

---