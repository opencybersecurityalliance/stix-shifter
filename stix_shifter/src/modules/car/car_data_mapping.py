from stix_shifter.src.exceptions import DataMappingException

# TODO: should this really be a class? Could be a module, made it a class
# in case we have configuration arguments at some point
class CarDataMapper:

    MAPPINGS = {
      "artifact": None,
      "as": None,
      "directory": None,
      "domain-name": {
        "car_type": "flow",
        "fields": {
          "value": "dest_fqdn"
        }
      },
      "email-addr": None,
      "email-message": None,
      "file": {
        "car_type": "file",
        "fields": {
          "hashes.MD5": "md5_hash",
          "hashes.SHA-1": "sha1_hash",
          "hashes.SHA-256": "sha256_hash",
          "name": "file_name",
          "created": "creation_time",
          "parent_directory_ref.path": "file_path"
        }
      },
      "ipv4-addr": {
        "car_type": "flow",
        "fields": {
          "value": "dest_ip"
        }
      },
      "ipv6-addr": None,
      "mac-addr": {
        "car_type": "flow",
        "fields": {
          "value": "mac"
        }
      },
      "mutex": None,
      "network-traffic": {
        "car_type": "flow",
        "fields": {
          "start": "start_time",
          "end": "end_time",
          "src_ref.value": "src_ip", # Impossible to say whether this is IP, domain, or MAC
          "dst_ref.value": "dest_ip",
          "src_port": "src_port",
          "dst_port": "dest_port",
          "protocols[*]": "protocol",
          "src_payload_ref.payload_bin": "content"
        }
      },
      "process": {
        "car_type": "process",
        "fields": {
          "pid": "pid",
          "name": "exe",
          "cwd": "current_directory",
          "command_line": "command_line",
          "creator_user_ref.account_login": "user",
          "binary_ref.name": "exe",
          "binary_ref.parent_directory_ref.path": "image_path",
          "binary_ref.hashes.MD5": "md5_hash",
          "binary_ref.hashes.SHA1": "sha1_hash",
          "binary_ref.hashes.SHA256": "sha256_hash",
          "parent_ref.name": "parent_exe",
          "parent_ref.pid": "ppid",
          "parent_ref.binary_ref.file_name": "parent_exe",
          "parent_ref.binary_ref.parent_directory_ref.path": "parent_image_path",
          "extensions.windows-process-ext.owner_sid": "sid"

        }
      },
      "software": None,
      "url": None,
      "user-account": {
        "car_type": "user_session",
        "fields": {
          "user_id": "logon_id",
          "account_login": "user",
          "account_type": "logon_type"
        }
      },
      "windows-registry-key": {
        "car_type": "registry",
        "fields": {
          "key": "key",
          "values[*]": "value",
          "creator_user_ref.account_login": "user",
        }
      },
      "x509-certificate": None
    }

    def __init__(self, mapping=None):
      # use user defined mapping object if provided in options
      if mapping:
        self.MAPPINGS = mapping

    def map_object(self, stix_object_name):
        if stix_object_name in self.MAPPINGS and self.MAPPINGS[stix_object_name] != None:
            return self.MAPPINGS[stix_object_name]["car_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CAR".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.MAPPINGS and stix_property_name in self.MAPPINGS[stix_object_name]["fields"]:
            return self.MAPPINGS[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into CAR".format(stix_object_name, stix_property_name))

mapper_class = CarDataMapper
