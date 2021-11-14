import React from "react";
import { Button } from "@carbon/ibm-security";
import styles from "./export.module.scss";

const Export = ({
  saveJsonToDisk,
  stateMappingToShifterMapping,
  stixMapping,
  metadataMapping,
}) => {
  return (
    <Button
      kind="tertiary"
      size="sm"
      onClick={() => {
        saveJsonToDisk(
          "",
          stateMappingToShifterMapping(stixMapping, metadataMapping)
        );
      }}
      className={styles.export__btn}
    >
      Export
    </Button>
  );
};

export default React.memo(Export);
