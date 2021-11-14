const stixLanguageV2 = [
  {
    title: "Artifact",
    type: "artifact",
    items: [
      { name: "mime_type", required: false },
      { name: "payload_bin", required: false },
      { name: "url", required: false },
      { name: "hashes.SHA-256", required: false },
      { name: "hashes.MD5", required: false },
      { name: "hashes.SHA-1", required: false },
    ],
  },
  {
    title: "AS",
    type: "autonomous-system",
    items: [
      { name: "number", required: true },
      { name: "name", required: false },
      { name: "rir", required: false },
    ],
  },
  {
    title: "Directory",
    type: "directory",
    items: [
      { name: "path", required: true },
      { name: "path_enc", required: false },
      { name: "created", required: false },
      { name: "modified", required: false },
      { name: "accessed", required: false },
    ],
  },
  {
    title: "Domain Name",
    type: "domain-name",
    items: [{ name: "value", required: true }],
  },
  {
    title: "Email Address",
    type: "email-addr",
    items: [
      { name: "value", required: true },
      { name: "display_name", required: false },
    ],
  },
  {
    title: "Email Message",
    type: "email-message",
    items: [
      { name: "is_multipart", required: true },
      { name: "date", required: false },
      { name: "content_type", required: false },
      { name: "subject", required: false },
      { name: "body", required: false },
    ],
  },
  {
    title: "File",
    type: "file",
    items: [
      { name: "hashes.SHA-256", required: false },
      { name: "hashes.MD5", required: false },
      { name: "hashes.SHA-1", required: false },
      { name: "size", required: false },
      { name: "name", required: false },
      { name: "name_enc", required: false },
      { name: "magic_number_hex", required: false },
      { name: "mime_type", required: false },
      { name: "created", required: false },
      { name: "modified", required: false },
      { name: "accessed", required: false },
      { name: "parent_directory_ref", required: false },
      { name: "is_encrypted", required: false },
    ],
  },
  {
    title: "IPv4 Address",
    type: "ipv4-addr",
    items: [{ name: "value", required: true }],
  },
  {
    title: "IPv6 Address",
    type: "ipv6-addr",
    items: [{ name: "value", required: true }],
  },
  {
    title: "MAC Address",
    type: "mac-addr",
    items: [{ name: "value", required: true }],
  },
  {
    title: "Network Traffic",
    type: "network-traffic",
    items: [
      { name: "src_ref", required: false },
      { name: "dst_ref", required: false },
      { name: "src_port", required: false },
      { name: "dst_port", required: false },
      { name: "protocols", required: false },
    ],
  },
  {
    title: "Process",
    type: "process",
    items: [
      { name: "pid", required: false },
      { name: "name", required: false },
      { name: "created", required: false },
      { name: "command_line", required: false },
      { name: "opened_connection_refs", required: false },
      { name: "creator_user_ref", required: false },
      { name: "binary_ref", required: false },
      { name: "parent_ref", required: false },
    ],
  },
  {
    title: "Software",
    type: "software",
    items: [
      { name: "name", required: true },
      { name: "cpe", required: false },
      { name: "vendor", required: false },
      { name: "version", required: false },
    ],
  },
  {
    title: "URL",
    type: "url",
    items: [{ name: "value", required: true }],
  },
  {
    title: "User Account",
    type: "user-account",
    items: [
      { name: "user_id", required: true },
      { name: "account_login", required: false },
      { name: "account_type", required: false },
      { name: "display_name", required: false },
      { name: "is_service_account", required: false },
      { name: "is_privileged", required: false },
      { name: "is_disabled", required: false },
    ],
  },
  {
    title: "Windows™ Registry Key",
    type: "windows-registry-key",
    items: [
      { name: "key", required: true },
      { name: "values", required: false },
      { name: "modified", required: false },
      { name: "creator_user_ref", required: false },
      { name: "number_of_subkeys", required: false },
    ],
  },
];

export default stixLanguageV2;
