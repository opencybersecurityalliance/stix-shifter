import React from "react";
import {
  Accordion,
  AccordionItem,
  UnorderedList,
  ListItem,
} from "@carbon/ibm-security";
import "./About.scss";

const About = () => {
  return (
    <>
      <div className={"bx--row"}>
        <div className={"bx--col"}>
          <img
            src="https://user-images.githubusercontent.com/16198896/129204519-78bb6448-246e-4e6d-a456-182792c7b894.png"
            alt="logo"
          />
          <h4>STIX-Shifter Connector's Mapping Builder</h4>
        </div>
      </div>

      <div className={"bx--row"}>
        <div className={"bx--col"}>
          <Accordion align="start">
            <AccordionItem title="Introduction" open>
              <p>
                The map-my-shifter (MMS) project provides a visual way for
                building mapping files for{" "}
                <a
                  href={
                    "https://github.com/opencybersecurityalliance/stix-shifter"
                  }
                >
                  STIX-Shifter
                </a>{" "}
                project.
              </p>

              <UnorderedList>
                <ListItem>
                  From STIX pattern mapping - When building the data source
                  query from STIX query, the STIX fields, for examples
                  `file:name`, is mapped to the target data source's field.
                  <a
                    href={
                      "https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-translation-module.md#step-2-edit-the-from_stix_map-json-files"
                    }
                  >
                    Read more...
                  </a>
                </ListItem>
                <ListItem>
                  To STIX object mapping - When results object is back from the
                  data source, this object should be displayed in the final
                  results as STIX object. For examples {"{"}"filename": "xxxxx"
                  {"}"}
                  should be translated to STIX object of type `file`.
                  <a
                    href={
                      "https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-translation-module.md#step-4-edit-the-to_stix_map-json-file"
                    }
                  >
                    Read more...
                  </a>
                </ListItem>
              </UnorderedList>
            </AccordionItem>

            <AccordionItem title="Use-cases" open>
              <UnorderedList>
                <ListItem>Create mapping file from scratch.</ListItem>
                <ListItem>
                  Load existing mapping file, edit the file and save it to a new
                  file
                </ListItem>
              </UnorderedList>
            </AccordionItem>

            <AccordionItem title="Authors" open>
              <UnorderedList>
                <ListItem>
                  <a href={"https://github.com/barvhaim"}>Bar Haim</a>
                </ListItem>
                <ListItem>
                  <a href={"https://github.com/idohersko"}>Ido Hersko</a>
                </ListItem>
                <ListItem>
                  <a href={"https://github.com/noaakl"}>Noaa Kless</a>
                </ListItem>
              </UnorderedList>
            </AccordionItem>

            <AccordionItem title="Licensing" open>
              <p>
                map-my-shifter is licensed under the Apache License, Version
                2.0. See{" "}
                <a
                  href={
                    "https://github.com/barvhaim/map-my-shifter/blob/master/LICENSE"
                  }
                >
                  LICENSE
                </a>{" "}
                for the full license text.
              </p>
            </AccordionItem>
          </Accordion>
        </div>
      </div>

      <div className={"bx--row"}>
        <div className={"bx--col footer"}>
          <p>
            Built with <span className="heart">❤</span> from{" "}
            <a href={"https://www.research.ibm.com/haifa/ccoe/"}>
              IBM Cyber Security Center of Excellence (CCoE)
            </a>
          </p>
        </div>
      </div>
    </>
  );
};

export default About;
