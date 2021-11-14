import React, { useMemo, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { MultiSelect } from "@carbon/ibm-security";
import { updateStixField } from "../../store/actions/to_stix";

const ReferencesSelector = ({
  selectedReferences,
  objectKey,
  sourceFieldId,
  mappedFieldId,
}) => {
  const dispatch = useDispatch();
  const stixObjects = useSelector((state) => state.toStix.stixObjects);
  const allAvailableObjectKeys = useMemo(() => {
    return stixObjects.filter((o) => o !== objectKey);
  }, [objectKey, stixObjects]);

  useEffect(() => {
    const updatedReferences = selectedReferences.filter((ref) => {
      return allAvailableObjectKeys.includes(ref);
    });
    dispatch(
      updateStixField(
        updatedReferences,
        "references",
        objectKey,
        sourceFieldId,
        mappedFieldId
      )
    );
    // eslint-disable-next-line
  }, [allAvailableObjectKeys]);

  return (
    <div className={"bx--col-md-2"}>
      <MultiSelect.Filterable
        key={`${mappedFieldId}_${selectedReferences}`}
        id={`MultiSelect.Filterable_${mappedFieldId}`}
        size={"sm"}
        downshiftProps={{ setItemCount: selectedReferences.length }}
        placeholder={"Search References"}
        invalid={false}
        invalidText="Invalid Selection"
        items={allAvailableObjectKeys}
        useTitleInItem={true}
        disabled={allAvailableObjectKeys.length === 0}
        initialSelectedItems={selectedReferences}
        selectedItems={selectedReferences}
        itemToString={(item) => (item ? item : "")}
        onChange={(e) => {
          dispatch(
            updateStixField(
              e.selectedItems,
              "references",
              objectKey,
              sourceFieldId,
              mappedFieldId
            )
          );
        }}
      />
    </div>
  );
};

export default ReferencesSelector;
