# STIX-Shifter

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

[STIX-Shifter github repo](https://github.com/opencybersecurityalliance/stix-shifter) is the official portal of everything STIX-Shifter beyond this documentation: source, connectors, tutorial, community entrances, and more.

::::

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`markdown;1.5em;sd-mr-1` Overview
For general information about STIX, this project, and the command line utilities, see the [STIX-shifter Overview](OVERVIEW.md).
:::

:::{grid-item-card} {octicon}`plug;1.5em;sd-mr-1` Available Connectors
There are more than 30 connectors. For the list of connectors, see the [Available Connectors](CONNECTORS.md).
:::

:::{grid-item-card} {octicon}`tools;1.5em;sd-mr-1` Developer Guide
Follow the developer guide to learn about developing a new STIX-Shifter connector, see [Connector Developer Guide](adapter-guide/develop-stix-adapter.md).
:::

::::

```{toctree}
:maxdepth: 2
README.md
```

```{toctree}
:hidden:
:caption: ✏️ Project Overview

OVERVIEW.md
```

```{toctree}
:hidden:
:caption: ✏️ Available Connectors

CONNECTORS.md
```

```{toctree}
:hidden:
:caption: ✏️ Developer Guide

adapter-guide/develop-stix-adapter.md
adapter-guide/develop-translation-module.md
adapter-guide/custom_mappings.md
adapter-guide/develop-mapping-keywords.md
adapter-guide/custom_mappings.md
adapter-guide/develop-transmission-module.md
adapter-guide/develop-configuration-json.md
adapter-guide/best_practices.md
```