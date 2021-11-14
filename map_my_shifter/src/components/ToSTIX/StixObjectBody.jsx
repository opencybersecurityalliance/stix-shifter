import React from "react";
import SourceField from "./SourceField";

const StixObjectBody = ({ sourceFields, objectKey }) => {
  const isEmptyObject = Object.keys(sourceFields).length === 0;

  if (isEmptyObject) {
    return (
      <div className={`bx--row`}>
        <div className={`bx--col`}>
          There are currently no data-source fields mapped. Click the "+" button
          to add your first data-source field.
        </div>
      </div>
    );
  }

  return Object.keys(sourceFields).map((fieldId) => {
    return (
      <SourceField
        isStix={true}
        key={fieldId}
        objectKey={objectKey}
        fieldId={fieldId}
        fieldData={sourceFields[fieldId]}
      />
    );
  });
};

export default React.memo(StixObjectBody);
