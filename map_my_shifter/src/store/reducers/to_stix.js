import { v4 as uuidv4 } from "uuid";

import {
  ADD_DATASOURCE_FIELD,
  ADD_NEW_STIX_OBJECT,
  ADD_NEW_METADATA_OBJECT,
  UPDATE_OBJECT_NAME,
  OPEN_NEW_OBJECT_MODAL,
  CLOSE_NEW_OBJECT_MODAL,
  REMOVE_DATASOURCE_FIELD,
  MOVE_DATASOURCE_FIELD_TO_OBJECT,
  REMOVE_STIX_OBJECT,
  REMOVE_METADATA_OBJECT,
  UPDATE_DATASOURCE_FIELD,
  ADD_STIX_FIELD,
  REMOVE_STIX_FIELD,
  UPDATE_STIX_FIELD,
  ADD_METADATA_FIELD,
  REMOVE_METADATA_FIELD,
  UPDATE_METADATA_FIELD,
  CLEAR_TO_STIX_MAPPINGS,
  UPDATE_TO_STIX_MAPPINGS_FROM_FILE,
  OPEN_SELECT_FIELD_MODAL,
  CLOSE_SELECT_FIELD_MODAL,
  OPEN_MOVE_FIELD_TO_OBJECT_MODAL,
  CLOSE_MOVE_FIELD_TO_OBJECT_MODAL,
} from "../actions/to_stix";

const INITIAL_STATE = {
  isNewObjectModalOpen: false,
  isNewMetadataFieldModalOpen: false,
  selectFieldModalData: null,
  moveFieldToObjectModalData: null,
  stixMapping: {},
  stixObjects: [],
  metadataMapping: {},
  metadataObjects: [],
};

const ToSTIXReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case OPEN_NEW_OBJECT_MODAL: {
      return {
        ...state,
        isNewObjectModalOpen: true,
      };
    }

    case CLOSE_NEW_OBJECT_MODAL: {
      return {
        ...state,
        isNewObjectModalOpen: false,
      };
    }

    case OPEN_SELECT_FIELD_MODAL: {
      return {
        ...state,
        selectFieldModalData: {
          objectKey: action.payload.objectKey,
          sourceFieldId: action.payload.sourceFieldId,
          stixFieldId: action.payload.stixFieldId,
        },
      };
    }

    case CLOSE_SELECT_FIELD_MODAL: {
      return {
        ...state,
        selectFieldModalData: null,
      };
    }

    case OPEN_MOVE_FIELD_TO_OBJECT_MODAL: {
      return {
        ...state,
        moveFieldToObjectModalData: {
          objectKey: action.payload.objectKey,
          fieldId: action.payload.fieldId,
          fieldName: action.payload.fieldName,
        },
      };
    }

    case CLOSE_MOVE_FIELD_TO_OBJECT_MODAL: {
      return {
        ...state,
        moveFieldToObjectModalData: null,
      };
    }

    case ADD_NEW_STIX_OBJECT: {
      if (!(action.payload?.name in state.stixMapping)) {
        return {
          ...state,
          stixObjects: [...state.stixObjects, action.payload.name],
          stixMapping: {
            ...state.stixMapping,
            [action.payload.name]: {},
          },
        };
      }
      return state;
    }

    case ADD_NEW_METADATA_OBJECT: {
      if (!(action.payload?.name in state.metadataMapping)) {
        return {
          ...state,
          metadataMapping: {
            ...state.metadataMapping,
            [action.payload.name]: [],
          },
        };
      }
      return state;
    }

    case REMOVE_STIX_OBJECT: {
      if (action.payload?.name in state.stixMapping) {
        const { [action.payload?.name]: omit, ...restOfMapping } =
          state.stixMapping;
        return {
          ...state,
          stixObjects: Object.keys(restOfMapping),
          stixMapping: restOfMapping,
        };
      }
      return state;
    }

    case REMOVE_METADATA_OBJECT: {
      if (action.payload?.name in state.metadataMapping) {
        const { [action.payload?.name]: omit, ...restOfMapping } =
          state.metadataMapping;
        return {
          ...state,
          metadataMapping: restOfMapping,
        };
      }
      return state;
    }

    case ADD_DATASOURCE_FIELD: {
      const objectName = action.payload?.objectName;
      if (objectName in state.stixMapping) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: {
              ...state.stixMapping[objectName],
              [uuidv4()]: {
                field: "",
                mapped_to: [],
              },
            },
          },
        };
      }
      return state;
    }

    case UPDATE_DATASOURCE_FIELD: {
      const objectName = action.payload?.objectName;
      const fieldName = action.payload?.fieldName;
      const fieldId = action.payload?.fieldId;
      if (
        objectName in state.stixMapping &&
        fieldId in state.stixMapping[objectName]
      ) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: {
              ...state.stixMapping[objectName],
              [fieldId]: {
                ...state.stixMapping[objectName][fieldId],
                field: fieldName,
              },
            },
          },
        };
      }
      return state;
    }

    case REMOVE_DATASOURCE_FIELD: {
      const objectName = action.payload?.objectName;
      const fieldId = action.payload?.fieldId;
      if (
        objectName in state.stixMapping &&
        fieldId in state.stixMapping[objectName]
      ) {
        const { [fieldId]: omit, ...restOfFields } =
          state.stixMapping[objectName];
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: restOfFields,
          },
        };
      }
      return state;
    }

    case MOVE_DATASOURCE_FIELD_TO_OBJECT: {
      const currObject = state.moveFieldToObjectModalData?.objectKey;
      const objectToMoveTo = action.payload?.objectToMoveTo;
      const fieldId = state.moveFieldToObjectModalData?.fieldId;
      if (
        currObject in state.stixMapping &&
        fieldId in state.stixMapping[currObject]
      ) {
        const { [fieldId]: omit, ...restOfFields } =
          state.stixMapping[currObject];
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectToMoveTo]: {
              ...state.stixMapping[objectToMoveTo],
              [fieldId]: {
                ...state.stixMapping[currObject][fieldId],
              },
            },
            [currObject]: restOfFields,
          },
        };
      }
      return state;
    }

    case ADD_STIX_FIELD: {
      const objectName = action.payload?.objectName;
      const fieldId = action.payload?.fieldId;
      const key = action.payload?.key;
      if (objectName in state.stixMapping) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: {
              ...state.stixMapping[objectName],
              [fieldId]: {
                ...state.stixMapping[objectName][fieldId],
                mapped_to: [
                  ...state.stixMapping[objectName][fieldId].mapped_to,
                  {
                    id: uuidv4(),
                    key: key,
                  },
                ],
              },
            },
          },
        };
      }
      return state;
    }

    case REMOVE_STIX_FIELD: {
      const objectName = action.payload?.objectName;
      const fieldId = action.payload?.fieldId;
      const mappingId = action.payload?.mappingId;
      if (
        objectName in state.stixMapping &&
        fieldId in state.stixMapping[objectName]
      ) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: {
              ...state.stixMapping[objectName],
              [fieldId]: {
                ...state.stixMapping[objectName][fieldId],
                mapped_to: state.stixMapping[objectName][
                  fieldId
                ].mapped_to.filter((o) => o.id !== mappingId),
              },
            },
          },
        };
      }
      return state;
    }

    case UPDATE_STIX_FIELD: {
      const objectName =
        state.selectFieldModalData?.objectKey || action.payload?.objectName;
      const sourceFieldId =
        state.selectFieldModalData?.sourceFieldId || action.payload?.fieldId;
      const stixFieldId =
        state.selectFieldModalData?.stixFieldId || action.payload?.mappingId;
      const value = action.payload?.value;
      const type = action.payload?.type;
      if (
        objectName in state.stixMapping &&
        sourceFieldId in state.stixMapping[objectName]
      ) {
        return {
          ...state,
          stixMapping: {
            ...state.stixMapping,
            [objectName]: {
              ...state.stixMapping[objectName],
              [sourceFieldId]: {
                ...state.stixMapping[objectName][sourceFieldId],
                mapped_to: state.stixMapping[objectName][
                  sourceFieldId
                ].mapped_to.map((o) =>
                  o.id === stixFieldId ? { ...o, [type]: value } : o
                ),
              },
            },
          },
        };
      }
      return state;
    }

    case ADD_METADATA_FIELD: {
      const objectName = action.payload?.objectName;
      if (objectName in state.metadataMapping) {
        return {
          ...state,
          metadataMapping: {
            ...state.metadataMapping,
            [objectName]: [
              ...state.metadataMapping[objectName],
              {
                id: uuidv4(),
                key: "",
              },
            ],
          },
        };
      }
      return state;
    }

    case UPDATE_OBJECT_NAME: {
      const oldName = action.payload?.oldName;
      const newName = action.payload?.newName;
      const isStix = action.payload?.isStix;
      const mapping = isStix ? "stixMapping" : "metadataMapping";
      const objects = isStix ? "stixObjects" : "metadataObjects";
      const oldNameData = state[mapping][oldName];
      const { [oldName]: omit, ...restOfMapping } = state[mapping];
      if (oldName in state[mapping]) {
        return {
          ...state,
          [mapping]: {
            [newName]: {
              ...oldNameData,
            },
            ...restOfMapping,
          },
          [objects]: Object.keys(restOfMapping),
        };
      }
      return state;
    }

    case REMOVE_METADATA_FIELD: {
      const objectName = action.payload?.objectName;
      const mappingId = action.payload?.mappingId;
      if (objectName in state.metadataMapping) {
        return {
          ...state,
          metadataMapping: {
            ...state.metadataMapping,
            [objectName]: state.metadataMapping[objectName].filter(
              (o) => o.id !== mappingId
            ),
          },
        };
      }
      return state;
    }

    case UPDATE_METADATA_FIELD: {
      const objectName = action.payload?.objectName;
      const metadataFieldId = action.payload?.mappingId;
      const value = action.payload?.value;
      const type = action.payload?.type;
      if (objectName in state.metadataMapping) {
        return {
          ...state,
          metadataMapping: {
            ...state.metadataMapping,
            [objectName]: state.metadataMapping[objectName].map((o) =>
              o.id === metadataFieldId ? { ...o, [type]: value } : o
            ),
          },
        };
      }
      return state;
    }

    case CLEAR_TO_STIX_MAPPINGS: {
      return {
        ...state,
        stixMapping: {},
        stixObjects: [],
        metadataMapping: {},
      };
    }

    case UPDATE_TO_STIX_MAPPINGS_FROM_FILE: {
      const stixMapping = action.payload.stixMapping;
      const metadataMapping = action.payload.metadataMapping;
      return {
        ...state,
        stixMapping: stixMapping,
        metadataMapping: metadataMapping,
        stixObjects: Object.keys(stixMapping),
      };
    }

    default: {
      return state;
    }
  }
};

export default ToSTIXReducer;
