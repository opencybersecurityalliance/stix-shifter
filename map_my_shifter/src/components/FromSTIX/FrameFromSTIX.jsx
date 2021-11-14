import React from "react";
import { useSelector } from "react-redux";
import { saveJsonToDisk } from "../STIX/utils";
import FromSTIX from ".";
import Import from "../Import/Import";
import Export from "../Export/Export";
import { stateMappingToShifterMapping, loadJsonFromDisk } from "./utils";
import {
  updateMappingsFromFile,
  clearMappings,
} from "../../store/actions/from_stix";
const FrameFromSTIX = () => {
  const stixMapping = useSelector((state) => state.fromStix.stixMapping);
  const metadataMapping = useSelector(
    (state) => state.fromStix.metadataMapping
  );

  return (
    <div className="bx--grid">
      <div className="bx--row">
        <div className="bx--col">
          <h1 className="page-title">{"From STIX"}</h1>
        </div>
        <div className="bx--col">
          <div className="bx--row" style={{ float: "right" }}>
            <div>
              <Import
                clearMappings={clearMappings}
                loadJsonFromDisk={loadJsonFromDisk}
                updateMappingsFromFile={updateMappingsFromFile}
              />
            </div>
            <div>
              <Export
                saveJsonToDisk={saveJsonToDisk}
                stateMappingToShifterMapping={stateMappingToShifterMapping}
                stixMapping={stixMapping}
                metadataMapping={metadataMapping}
              />
            </div>
          </div>
        </div>
      </div>
      <FromSTIX />
    </div>
  );
};

export default FrameFromSTIX;
