import React from "react";
import styles from "./to_stix.module.scss";
import {
  openSelectFieldModal,
  removeStixField,
  removeMetadataField,
  updateStixField,
  updateMetadataField,
} from "../../store/actions/to_stix";
import { ComboBox, TextInput } from "@carbon/ibm-security";
import { useDispatch } from "react-redux";
import transformers from "../../global/transformers";
import { Delete20, List20 } from "@carbon/icons-react";
import ReferencesSelector from "./ReferencesSelector";

const MappedField = ({
  isStix,
  objectKey,
  sourceFieldId,
  mappedFieldId,
  mappedFieldKey,
  mappedFieldTransformer,
  mappedFieldReferences,
}) => {
  const dispatch = useDispatch();
  return (
    <div key={mappedFieldId}>
      <div className={`bx--row ${styles.object_item__field}`}>
        <div className={"bx--col-md-3"}>
          <div className={"bx--row"}>
            <div className={"bx--col"}>
              <TextInput
                id={`${mappedFieldId}`}
                labelText={""}
                onChange={(e) => {
                  isStix
                    ? dispatch(
                        updateStixField(
                          e.target.value,
                          "key",
                          objectKey,
                          sourceFieldId,
                          mappedFieldId
                        )
                      )
                    : dispatch(
                        updateMetadataField(
                          e.target.value,
                          "key",
                          objectKey,
                          mappedFieldId
                        )
                      );
                }}
                size={"sm"}
                value={mappedFieldKey}
              />
            </div>
            {isStix && (
              <div>
                <List20
                  style={{ border: 0 }}
                  className={`${styles.object_item__btn}`}
                  onClick={() => {
                    dispatch(
                      openSelectFieldModal(
                        objectKey,
                        sourceFieldId,
                        mappedFieldId
                      )
                    );
                  }}
                />
              </div>
            )}
          </div>
        </div>
        <div className={"bx--col-md-2"}>
          <ComboBox
            id={`ComboBox_${mappedFieldId}`}
            size={"sm"}
            placeholder={"Search Transformer"}
            ariaLabel="transformers_combobox"
            items={transformers}
            selectedItem={
              mappedFieldTransformer ? mappedFieldTransformer : null
            }
            onChange={(e) => {
              isStix
                ? dispatch(
                    updateStixField(
                      e.selectedItem,
                      "transformer",
                      objectKey,
                      sourceFieldId,
                      mappedFieldId
                    )
                  )
                : dispatch(
                    updateMetadataField(
                      e.selectedItem,
                      "transformer",
                      objectKey,
                      mappedFieldId
                    )
                  );
            }}
          />
        </div>

        {isStix && (
          <ReferencesSelector
            objectKey={objectKey}
            sourceFieldId={sourceFieldId}
            mappedFieldId={mappedFieldId}
            selectedReferences={mappedFieldReferences}
          />
        )}

        <div>
          <Delete20
            className={`${styles.object_item__btn}`}
            onClick={() => {
              isStix
                ? dispatch(
                    removeStixField(objectKey, sourceFieldId, mappedFieldId)
                  )
                : dispatch(removeMetadataField(objectKey, mappedFieldId));
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default React.memo(MappedField);
