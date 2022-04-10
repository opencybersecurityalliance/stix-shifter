##### Updated on 02/04/22
## OneLogin
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | or |
| = | = |
| OR | or |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | ipaddr |
| <br> | | |
| user-account | user_id | user_id |
| user-account | x_assuming_acting_user_id | assuming_acting_user_id |
| user-account | x_actor_user_name | actor_user_name |
| user-account | x_actor_user_id | actor_user_id |
| user-account | x_account_id | account_id |
| user-account | display_name | user_name |
| <br> | | |
| x-ibm-finding | policy_id | policy_id |
| x-ibm-finding | name | policy_name |
| x-ibm-finding | time_observed | created_at |
| <br> | | |
| x-onelogin-finding | client_id | client_id |
| x-onelogin-finding | directory_id | directory_id |
| x-onelogin-finding | event_type_id | event_type_id |
| x-onelogin-finding | unique_id | id |
| x-onelogin-finding | resolution | resolution |
| x-onelogin-finding | proxy_ip | proxy_ip |
| x-onelogin-finding | role_id | role_id |
| x-onelogin-finding | app_id | app_id |
| x-onelogin-finding | custom_message | custom_message |
| x-onelogin-finding | role_name | role_name |
| x-onelogin-finding | app_name | app_name |
| x-onelogin-finding | group_name | group_name |
| x-onelogin-finding | otp_device_name | otp_device_name |
| x-onelogin-finding | operation_name | operation_name |
| x-onelogin-finding | directory_sync_run_id | directory_sync_run_id |
| x-onelogin-finding | resource_type_id | resource_type_id |
| x-onelogin-finding | browser_fingerprint | browser_fingerprint |
| x-onelogin-finding | notes | notes |
| <br> | | |
| x-onelogin-risk | risk_score | risk_score |
| x-onelogin-risk | risk_reasons | risk_reasons |
| x-onelogin-risk | risk_cookie_id | risk_cookie_id |
| x-onelogin-risk | error_description | error_description |
| <br> | | |
