# OneLogin Connector

This is a connector for searching Onelogin events. 

This example input pattern for TRANSLATE:

`python main.py translate "onelogin" "query" '{}' "[user-account:user_id = 'admin']"`

Returns the following search query:

```
{
    "queries": [
        "user_id=admin&limit=50"
    ]
}
```
