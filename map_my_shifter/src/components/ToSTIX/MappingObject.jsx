import React, { useState } from "react";
import { TextInput, Button } from "@carbon/ibm-security";
import {
  Add20,
  Close20,
  Close16,
  ChevronUp32,
  ChevronDown32,
  Checkmark16,
  Edit16,
} from "@carbon/icons-react";
import {
  addDataSourceField,
  removeStixObject,
  removeMetadataObject,
  updateObjectName,
} from "../../store/actions/to_stix";
import { isValidObjectName } from "./utils";
import { useDispatch, useSelector } from "react-redux";
import StixObjectBody from "./StixObjectBody";
import MetadataObjectBody from "./MetadataObjectBody";
import styles from "./to_stix.module.scss";

const ObjectHeader = ({ name, isOpen, setIsOpen, isStix }) => {
  const dispatch = useDispatch();
  const mappingObjects = isStix ? "stixObjects" : "metadataObjects";
  const objects = useSelector((state) => state.toStix[mappingObjects]);
  const [newName, setName] = useState(name);
  const [isEditingObjectName, setEditObjectName] = useState(false);
  const objectNameChangeHandler = () => {
    if (isValidObjectName(name, newName, objects)) {
      dispatch(updateObjectName(name, newName, isStix));
      setEditObjectName(false);
    }
  };

  return (
    <div className={`bx--row`}>
      <span style={{ marginLeft: "1rem", cursor: "pointer" }}>
        {isOpen ? (
          <ChevronDown32
            onClick={() => {
              setIsOpen(!isOpen);
            }}
          />
        ) : (
          <ChevronUp32
            onClick={() => {
              setIsOpen(!isOpen);
            }}
          />
        )}
      </span>
      {isEditingObjectName ? (
        <div className={`bx--row ${styles.object_item__edit_title}`}>
          <TextInput
            className={`bx--col ${styles.object_item__title}`}
            id={`${isStix}__${name}`}
            labelText={""}
            autoComplete={"off"}
            value={newName}
            invalid={!isValidObjectName(name, newName, objects)}
            invalidText={
              !newName
                ? "Object name must contain atleast one character."
                : "Object name already exists."
            }
            onChange={(input) => {
              setName(input.target.value);
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                objectNameChangeHandler();
              }
            }}
          />
          <Button
            className={`bx--col`}
            kind="ghost"
            size="sm"
            style={{ paddingTop: 1 }}
            renderIcon={Checkmark16}
            iconDescription="Submit new object name"
            hasIconOnly
            disabled={!isValidObjectName(name, newName, objects)}
            onClick={() => {
              objectNameChangeHandler();
            }}
          />
          <Button
            className={`bx--col`}
            kind="ghost"
            size="sm"
            style={{ paddingTop: 1 }}
            renderIcon={Close16}
            iconDescription="Cancel"
            hasIconOnly
            onClick={() => {
              setName(name);
              setEditObjectName(false);
            }}
          />
        </div>
      ) : (
        <div className={`bx--col ${styles.object_item__title}`}>
          {name}
          <Button
            kind="ghost"
            style={{ paddingTop: 1 }}
            renderIcon={Edit16}
            iconDescription="Edit object name"
            hasIconOnly
            onClick={() => {
              setEditObjectName(true);
            }}
          />
        </div>
      )}

      <div className={`bx--col`} style={{ textAlign: "right" }}>
        {isStix && (
          <Add20
            className={`${styles.object_item__btn}`}
            style={{
              marginRight: ".5rem",
            }}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              dispatch(addDataSourceField(name));
            }}
          />
        )}
        <Close20
          className={`${styles.object_item__btn}`}
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            isStix
              ? dispatch(removeStixObject(name))
              : dispatch(removeMetadataObject(name));
          }}
        />
      </div>
    </div>
  );
};

const MappingObject = ({ objectKey, objectData, isStix }) => {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <div className={`bx--row ${styles.object__item_box}`}>
      <div className={`bx--col ${styles.object__item_content}`}>
        <ObjectHeader
          name={objectKey}
          isOpen={isOpen}
          setIsOpen={setIsOpen}
          isStix={isStix}
        />
        {isOpen &&
          (isStix ? (
            <StixObjectBody objectKey={objectKey} sourceFields={objectData} />
          ) : (
            <MetadataObjectBody
              objectKey={objectKey}
              sourceFields={objectData}
            />
          ))}
      </div>
    </div>
  );
};

export default React.memo(MappingObject);
