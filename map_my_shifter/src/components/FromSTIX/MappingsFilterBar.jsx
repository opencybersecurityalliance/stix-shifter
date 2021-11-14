import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { TextInput } from "@carbon/ibm-security";
import { updateMappingsFilterFieldValue } from "../../store/actions/from_stix";

const MappingsFilterBar = () => {
  const dispatch = useDispatch();
  const fieldMappingFilter = useSelector(
    (state) => state.fromStix.fieldMappingFilter
  );
  return (
    <TextInput
      light={true}
      value={fieldMappingFilter}
      onChange={(event) => {
        dispatch(updateMappingsFilterFieldValue(event.target.value));
      }}
      labelText=""
      id={"mappings-filter-input"}
      placeholder={"Filter field…"}
      autoComplete={"off"}
    />
  );
};

export default React.memo(MappingsFilterBar);
