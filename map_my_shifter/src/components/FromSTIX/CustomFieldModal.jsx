import React, { useState } from "react";
import { Modal, TextInput } from "@carbon/ibm-security";
import { useDispatch, useSelector } from "react-redux";
import { closeCustomFieldModal, addField } from "../../store/actions/from_stix";
import { isValidCustomStixField } from "../../global/stixHelper";

const CustomFieldModal = () => {
  const customFieldModalShow = useSelector(
    (state) => state.fromStix.customFieldModalShow
  );
  const dispatch = useDispatch();
  const [customField, setCustomField] = useState("");

  return (
    <Modal
      open={customFieldModalShow}
      size="xs"
      modalHeading={"Add custom field"}
      primaryButtonText={"Add"}
      secondaryButtonText={"Cancel"}
      onRequestClose={() => {
        setCustomField("");
        dispatch(closeCustomFieldModal());
      }}
      onRequestSubmit={() => {
        const [type, key] = customField.split(":");
        dispatch(addField(`${type}:${key}`));
        setCustomField("");
        dispatch(closeCustomFieldModal());
      }}
      primaryButtonDisabled={!isValidCustomStixField(customField)}
      shouldSubmitOnEnter={true}
      hasForm={true}
    >
      <TextInput
        id="customField"
        type="text"
        labelText={`e.g "x-oca-event:category_id"`}
        onChange={(e) => {
          setCustomField(e.target.value);
        }}
        invalid={customField !== "" && !isValidCustomStixField(customField)}
        invalidText="A valid value is required"
      />
    </Modal>
  );
};

export default CustomFieldModal;
