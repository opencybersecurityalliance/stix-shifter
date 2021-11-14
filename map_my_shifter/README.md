![logo](https://user-images.githubusercontent.com/16198896/129204519-78bb6448-246e-4e6d-a456-182792c7b894.png)

# `map-my-shifter`

> STIX-Shifter Connector's Mapping Builder

The map-my-shifter (MMS) project provides a visual way for building mapping files for [STIX-Shifter](https://github.com/opencybersecurityalliance/stix-shifter) project.
A typical connector requires two types of fields mapping:

- From STIX pattern mapping - When building the data source query from STIX query, the STIX fields, for examples `file:name`, is mapped to the target data source's field. [Read more...](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-translation-module.md#step-2-edit-the-from_stix_map-json-files)
- To STIX object mapping - When results object is back from the data source, this object should be displayed in the final results as STIX object. For examples `{"filename": "xxxxx"}` should be translated to STIX object of type `file`. [Read more...](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-translation-module.md#step-4-edit-the-to_stix_map-json-file)

### Use-cases

- Create mapping file from scratch.
- Load existing mapping file, edit the file and save it to a new file.

### Development

MMS is a static client side app, there is no backend involved, except from serving the static content. It is built with [ReactJS](https://reactjs.org) library, and designed using [Carbon Design System](https://www.carbondesignsystem.com) components.

### Installation

- run `npm install map-my-shifter`
- import moduls: `import {FromStix, ToStix} from 'map-my-shifter';`

### Usage

1. map-my-shifter component: react component that shows the STIX mapping
   - `<FromStix.Mapping/>`
   - `<ToStix.Mapping/>`
   - you can add property `StixVersion` with the value `V_2_0` or `V_2_1`, defult is V_2_0.
   - for example: `<FromStix.Mapping StixVersion='V_2_1'/>`

##

2. map-my-shifter import function: gets a javaScript object and adds the content to the mapping
   - `FromStix.Import(JSON.parse({"ipv4-addr": {"fields": {"value": ["sourceip"]}}}))`
   - `ToStix.Import(JSON.parse({"ipv4-addr": {"fields": {"value": ["sourceip"]}}}))`

##

3. map-my-shifter export function: gets a string and opens a window to save the mapping to a file.
   - `FromStix.Export('fileName')`
   - `ToStix.Export('fileName')`

### Authors

- [Bar Haim](https://github.com/barvhaim)
- [Ido Hersko](https://github.com/idohersko)
- [Noaa Kless](https://github.com/noaakl)

### Licensing

map-my-shifter is licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/barvhaim/map-my-shifter/blob/master/LICENSE) for the full license text.

Built with ❤️ from
[IBM Cyber Security Center of Excellence (CCoE)](https://www.research.ibm.com/haifa/ccoe/)
