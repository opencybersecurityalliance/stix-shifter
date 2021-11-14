import { v4 as uuidv4 } from "uuid";

export function loadJsonFromDisk(obj) {
  return shifterMappingToStateMapping(obj, {}, {}, "");
}

export function getDataSourceFieldId(
  stateMapping,
  objectName,
  fieldName,
  dataSourceFieldId
) {
  let ids = [];
  if (objectName in stateMapping) {
    ids = Object.keys(stateMapping[objectName]).filter((id) => {
      return fieldName === stateMapping[objectName][id].field;
    });
  }
  const id = ids.length !== 0 ? ids[0] : dataSourceFieldId;
  return id;
}

export function shifterMappingToStateMapping(
  shifterMapping,
  stateMapping,
  metadataMapping,
  fieldName
) {
  if (!shifterMapping) return stateMapping;
  Object.keys(shifterMapping).forEach((dataSourceField) => {
    const newFieldName = getFieldName(fieldName, dataSourceField);
    if (
      new Set(Object.keys(shifterMapping[dataSourceField])).has("key") &&
      shifterMapping[dataSourceField].key.constructor === String
    ) {
      if (new Set(Object.keys(shifterMapping[dataSourceField])).has("object")) {
        stateMapping = createStateMapping(
          shifterMapping,
          stateMapping,
          dataSourceField,
          newFieldName
        );
      } else {
        metadataMapping = createMetadata(
          shifterMapping,
          metadataMapping,
          dataSourceField,
          newFieldName
        );
      }
    } else
      shifterMappingToStateMapping(
        shifterMapping[dataSourceField],
        stateMapping,
        metadataMapping,
        newFieldName
      );
  });
  return [stateMapping, metadataMapping];
}

export function getFieldName(fieldName, dataSourceField) {
  return fieldName
    ? isNaN(parseInt(dataSourceField))
      ? `${fieldName}.${dataSourceField}`
      : fieldName
    : dataSourceField;
}

export function createStateMapping(
  shifterMapping,
  stateMapping,
  dataSourceField,
  fieldName
) {
  const objectName = shifterMapping[dataSourceField].object;
  const dataSourceFieldId = uuidv4();
  const mapped_to_id = uuidv4();
  let id = getDataSourceFieldId(
    stateMapping,
    objectName,
    fieldName,
    dataSourceFieldId
  );
  const references = shifterMapping[dataSourceField]?.references;
  const transformer = shifterMapping[dataSourceField]?.transformer;

  if (!(objectName in stateMapping)) stateMapping[objectName] = {};
  if (!(id in stateMapping[objectName])) stateMapping[objectName][id] = {};
  if (!("field" in stateMapping[objectName][id])) {
    stateMapping[objectName][id] = {
      field: fieldName,
      mapped_to: [],
    };
  }
  stateMapping[objectName][id].mapped_to = [
    ...stateMapping[objectName][id].mapped_to,
    {
      id: mapped_to_id,
      key: shifterMapping[dataSourceField].key.replace(".", ":"),
      ...(transformer ? { transformer: transformer } : {}),
      ...(references
        ? {
            references:
              references.constructor === Array ? references : [references],
          }
        : {}),
    },
  ];
  return stateMapping;
}

export function createMetadata(
  shifterMapping,
  metadataMapping,
  dataSourceField,
  fieldName
) {
  const key = shifterMapping[dataSourceField].key;
  const transformer = shifterMapping[dataSourceField]?.transformer;
  const id = uuidv4();
  if (!(fieldName in metadataMapping)) metadataMapping[fieldName] = [];
  metadataMapping[fieldName] = [
    ...metadataMapping[fieldName],
    {
      id: id,
      key: key,
      ...(transformer ? { transformer: transformer } : {}),
    },
  ];
  return metadataMapping;
}

export function buildInnerField(sourceField, outputLevel) {
  const splitedField = sourceField.split(".");
  const innerField = splitedField[splitedField.length - 1];
  for (let i = 0; i < splitedField.length - 1; i++) {
    if (splitedField[i] in outputLevel)
      outputLevel = outputLevel[splitedField[i]];
    else {
      outputLevel[splitedField[i]] = {};
      outputLevel = outputLevel[splitedField[i]];
    }
  }
  return [innerField, outputLevel];
}

export function stateMappingToShifterMapping(stateMapping, metadataMapping) {
  let output = {};
  Object.keys(metadataMapping).forEach((field) => {
    Object.keys(metadataMapping[field]).forEach((index) => {
      const transformer = getValue(metadataMapping[field][index]?.transformer);
      if (!(field in output)) {
        output[field] = [];
      }
      output[field] = [
        ...output[field],
        {
          key: metadataMapping[field][index].key,
          ...(transformer ? { transformer: transformer } : {}),
          cybox: false,
        },
      ];
    });
  });
  Object.keys(stateMapping).forEach((object) => {
    Object.keys(stateMapping[object]).forEach((field) => {
      let sourceField = stateMapping[object][field].field;
      const mappedTo = stateMapping[object][field].mapped_to;
      Object.keys(mappedTo).forEach((index) => {
        const key = mappedTo[index].key.replace(":", ".");
        const transformer = getValue(mappedTo[index]?.transformer);
        const references = getValue(mappedTo[index].references);
        let outputLevel = output;
        let innerField = sourceField;
        if (sourceField.includes(".")) {
          [innerField, outputLevel] = buildInnerField(sourceField, outputLevel);
        }
        if (!(innerField in outputLevel)) {
          outputLevel[innerField] = [];
        }
        outputLevel[innerField] = [
          ...outputLevel[innerField],
          {
            key: key,
            object: object,
            ...(transformer ? { transformer: transformer } : {}),
            ...(references ? { references: references } : {}),
          },
        ];
      });
    });
  });
  return output;
}

export function getValue(value) {
  return value && value !== "None" && value.length !== 0 ? value : null;
}

export function getDataForStatistics(stixMapping, stixTypesSet) {
  const officialFields = new Set();
  const CustomFields = new Set();
  const officialObjects = new Set();
  const CustomObjects = new Set();
  Object.keys(stixMapping).forEach((object) => {
    Object.keys(stixMapping[object]).forEach((id) => {
      Object.keys(stixMapping[object][id].mapped_to).forEach((index) => {
        const [type, key] =
          stixMapping[object][id].mapped_to[index].key.split(":");
        if (stixTypesSet.has(type)) {
          officialFields.add(`${type}:${key}`);
          officialObjects.add(object);
        } else if (type.startsWith("x-")) {
          CustomFields.add(`${type}:${key}`);
          CustomObjects.add(object);
        }
      });
    });
  });
  const data = [
    officialFields.size,
    CustomFields.size,
    officialObjects.size,
    CustomObjects.size,
  ];
  return data;
}

export function isValidObjectName(oldName, newName, objects) {
  return newName && (oldName === newName || !objects.includes(newName));
}

export function isActiveObject(object, activObject) {
  return object === activObject;
}
