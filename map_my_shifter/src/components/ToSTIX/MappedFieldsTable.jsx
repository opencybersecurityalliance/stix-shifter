import React from "react";
import { Add20 } from "@carbon/icons-react";
import { addStixField, addMetadataField } from "../../store/actions/to_stix";
import { useDispatch } from "react-redux";
import MappedField from "./MappedField";
import styles from "./to_stix.module.scss";

const MappedFieldsTableHeader = ({ objectKey, sourceFieldId, isStix }) => {
  const dispatch = useDispatch();
  return (
    <div className={`bx--row ${styles.object_item_field__header}`}>
      <div className={"bx--col-md-3"}>{isStix ? "STIX field" : "Key"}</div>
      <div className={"bx--col-md-2"}>Transformer</div>
      <div className={"bx--col-md-2"}>{isStix ? "References" : ""}</div>
      <div className={"bx--col-md-1"} style={{ textAlign: "right" }}>
        <Add20
          className={`${styles.object_item__btn}`}
          onClick={() => {
            isStix
              ? dispatch(addStixField(objectKey, sourceFieldId, ""))
              : dispatch(addMetadataField(objectKey, ""));
          }}
        />
      </div>
    </div>
  );
};

const MappedFieldsTableBody = ({
  objectKey,
  sourceFieldId,
  fieldsData,
  isStix,
}) => {
  return fieldsData.map((mappedField) => {
    const mappedFieldTransformer = mappedField?.transformer;
    const mappedFieldReferences =
      mappedField.references && mappedField.references.length !== 0
        ? mappedField.references
        : [];
    return (
      <MappedField
        isStix={isStix}
        key={`${objectKey}_${mappedField.id}`}
        sourceFieldId={sourceFieldId}
        objectKey={objectKey}
        mappedFieldId={mappedField.id}
        mappedFieldKey={mappedField.key}
        mappedFieldTransformer={mappedFieldTransformer}
        mappedFieldReferences={mappedFieldReferences}
      />
    );
  });
};

const MappedFieldsTable = ({
  objectKey,
  sourceFieldId,
  sourceFieldData,
  isStix,
}) => {
  return (
    <>
      <MappedFieldsTableHeader
        isStix={isStix}
        objectKey={objectKey}
        sourceFieldId={sourceFieldId}
      />
      <MappedFieldsTableBody
        key={`${objectKey}_${sourceFieldId}`}
        isStix={isStix}
        objectKey={objectKey}
        sourceFieldId={sourceFieldId}
        fieldsData={isStix ? sourceFieldData.mapped_to : sourceFieldData}
      />
    </>
  );
};

export default MappedFieldsTable;
