import React from "react";
import { FileUploader } from "@carbon/ibm-security";
import { useDispatch } from "react-redux";

const Import = ({
  clearMappings,
  loadJsonFromDisk,
  updateMappingsFromFile,
}) => {
  const dispatch = useDispatch();

  return (
    <FileUploader
      accept={[".json"]}
      buttonKind="tertiary"
      buttonLabel="Import"
      filenameStatus="edit"
      multiple={false}
      size="sm"
      onDelete={() => {
        dispatch(clearMappings());
      }}
      onChange={(event) => {
        let reader = new FileReader();
        reader.onload = (_event) => {
          let input = null;
          if (_event && "target" in _event && "result" in _event.target) {
            input = JSON.parse(_event.target.result);
            const [stix, metadata] = loadJsonFromDisk(input);
            dispatch(updateMappingsFromFile(stix, metadata));
          }
        };
        reader.readAsText(event.target.files[0]);
      }}
    />
  );
};

export default React.memo(Import);
