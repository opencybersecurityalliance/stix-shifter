import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { Search } from "@carbon/ibm-security";
import { updateSearchFieldValue } from "../../store/actions/stix";

const FieldSearchBar = () => {
  const dispatch = useDispatch();
  const fieldSearch = useSelector((state) => state.fromStix.fieldSearch);
  return (
    <Search
      light={true}
      labelText={"search"}
      size={"sm"}
      value={fieldSearch}
      onChange={(event) => {
        dispatch(updateSearchFieldValue(event.target.value));
      }}
      placeholder={"Search field…"}
    />
  );
};

export default React.memo(FieldSearchBar);
