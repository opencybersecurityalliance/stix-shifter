from stix_shifter.stix_translation.src.exceptions import DataMappingException

# TODO: should this really be a class? Could be a module, made it a class
# in case we have configuration arguments at some point
class CimDataMapper:

    MAPPINGS = {
      "artifact": "None",
      "as": "None",
      "directory": {
        "cim_type": "endpoint",
        "fields": {
          "path": "file_path",
          "created": "file_create_time",
          "modified": "file_modify_time"
        }
      },
      "domain-name": {
        "cim_type": "flow",
        "fields": {
          "value": "url"
        }
      },
      "email-addr": {
        "cim_type": "email",
        "fields": {
          "value": ["src_user", "recipient"]
        }
      },
      "email-message": {
        "cim_type": "email",
        "fields": {
          "body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.MD5": "file_hash",
          "body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.SHA-1": "file_hash",
          "body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.SHA-256": "file_hash",
          "body_multipart.[*].'mime-part-type'.body_raw_ref.name": "file_name",
          "body_multipart.[*].'mime-part-type'.body_raw_ref.size": "file_size",
          "to_refs.[*].value": "recipient",
          "cc_refs.[*].value": "recipient",
          "bcc_refs.[*].value": "recipient",
          "subject": "subject",
          "sender_ref.value": "src_user",
          "from_ref.value": "src_user"
        }
      },
      "file": {
        "cim_type": "endpoint",
        "fields": {
          "hashes.MD5": "file_hash",
          "hashes.SHA-1": "file_hash",
          "hashes.SHA-256": "file_hash",
          "name": "file_name",
          "created": "file_create_time",
          "modified": "file_modify_time",
          "parent_directory_ref.path": "file_path",
          "size": "file_size"
        }
      },
      "ipv4-addr": {
        "cim_type": "flow",
        "fields": {
          "value": ["src_ip","dest_ip"]
        }
      },
      "ipv6-addr": {
        "cim_type": "flow",
        "fields": {
          "value": ["src_ipv6","dest_ipv6"]
        }
      },
      "mac-addr": {
        "cim_type": "flow",
        "fields": {
          "value": ["src_mac","dest_mac"]
        }
      },
      "mutex": "None",
      "network-traffic": {
        "cim_type": "network",
        "fields": {
          "src_ref.value": "src",
          "src_port": "src_port",
          "dst_ref.value": "src",
          "dst_port": "dest_port",
          "protocols[*]": "protocol",
          "start":"earliest",
          "end":"latest"
        }
      },
      "process": {
        "cim_type": "process",
        "fields": {
          "name": "process",
          "pid": "pid",
          "creator_user_ref.account_login": "user",
          "binary_ref.parent_directory_ref.path":"file_path",
          "binary_ref.name":"file_name"
        }
      },
      "software": "None",
      "url": {
        "cim_type": "web",
        "fields": {
          "value": "url"
        }
      },
      "user-account": {
        "cim_type": "authentication",
        "fields": {
          "user_id": "user"
        }
      },
      "windows-registry-key": {
        "cim_type": "endpoint",
        "fields": {
          "key": "object",
          "values[*]": "result",
          "creator_user_ref.account_login": "user",
        }
      },
      "x509-certificate": {
        "cim_type": "certificate",
        "fields": {
          "hashes.SHA-256": "ssl_hash",
          "hashes.SHA-1": "ssl_hash",
          "version": "ssl_version",
          "serial_number": "ssl_serial",
          "signature_algorithm": "ssl_signature_algorithm",
          "issuer": "ssl_issuer",
          "subject": "ssl_subject",
          "subject_public_key_algorithm": "ssl_publickey_algorithm"
        }
      }
    }

    FIELDS = {
      "default": [
        "src_ip",
        "src_port",
        "src_mac",
        "src_ipv6",
        "dest_ip",
        "dest_port",
        "dest_mac",
        "dest_ipv6",
        "file_hash",
        "user",
        "url",
        "protocol"
      ]
    }

    def __init__(self, mapping=None, fields=None):
        # use user defined mapping object if provided in options
        if mapping:
            self.MAPPINGS = mapping
        if fields:
            self.FIELDS = fields


    # TODO:
    # This mapping is not super straightforward. It could use the following improvements:
    # * Registry keys need to pull the path apart from the key name, I believe. Need to investigate with Splunk
    # * Need to validate that the src and dest aliases are working
    # * Need to add in the static attributes, like the `object_category` field
    # * Need to verify "software" == "inventory"
    # * Need to figure out network traffic when it's for web URLs
    # * Hashes are kind of hacky, just hardcoded. Probably needs to be a regex
    def map_object(self, stix_object_name):
        if stix_object_name in self.MAPPINGS and self.MAPPINGS[stix_object_name] != None:
            return self.MAPPINGS[stix_object_name]["cim_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CIM".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.MAPPINGS and stix_property_name in self.MAPPINGS[stix_object_name]["fields"]:
            return self.MAPPINGS[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into CIM".format(stix_object_name, stix_property_name))

mapper_class = CimDataMapper
