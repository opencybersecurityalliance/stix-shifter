# OneLogin Connector

This is a connector for searching Onelogin events. 

This example input pattern for TRANSLATE:

`python main.py translate "onelogin" "query" '{}' "[user-account:user_id= '123456']"`

Returns the following search query:

```
{
    "queries": [
        "user_id=123456&limit=50"
    ]
}
```
