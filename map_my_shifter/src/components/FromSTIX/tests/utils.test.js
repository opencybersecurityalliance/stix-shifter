import {
  stateMappingToShifterMapping,
  loadJsonFromDisk,
  shifterMappingToStateMapping,
  filterMappingFieldsForValue,
  getOfficialFieldsFromMapping,
  getDataForStatistics,
  getNumOfFields,
} from "../utils.js";
import { testArgs } from "./testHelper";

jest.mock("uuid", () => {
  const uuidGen = () => `uuid`;
  return { v4: uuidGen };
});

test("stateMappingToShifterMapping", () => {
  expect(stateMappingToShifterMapping(testArgs.fromStateMapping)).toEqual(
    testArgs.toShifterMapping
  );
});

test("loadJsonFromDisk", () => {
  loadJsonFromDisk();
  expect(shifterMappingToStateMapping.toHaveBeenCalled);
});

test("shifterMappingToStateMapping", () => {
  expect(shifterMappingToStateMapping(testArgs.fromShifterMapping)).toEqual(
    testArgs.toStateMapping
  );
});

test("filterMappingFieldsForValue", () => {
  expect(filterMappingFieldsForValue(testArgs.toStateMapping[0], "ip")).toEqual(
    testArgs.filterdMapping
  );
});

test("filterMappingFieldsForValue - empty", () => {
  expect(filterMappingFieldsForValue(testArgs.toStateMapping[0], "")).toEqual(
    testArgs.toStateMapping[0]
  );
});

test("getOfficialFieldsFromMapping", () => {
  expect(
    getOfficialFieldsFromMapping(
      testArgs.toStateMapping[0],
      testArgs.officialStixFields,
      testArgs.officialStixKeys
    )
  ).toEqual(testArgs.officialFields);
});

test("getDataForStatistics", () => {
  expect(
    getDataForStatistics(testArgs.officialFields, testArgs.requiredFields)
  ).toEqual([1, 1]);
});

test("getNumOfFields", () => {
  expect(getNumOfFields(testArgs.stixFields)).toEqual([68, 12]);
});
