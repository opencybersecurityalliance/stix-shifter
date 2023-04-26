# STIX Bundle

Example of stix_bundle translate:
```
python main.py translate stix_bundle query '{}' "[ipv4-addr:value = '127.0.0.1']"
```

Example of stix_bundle transmission (stix v2.0)
```
python main.py transmit stix_bundle '{"host":"https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/1.json"}' '{}' results "[ipv4-addr:value = '127.0.0.1']" 0 9
```


Example of stix_bundle transmission (stix v2.1)
```
python main.py transmit stix_bundle '{"host":"https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/stix-2.1.json", "options": {"stix_2.1": true}}' '{}' results "[ipv4-addr:value = '127.0.0.1']" 0 9 
```
