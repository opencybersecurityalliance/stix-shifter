import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dropdown } from "@carbon/ibm-security";
import { changeStixVersion } from "../../store/actions/stix";
import { STIX_VERSION } from "../../global/constants";

const stixVersionsList = [
  {
    id: STIX_VERSION.V_2_0,
    label: "STIX version 2.0",
  },
  {
    id: STIX_VERSION.V_2_1,
    label: "STIX version 2.1",
  },
];

const ChangeVersion = () => {
  const dispatch = useDispatch();
  const stixVersion = useSelector((state) => state.stix.stixVersion);
  return (
    <div>
      <Dropdown
        ariaLabel="Dropdown"
        label="Select STIX version"
        selectedItem={stixVersionsList.find((o) => o.id === stixVersion)}
        id="version-of-stix"
        items={stixVersionsList}
        onChange={(event) => {
          dispatch(changeStixVersion(event.selectedItem.id));
        }}
      />
    </div>
  );
};

export default React.memo(ChangeVersion);
