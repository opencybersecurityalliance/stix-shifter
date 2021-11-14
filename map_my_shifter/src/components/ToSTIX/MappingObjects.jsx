import React from "react";
import { useSelector } from "react-redux";
import MappingObject from "./MappingObject";
import Minimap from "./Minimap";
import styles from "./to_stix.module.scss";
import { MAPPING_TYPE } from "../../global/constants";

const MappingObjects = ({ type }) => {
  const isStix = type === MAPPING_TYPE.OBJECT;
  const mappingObjects = isStix ? "stixMapping" : "metadataMapping";
  const mapping = useSelector((state) => state.toStix[mappingObjects]);
  const isMappingEmpty = Object.keys(mapping).length === 0;

  if (isMappingEmpty) {
    return (
      <div className="bx--row">
        <div className={`bx--col`}>
          <p style={{ paddingTop: "1rem" }}>
            There are currently no {type}s to show. Click the “New {type}”
            button to start mapping or load configuration.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`bx--row ${styles.MappingObjects}`}>
      <Minimap isStix={isStix} />
      <div className="bx--col-sm-3">
        {Object.keys(mapping).map((o) => {
          return (
            <div id={`${o}`} key={`${o}`}>
              <MappingObject
                key={`${o}`}
                objectKey={o}
                objectData={mapping[o]}
                isStix={isStix}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MappingObjects;
