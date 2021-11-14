import React from "react";
import CustomField from "./CustomField";
import AddFields from "../STIX/AddFields";
import styles from "./from_stix.module.scss";

const SelectFields = ({ officialFields }) => {
  return (
    <>
      <div className="bx--row">
        <div className="bx--col">
          <h4 className={`${styles.section_title}`}>Select Fields</h4>
        </div>
        <div className="bx--col" style={{ textAlign: "right" }}>
          <CustomField />
        </div>
      </div>

      <AddFields officialFields={officialFields} />
    </>
  );
};

export default React.memo(SelectFields);
