import React, { useMemo, useState } from "react";
import { Modal, ComboBox } from "@carbon/ibm-security";
import { useDispatch, useSelector } from "react-redux";
import {
  closeMoveFieldToObjectModal,
  moveDataSourceFieldToObject,
} from "../../store/actions/to_stix";
import styles from "./to_stix.module.scss";

const MoveFieldToObjectModal = () => {
  const dispatch = useDispatch();
  const stixObjects = useSelector((state) => state.toStix.stixObjects);
  const data = useSelector((state) => state.toStix.moveFieldToObjectModalData);
  const allAvailableObjectKeys = useMemo(() => {
    return stixObjects.filter((o) => o !== data?.objectKey);
  }, [data, stixObjects]);
  const isOpen = !!data;
  const [object, setObject] = useState("");
  const fieldName = data?.fieldName;

  return (
    <Modal
      shouldSubmitOnEnter={true}
      open={isOpen}
      primaryButtonText={"Move"}
      secondaryButtonText={"Cancel"}
      onRequestClose={() => {
        dispatch(closeMoveFieldToObjectModal());
        setObject("");
      }}
      onRequestSubmit={() => {
        dispatch(moveDataSourceFieldToObject(object));
        dispatch(closeMoveFieldToObjectModal());
        setObject("");
      }}
      modalHeading={`Select object to move field ${
        fieldName ? `${fieldName}` : ""
      } to`}
      className={styles.modal}
    >
      <div className={styles.modal} id={`div_${data?.objectKey}`}>
        <ComboBox
          className={styles.combo_box}
          id={`comboBox_${data?.objectKey}`}
          light
          placeholder={"Search object..."}
          items={allAvailableObjectKeys}
          itemToString={(item) => (item ? item : "")}
          selectedItem={object}
          onChange={(e) => {
            setObject(e.selectedItem);
          }}
        />
      </div>
    </Modal>
  );
};

export default MoveFieldToObjectModal;
