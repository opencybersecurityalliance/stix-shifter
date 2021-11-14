export const OPEN_NEW_OBJECT_MODAL = "OPEN_NEW_OBJECT_MODAL";
export const CLOSE_NEW_OBJECT_MODAL = "CLOSE_NEW_OBJECT_MODAL";
export const ADD_NEW_STIX_OBJECT = "ADD_NEW_STIX_OBJECT";
export const ADD_NEW_METADATA_OBJECT = "ADD_NEW_METADATA_OBJECT";
export const UPDATE_OBJECT_NAME = "UPDATE_OBJECT_NAME";
export const REMOVE_STIX_OBJECT = "REMOVE_STIX_OBJECT";
export const REMOVE_METADATA_OBJECT = "REMOVE_METADATA_OBJECT";
export const ADD_DATASOURCE_FIELD = "ADD_DATASOURCE_FIELD";
export const REMOVE_DATASOURCE_FIELD = "REMOVE_DATASOURCE_FIELD";
export const MOVE_DATASOURCE_FIELD_TO_OBJECT =
  "MOVE_DATASOURCE_FIELD_TO_OBJECT";
export const UPDATE_DATASOURCE_FIELD = "UPDATE_DATASOURCE_FIELD";
export const REMOVE_STIX_FIELD = "REMOVE_STIX_FIELD";
export const ADD_STIX_FIELD = "ADD_STIX_FIELD";
export const UPDATE_STIX_FIELD = "UPDATE_STIX_FIELD";
export const ADD_METADATA_FIELD = "ADD_METADATA_FIELD";
export const REMOVE_METADATA_FIELD = "REMOVE_METADATA_FIELD";
export const UPDATE_METADATA_FIELD = "UPDATE_METADATA_FIELD";
export const CLEAR_TO_STIX_MAPPINGS = "CLEAR_TO_STIX_MAPPINGS";
export const UPDATE_TO_STIX_MAPPINGS_FROM_FILE =
  "UPDATE_TO_STIX_MAPPINGS_FROM_FILE";
export const OPEN_SELECT_FIELD_MODAL = "OPEN_SELECT_FIELD_MODAL";
export const CLOSE_SELECT_FIELD_MODAL = "CLOSE_SELECT_FIELD_MODAL";
export const OPEN_MOVE_FIELD_TO_OBJECT_MODAL =
  "OPEN_MOVE_FIELD_TO_OBJECT_MODAL";
export const CLOSE_MOVE_FIELD_TO_OBJECT_MODAL =
  "CLOSE_MOVE_FIELD_TO_OBJECT_MODAL";

export function openNewObjectModal() {
  return {
    type: OPEN_NEW_OBJECT_MODAL,
  };
}

export function closeNewObjectModal() {
  return {
    type: CLOSE_NEW_OBJECT_MODAL,
  };
}

export function openSelectFieldModal(objectKey, sourceFieldId, stixFieldId) {
  return {
    type: OPEN_SELECT_FIELD_MODAL,
    payload: {
      objectKey,
      sourceFieldId,
      stixFieldId,
    },
  };
}

export function closeSelectFieldModal() {
  return {
    type: CLOSE_SELECT_FIELD_MODAL,
  };
}

export function openMoveFieldToObjectModal(objectKey, fieldId, fieldName) {
  return {
    type: OPEN_MOVE_FIELD_TO_OBJECT_MODAL,
    payload: {
      objectKey,
      fieldId,
      fieldName,
    },
  };
}

export function closeMoveFieldToObjectModal() {
  return {
    type: CLOSE_MOVE_FIELD_TO_OBJECT_MODAL,
  };
}

export function addNewStixObject(name) {
  return {
    type: ADD_NEW_STIX_OBJECT,
    payload: {
      name,
    },
  };
}

export function addNewMetadataObject(name) {
  return {
    type: ADD_NEW_METADATA_OBJECT,
    payload: {
      name,
    },
  };
}

export function removeStixObject(name) {
  return {
    type: REMOVE_STIX_OBJECT,
    payload: {
      name,
    },
  };
}

export function removeMetadataObject(name) {
  return {
    type: REMOVE_METADATA_OBJECT,
    payload: {
      name,
    },
  };
}

export function updateObjectName(oldName, newName, isStix) {
  return {
    type: UPDATE_OBJECT_NAME,
    payload: {
      oldName,
      newName,
      isStix,
    },
  };
}

export function addDataSourceField(objectName) {
  return {
    type: ADD_DATASOURCE_FIELD,
    payload: {
      objectName,
    },
  };
}

export function updateDataSourceField(objectName, fieldId, fieldName) {
  return {
    type: UPDATE_DATASOURCE_FIELD,
    payload: {
      objectName,
      fieldId,
      fieldName,
    },
  };
}

export function removeDataSourceField(objectName, fieldId) {
  return {
    type: REMOVE_DATASOURCE_FIELD,
    payload: {
      objectName,
      fieldId,
    },
  };
}

export function moveDataSourceFieldToObject(objectToMoveTo) {
  return {
    type: MOVE_DATASOURCE_FIELD_TO_OBJECT,
    payload: {
      objectToMoveTo,
    },
  };
}

export function addStixField(objectName, fieldId, key) {
  return {
    type: ADD_STIX_FIELD,
    payload: {
      objectName,
      fieldId,
      key,
    },
  };
}

export function updateStixField(value, type, objectName, fieldId, mappingId) {
  return {
    type: UPDATE_STIX_FIELD,
    payload: {
      value,
      type,
      objectName,
      fieldId,
      mappingId,
    },
  };
}

export function removeStixField(objectName, fieldId, mappingId) {
  return {
    type: REMOVE_STIX_FIELD,
    payload: {
      objectName,
      fieldId,
      mappingId,
    },
  };
}

export function addMetadataField(objectName) {
  return {
    type: ADD_METADATA_FIELD,
    payload: {
      objectName,
    },
  };
}

export function removeMetadataField(objectName, mappingId) {
  return {
    type: REMOVE_METADATA_FIELD,
    payload: {
      objectName,
      mappingId,
    },
  };
}

export function updateMetadataField(value, type, objectName, mappingId) {
  return {
    type: UPDATE_METADATA_FIELD,
    payload: {
      value,
      type,
      objectName,
      mappingId,
    },
  };
}

export function clearMappings() {
  return {
    type: CLEAR_TO_STIX_MAPPINGS,
  };
}

export function updateMappingsFromFile(stixMapping, metadataMapping) {
  return {
    type: UPDATE_TO_STIX_MAPPINGS_FROM_FILE,
    payload: {
      stixMapping,
      metadataMapping,
    },
  };
}
