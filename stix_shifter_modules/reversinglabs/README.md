# ReversingLabs

Enrich IP addresses, domains, hashes and URLs with the ReversingLabs threat intelligence service.

## Supported STIX Mappings

See the [table of mappings](reversinglabs_supported_stix.md) for the STIX objects and operators supported by this connector.

## ReversingLabs Supported STIX Pattern values (Querying):

The following STIX Patterns are supported by ReversingLabs:

```bash
* ipv4-addr:value
* ipv6-addr:value
* file:hashes.MD5
* file:hashes.SHA-1
* file:hashes.SHA-256   
* domain-name:value
* url:value
```

### Execute a STIX pattern on a ReversingLabs instance

```bash
$ python3 main.py execute reversinglabs reversinglabs "<data_source>" "<connection>" "<configuration>" "<stix_pattern_query>"
```


```bash
python3 main.py execute reversinglabs reversinglabs '{"name": "ReversingLabs", "identity_class": "system"}' '{"host":"www.example.reversinglabs.com", "namespace": "01234567-0123-4567-8901-234567890123"}' '{"auth": {"username": "abc", "password": "xyz"}}' "[file:hashes.MD5 = 'dccbda7c9ad6201ccb088078765e035d']"
```

## Exclusions
ReversingLabs only supports one IOC pattern at a time, and will ignore a query with more AND, OR - it will check the IOC for the first pattern in the query, and return a bundle for that query