import { v4 as uuidv4 } from "uuid";
import {
  ADD_FIELD,
  ADD_VALUE,
  DELETE_FIELD,
  DELETE_VALUE,
  UPDATE_VALUE,
  UPDATE_MAPPINGS_FILTER_FIELD_VALUE,
  CLEAR_FROM_STIX_MAPPINGS,
  SHOW_CUSTOM_FIELD_MODAL,
  CLOSE_CUSTOM_FIELD_MODAL,
  UPDATE_FROM_STIX_MAPPINGS_FROM_FILE,
} from "../actions/from_stix";

const INITIAL_STATE = {
  stixMapping: {},
  fieldMappingFilter: "",
  customFieldModalShow: false,
};

const FromSTIXReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case ADD_FIELD: {
      const field = action.payload.field;
      if (!(field in state.stixMapping)) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [field]: {
              values: [],
            },
          },
        };
      }
      return state;
    }

    case DELETE_FIELD: {
      if (action.payload.field in state.stixMapping) {
        const { [action.payload.field]: v, ...stixMapping } = state.stixMapping;
        return {
          ...state,
          stixMapping: stixMapping,
        };
      }
      return state;
    }

    case ADD_VALUE: {
      if (action.payload.field in state.stixMapping) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [action.payload.field]: {
              ...state.stixMapping[action.payload.field],
              values: [
                ...state.stixMapping[action.payload.field].values,
                { value: "", id: uuidv4() },
              ],
            },
          },
        };
      }
      return state;
    }

    case DELETE_VALUE: {
      if (action.payload.field in state.stixMapping) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [action.payload.field]: {
              ...state.stixMapping[action.payload.field],
              values: state.stixMapping[action.payload.field].values.filter(
                (o) => o.id !== action.payload.id
              ),
            },
          },
        };
      }
      return state;
    }

    case UPDATE_VALUE: {
      if (action.payload.field in state.stixMapping) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [action.payload.field]: {
              ...state.stixMapping[action.payload.field],
              values: state.stixMapping[action.payload.field].values.map((o) =>
                o.id === action.payload.id
                  ? { ...o, value: action.payload.value }
                  : o
              ),
            },
          },
        };
      }
      return state;
    }

    case UPDATE_MAPPINGS_FILTER_FIELD_VALUE: {
      return {
        ...state,
        fieldMappingFilter: action.payload.value,
      };
    }

    case UPDATE_FROM_STIX_MAPPINGS_FROM_FILE: {
      return {
        ...state,
        stixMapping: action.payload.stixMapping,
      };
    }

    case CLEAR_FROM_STIX_MAPPINGS: {
      return {
        ...state,
        stixMapping: {},
      };
    }

    case SHOW_CUSTOM_FIELD_MODAL: {
      return {
        ...state,
        customFieldModalShow: true,
      };
    }

    case CLOSE_CUSTOM_FIELD_MODAL: {
      return {
        ...state,
        customFieldModalShow: false,
      };
    }

    default:
      return state;
  }
};

export default FromSTIXReducer;
