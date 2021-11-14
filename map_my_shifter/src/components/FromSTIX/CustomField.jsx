import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { showCustomFieldModal } from "../../store/actions/from_stix";
import CustomFieldModal from "./CustomFieldModal";
import { Button } from "@carbon/ibm-security";
import { Add16 } from "@carbon/icons-react";

const CustomField = () => {
  const dispatch = useDispatch();
  const customFieldModalShow = useSelector(
    (state) => state.fromStix.customFieldModalShow
  );

  return (
    <div>
      <Button
        renderIcon={Add16}
        kind="ghost"
        size="sm"
        onClick={() => {
          dispatch(showCustomFieldModal());
        }}
      >
        Custom Field
      </Button>
      {customFieldModalShow && <CustomFieldModal />}
    </div>
  );
};

export default React.memo(CustomField);
