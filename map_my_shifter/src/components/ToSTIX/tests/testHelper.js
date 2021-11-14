export const testArgs = {
  // ------------------------------------------------------
  // getDataSourceFieldId

  stateMapping: {
    process: {
      "3449d1d8-f0da-419f-a1ca-14d89c679615": {
        field: "username",
        mapped_to: [
          {
            id: "702f1e4d-e75c-4230-83dd-8a5d6c8de1ff",
            key: "process:creator_user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
  },
  objectName: process,

  dataSourceFieldId: "3449d1d8-f0da-419f-a1ca-14d89c679615",

  // ------------------------------------------------------
  // shifterMappingToStateMapping

  shifterMappingQradar: {
    categoryid: [
      {
        key: "x-qradar.category_id",
        object: "x-qradar",
        transformer: "ToInteger",
      },
      {
        key: "x-qradar.category_id",
        object: "x-qradar",
      },
    ],
    username: [
      {
        key: "user-account.user_id",
        object: "useraccount",
      },
      {
        key: "x-ibm-finding.src_application_user_ref",
        object: "finding",
        references: ["useraccount"],
      },
      {
        key: "process.creator_user_ref",
        object: "process",
        references: ["useraccount"],
      },
      {
        key: "x-oca-event.user_ref",
        object: "event",
        references: ["useraccount"],
      },
    ],
  },

  shifterMappingElastic: {
    "@timestamp": [
      {
        key: "first_observed",
        cybox: false,
      },
      {
        key: "last_observed",
        cybox: false,
      },
    ],
    source: {
      ip: [
        {
          key: "ipv4-addr.value",
          object: "src_ip",
        },
        {
          key: "ipv6-addr.value",
          object: "src_ip",
        },
        {
          key: "network-traffic.src_ref",
          object: "nt",
          references: ["src_ip"],
        },
      ],
    },
  },

  stateMappingQradar: [
    {
      "x-qradar": {
        uuid: {
          field: "categoryid",
          mapped_to: [
            {
              id: "uuid",
              key: "x-qradar:category_id",
              transformer: "ToInteger",
            },
            {
              id: "uuid",
              key: "x-qradar:category_id",
            },
          ],
        },
      },
      useraccount: {
        uuid: {
          field: "username",
          mapped_to: [
            {
              id: "uuid",
              key: "user-account:user_id",
            },
          ],
        },
      },
      finding: {
        uuid: {
          field: "username",
          mapped_to: [
            {
              id: "uuid",
              key: "x-ibm-finding:src_application_user_ref",
              references: ["useraccount"],
            },
          ],
        },
      },
      process: {
        uuid: {
          field: "username",
          mapped_to: [
            {
              id: "uuid",
              key: "process:creator_user_ref",
              references: ["useraccount"],
            },
          ],
        },
      },
      event: {
        uuid: {
          field: "username",
          mapped_to: [
            {
              id: "uuid",
              key: "x-oca-event:user_ref",
              references: ["useraccount"],
            },
          ],
        },
      },
    },
    {},
  ],

  stateMappingElastic: [
    {
      src_ip: {
        uuid: {
          field: "source.ip",
          mapped_to: [
            {
              id: "uuid",
              key: "ipv4-addr:value",
            },
            {
              id: "uuid",
              key: "ipv6-addr:value",
            },
          ],
        },
      },
      nt: {
        uuid: {
          field: "source.ip",
          mapped_to: [
            {
              id: "uuid",
              key: "network-traffic:src_ref",
              references: ["src_ip"],
            },
          ],
        },
      },
    },
    {
      "@timestamp": [
        {
          id: "uuid",
          key: "first_observed",
        },
        {
          id: "uuid",
          key: "last_observed",
        },
      ],
    },
  ],

  // ------------------------------------------------------
  // createStateMapping

  shifterMapping: [
    {
      key: "ipv4-addr.value",
      object: "src_ip",
    },
    {
      key: "ipv6-addr.value",
      object: "src_ip",
    },
    {
      key: "network-traffic.src_ref",
      object: "nt",
      references: ["src_ip"],
    },
  ],

  currStateMapping: {
    src_ip: {
      "ff6849ad-62fc-45ee-912c-b84358f022c8": {
        field: "source.ip",
        mapped_to: [
          {
            id: "ccff4a12-b433-42c0-9104-872ab5f686c5",
            key: "ipv4-addr:value",
          },
          {
            id: "00b0bff2-e9b3-4897-9ba2-e0ed4358c1c4",
            key: "ipv4-addr:value",
          },
          {
            id: "727bfa28-11f8-45c2-a449-cfadf7f402d3",
            key: "ipv6-addr:value",
          },
          {
            id: "2e134eea-4207-4163-a5cd-d0957b2fe2bf",
            key: "ipv6-addr:value",
          },
        ],
      },
    },
    nt: {
      "e957360f-ef2e-42fa-ad05-a50c3ae25aac": {
        field: "source.ip",
        mapped_to: [
          {
            id: "1400517f-ea68-4ecc-af74-998767fc109d",
            key: "network-traffic:src_ref",
            references: ["src_ip"],
          },
          {
            id: "6885e92c-497c-44a8-b051-2b9240e6edca",
            key: "network-traffic:src_ref",
            references: ["src_ip"],
          },
        ],
      },
    },
  },

  createdStateMapping: {
    src_ip: {
      "ff6849ad-62fc-45ee-912c-b84358f022c8": {
        field: "source.ip",
        mapped_to: [
          {
            id: "ccff4a12-b433-42c0-9104-872ab5f686c5",
            key: "ipv4-addr:value",
          },
          {
            id: "00b0bff2-e9b3-4897-9ba2-e0ed4358c1c4",
            key: "ipv4-addr:value",
          },
          {
            id: "727bfa28-11f8-45c2-a449-cfadf7f402d3",
            key: "ipv6-addr:value",
          },
          {
            id: "2e134eea-4207-4163-a5cd-d0957b2fe2bf",
            key: "ipv6-addr:value",
          },
        ],
      },
    },
    nt: {
      "e957360f-ef2e-42fa-ad05-a50c3ae25aac": {
        field: "source.ip",
        mapped_to: [
          {
            id: "1400517f-ea68-4ecc-af74-998767fc109d",
            key: "network-traffic:src_ref",
            references: ["src_ip"],
          },
          {
            id: "6885e92c-497c-44a8-b051-2b9240e6edca",
            key: "network-traffic:src_ref",
            references: ["src_ip"],
          },
        ],
      },
    },
  },

  // ------------------------------------------------------
  // stateMappingToShifterMapping

  QradarMapping: {
    "x-qradar": {
      "7cf1f4b3-2c62-4ee7-bd7f-0e18d266440e": {
        field: "categoryid",
        mapped_to: [
          {
            id: "b9e9c970-8b4f-41e2-a3dc-c2da48676d52",
            key: "x-qradar:category_id",
            transformer: "ToInteger",
          },
        ],
      },
    },
    useraccount: {
      "c3e7a403-c733-4b02-8d9b-ec7e24a1f001": {
        field: "username",
        mapped_to: [
          {
            id: "2663fd6e-17dc-4d4f-8c33-f6cd0a317cce",
            key: "user-account:user_id",
          },
        ],
      },
    },
    finding: {
      "5017aa35-239d-495e-9715-4da4a839278f": {
        field: "username",
        mapped_to: [
          {
            id: "ae999cdc-355a-423f-af28-524f3929fea7",
            key: "x-ibm-finding:src_application_user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
    process: {
      "00184524-60bc-41d8-93da-79c4d2570760": {
        field: "username",
        mapped_to: [
          {
            id: "ff0db88b-0e20-4840-bfe6-c42f5829b922",
            key: "process:creator_user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
    event: {
      "598bb818-410d-4cf0-b51c-1c693039ec51": {
        field: "username",
        mapped_to: [
          {
            id: "0c591d52-6160-4756-a8a6-10426e892d58",
            key: "x-oca-event:user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
  },

  QradarOutput: {
    categoryid: [
      {
        key: "x-qradar.category_id",
        object: "x-qradar",
        transformer: "ToInteger",
      },
    ],
    username: [
      {
        key: "user-account.user_id",
        object: "useraccount",
      },
      {
        key: "x-ibm-finding.src_application_user_ref",
        object: "finding",
        references: ["useraccount"],
      },
      {
        key: "process.creator_user_ref",
        object: "process",
        references: ["useraccount"],
      },
      {
        key: "x-oca-event.user_ref",
        object: "event",
        references: ["useraccount"],
      },
    ],
  },

  elasticMapping: [
    {
      src_ip: {
        "375172af-ed16-477a-bca3-5b884d510e0d": {
          field: "source.ip",
          mapped_to: [
            {
              id: "99b12982-c493-4deb-ab42-4640bc576691",
              key: "ipv4-addr:value",
            },
            {
              id: "0e5438ae-da18-442f-b917-eff6c02efd9a",
              key: "ipv6-addr:value",
            },
          ],
        },
        "89890909-ffd1-4e1e-a5e1-76c9d1b58401": {
          field: "source.as.number",
          mapped_to: [
            {
              id: "59d4bc2b-5215-4e6e-876a-b68f6fe166b2",
              key: "ipv4-addr:belongs_to_refs",
              references: ["nt"],
            },
          ],
        },
      },
      nt: {
        "de2857a7-85ad-4aa4-bc5e-4675f8d08187": {
          field: "source.port",
          mapped_to: [
            {
              id: "fed1dff8-fbec-400b-8ff7-291504d654f2",
              key: "network-traffic:src_port",
              transformer: "ToInteger",
            },
          ],
        },
      },
      "autonomous-system": {
        "186c5bb6-e150-476d-915f-07679c1028d4": {
          field: "source.as.number",
          mapped_to: [
            {
              id: "ba70d5a6-fb92-46ec-ad84-668aa70c57d2",
              key: "autonomous-system:number",
            },
          ],
        },
      },
    },
    {
      "@timestamp": [
        {
          id: "f8803c88-81a4-4adc-9aa8-89776b50e1ca",
          key: "first_observed",
        },
        {
          id: "9970eb70-548c-4a31-bc74-480854761b44",
          key: "last_observed",
        },
      ],
      "source.as.organization.name": [
        {
          id: "48d3fc90-393f-42da-b22b-f257afd137dd",
          key: "autonomous-system.name",
        },
      ],
    },
  ],
  elasticOutput: {
    "@timestamp": [
      {
        key: "first_observed",
        cybox: false,
      },
      {
        key: "last_observed",
        cybox: false,
      },
    ],
    "source.as.organization.name": [
      {
        key: "autonomous-system.name",
        cybox: false,
      },
    ],
    source: {
      ip: [
        {
          key: "ipv4-addr.value",
          object: "src_ip",
        },
        {
          key: "ipv6-addr.value",
          object: "src_ip",
        },
      ],
      as: {
        number: [
          {
            key: "ipv4-addr.belongs_to_refs",
            object: "src_ip",
            references: ["nt"],
          },
          {
            key: "autonomous-system.number",
            object: "autonomous-system",
          },
        ],
      },
      port: [
        {
          key: "network-traffic.src_port",
          object: "nt",
          transformer: "ToInteger",
        },
      ],
    },
  },

  // ------------------------------------------------------
  // getValue

  mappedTo: [
    {
      id: "896a76a4-7896-46be-a1f5-462e06ac4d77",
      key: "directory:path",
      transformer: "ToDirectoryPath",
    },
  ],

  // ------------------------------------------------------
  // getDataForStatistics

  mappingForStatictic: {
    "x-qradar": {
      "14c45672-2780-4255-9d50-3f0081718bdb": {
        field: "categoryid",
        mapped_to: [
          {
            id: "64f690f2-4772-4c21-bc34-b454914fba63",
            key: "x-qradar:category_id",
            transformer: "ToInteger",
          },
          {
            id: "5f2efb29-7a0e-4b8d-aeb6-f5bab61f3aff",
            key: "x-qradar:category_id",
          },
        ],
      },
    },
    useraccount: {
      "c181bb89-e313-4b33-9dc9-de742f1c1ca8": {
        field: "username",
        mapped_to: [
          {
            id: "ecd0d6e6-8bcc-4c83-88bb-0490fa323e74",
            key: "user-account:user_id",
          },
        ],
      },
    },
    finding: {
      "dbbdb756-7d7e-41d8-902e-2e9bec913ff0": {
        field: "username",
        mapped_to: [
          {
            id: "a27d2d66-1367-439d-bdf6-43732dc8282d",
            key: "x-ibm-finding:src_application_user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
    process: {
      "f644c2ad-fc29-43b4-a456-4a069bdac9de": {
        field: "username",
        mapped_to: [
          {
            id: "d52c46ab-ba0b-4e87-b403-402b459e0121",
            key: "process:creator_user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
    event: {
      "bfd8fb6b-e6fd-4a22-ace2-341402d2ec8a": {
        field: "username",
        mapped_to: [
          {
            id: "c171f8a2-cf81-451a-a36b-25021fa3ab32",
            key: "x-oca-event:user_ref",
            references: ["useraccount"],
          },
        ],
      },
    },
  },

  stixTypesSet: new Set([
    "artifact",
    "autonomous-system",
    "directory",
    "domain-name",
    "email-addr",
    "email-message",
    "file",
    "ipv4-addr",
    "ipv6-addr",
    "mac-addr",
    "network-traffic",
    "process",
    "software",
    "url",
    "user-account",
    "windows-registry-key",
  ]),

  data: [2, 3, 2, 3],
};
