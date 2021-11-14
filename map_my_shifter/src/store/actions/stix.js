export const UPDATE_SEARCH_FIELD_VALUE = "UPDATE_SEARCH_FIELD_VALUE";
export const CHANGE_STIX_VERSION = "CHANGE_STIX_VERSION";

export function updateSearchFieldValue(value) {
  return {
    type: UPDATE_SEARCH_FIELD_VALUE,
    payload: {
      value,
    },
  };
}

export function changeStixVersion(stixVersion) {
  return {
    type: CHANGE_STIX_VERSION,
    payload: {
      version: stixVersion,
    },
  };
}
