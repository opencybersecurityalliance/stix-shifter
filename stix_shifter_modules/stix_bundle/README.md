Example of stix_bundle translate:
```
python main.py translate stix_bundle query '{}' "[ipv4-addr:value = '127.0.0.1']"
```

Example of stix_bundle transmission
```
python main.py transmit stix_bundle '{"host":"https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/1.json"}' '{}' results "[ipv4-addr:value = '127.0.0.1']" 0 9
```
