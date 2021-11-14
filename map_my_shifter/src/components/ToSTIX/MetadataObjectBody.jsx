import React from "react";
import MappedFieldsTable from "./MappedFieldsTable";
import styles from "./to_stix.module.scss";

const MetadataObjectBody = ({ sourceFields, objectKey }) => {
  return (
    <div className={`bx--row ${styles.object_item__field}`}>
      <div className={"bx--col-sm-4"}>
        <MappedFieldsTable
          isStix={false}
          objectKey={objectKey}
          sourceFieldId={sourceFields}
          sourceFieldData={sourceFields}
        />
      </div>
    </div>
  );
};

export default React.memo(MetadataObjectBody);
