## Transmissions module for Cortex analyzers

The following methods are supported:
```
ping
is_async (-> True)
query (all available analyzers work with all provided observables when applicable)
status
results (returns all extracted artifacts)
```

__REMINDER: The transmission module is only returning results for a Cortex analyzer who's option `Extract Observables` is enabled (server side option, talk to your admin if necessary).__

### Further configuration options

#### Proxies

The provided configuration-json can be extended by a `http_proxy` and/or a `https_proxy` parameter for proxy support. A `verify_cert` option is also available. __See [Cortex4Py API Usage](https://github.com/TheHive-Project/Cortex4py/blob/master/Usage.md) for more details__
