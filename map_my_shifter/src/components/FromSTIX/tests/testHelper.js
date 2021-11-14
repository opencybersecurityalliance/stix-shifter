import stixLanguageV2_0 from "../../../global/stixLangV2";
import { requiredStixFields } from "../../../global/requiredStixFields";

export const testArgs = {
  // ------------------------------------------------------
  // stateMappingToShifterMapping

  fromStateMapping: {
    "ipv4-addr:value": {
      values: [
        {
          value: "sourceip",
          id: "58c751a1-154f-42de-b0b5-0e90dbe302ae",
        },
        {
          value: "destinationip",
          id: "6b91d161-b0fc-42a5-b96d-c3f5f7341880",
        },
      ],
    },
    "x-ibm-windows:pipename": {
      values: [
        {
          value: "PipeName",
          id: "c4bdd1b3-590f-45ad-b784-b2b04a152cf4",
        },
      ],
    },
  },

  toShifterMapping: {
    "ipv4-addr": {
      fields: {
        value: ["sourceip", "destinationip"],
      },
    },
    "x-ibm-windows": {
      fields: {
        pipename: ["PipeName"],
      },
    },
  },

  // ------------------------------------------------------
  // shifterMappingToStateMapping

  fromShifterMapping: {
    "ipv4-addr": {
      fields: {
        value: ["sourceip", "destinationip"],
      },
    },
    "x-oca-asset": {
      fields: {
        hostname: ["identityhostname"],
        "ip_refs[*].value": ["identityip", "sourceip"],
        "mac_refs[*].value": ["sourcemac"],
      },
    },
  },

  toStateMapping: [
    {
      "ipv4-addr:value": {
        values: [
          {
            value: "sourceip",
            id: "uuid",
          },
          {
            value: "destinationip",
            id: "uuid",
          },
        ],
      },
      "x-oca-asset:hostname": {
        values: [
          {
            value: "identityhostname",
            id: "uuid",
          },
        ],
      },
      "x-oca-asset:ip_refs[*].value": {
        values: [
          {
            value: "identityip",
            id: "uuid",
          },
          {
            value: "sourceip",
            id: "uuid",
          },
        ],
      },
      "x-oca-asset:mac_refs[*].value": {
        values: [
          {
            value: "sourcemac",
            id: "uuid",
          },
        ],
      },
    },
    {},
  ],

  // ------------------------------------------------------
  // filterMappingFieldsForValue

  filterdMapping: {
    "ipv4-addr:value": {
      values: [
        {
          value: "sourceip",
          id: "uuid",
        },
        {
          value: "destinationip",
          id: "uuid",
        },
      ],
    },
    "x-oca-asset:ip_refs[*].value": {
      values: [
        {
          value: "identityip",
          id: "uuid",
        },
        {
          value: "sourceip",
          id: "uuid",
        },
      ],
    },
  },

  // ------------------------------------------------------
  // getOfficialFieldsFromMapping

  officialStixFields: Object.assign(
    ...Array.from(stixLanguageV2_0, (field) => ({
      [field.type]: field.items.map((item) => item.name),
    }))
  ),

  officialStixKeys: Object.assign(
    {},
    ...Array.from(
      Object.keys(
        Object.assign(
          ...Array.from(stixLanguageV2_0, (field) => ({
            [field.type]: field.items.map((item) => item.name),
          }))
        )
      ),
      (value) => ({
        [value]: new Set(),
      })
    )
  ),

  officialFields: {
    artifact: new Set(),
    "autonomous-system": new Set(),
    directory: new Set(),
    "domain-name": new Set(),
    "email-addr": new Set(),
    "email-message": new Set(),
    file: new Set(),
    "ipv4-addr": new Set(["value"]),
    "ipv6-addr": new Set(),
    "mac-addr": new Set(),
    "network-traffic": new Set(),
    process: new Set(),
    software: new Set(),
    url: new Set(),
    "user-account": new Set(),
    "windows-registry-key": new Set(),
  },

  // ------------------------------------------------------
  // getDataForStatistics

  requiredFields: requiredStixFields.stix_version_2_0,

  // ------------------------------------------------------
  // getNumOfFields

  stixFields: stixLanguageV2_0,
};
