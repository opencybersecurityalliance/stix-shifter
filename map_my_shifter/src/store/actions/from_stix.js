export const ADD_FIELD = "ADD_FIELD";
export const DELETE_FIELD = "DELETE_FIELD";
export const ADD_VALUE = "ADD_VALUE";
export const UPDATE_VALUE = "UPDATE_VALUE";
export const DELETE_VALUE = "DELETE_VALUE";
export const UPDATE_SEARCH_FIELD_VALUE = "UPDATE_SEARCH_FIELD_VALUE";
export const UPDATE_FROM_STIX_MAPPINGS_FROM_FILE =
  "UPDATE_FROM_STIX_MAPPINGS_FROM_FILE";
export const UPDATE_MAPPINGS_FILTER_FIELD_VALUE =
  "UPDATE_MAPPINGS_FILTER_FIELD_VALUE";
export const CLEAR_FROM_STIX_MAPPINGS = "CLEAR_FROM_STIX_MAPPINGS";
export const SHOW_CUSTOM_FIELD_MODAL = "SHOW_CUSTOM_FIELD_MODAL";
export const CLOSE_CUSTOM_FIELD_MODAL = "CLOSE_CUSTOM_FIELD_MODAL";

export function addField(field, required = false) {
  return {
    type: ADD_FIELD,
    payload: {
      field,
      required,
    },
  };
}

export function deleteField(field) {
  return {
    type: DELETE_FIELD,
    payload: {
      field,
    },
  };
}

export function addValue(field) {
  return {
    type: ADD_VALUE,
    payload: {
      field,
    },
  };
}

export function deleteValue(field, id) {
  return {
    type: DELETE_VALUE,
    payload: {
      field,
      id,
    },
  };
}

export function updateValue(field, id, value) {
  return {
    type: UPDATE_VALUE,
    payload: {
      field,
      id,
      value,
    },
  };
}

export function updateMappingsFilterFieldValue(value) {
  return {
    type: UPDATE_MAPPINGS_FILTER_FIELD_VALUE,
    payload: {
      value,
    },
  };
}

export function updateMappingsFromFile(stixMapping) {
  return {
    type: UPDATE_FROM_STIX_MAPPINGS_FROM_FILE,
    payload: {
      stixMapping,
    },
  };
}

export function clearMappings() {
  return {
    type: CLEAR_FROM_STIX_MAPPINGS,
  };
}

export function showCustomFieldModal() {
  return {
    type: SHOW_CUSTOM_FIELD_MODAL,
  };
}

export function closeCustomFieldModal() {
  return {
    type: CLOSE_CUSTOM_FIELD_MODAL,
  };
}
