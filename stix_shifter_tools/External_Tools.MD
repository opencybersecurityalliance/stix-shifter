Stix Shifter Tools
===============
These are development and testing tools that can be used to assist with developing STIX Shifter. These tools are used externally to the core of STIX Shifter. The intended purpose behind this folder is to hold useful scripts and code that should not be shipped with the stix-shifter package. Included below will be a list of these tools, including their purpose and how to use them.

# Proxy Host Server Routing
The Proxyhost server routing provides a python file with all of the required mappings to start a flask server that can be used to allow communication through the proxy module. The flask server is run on the local instance from the CLI. When a `proxy` data source is passed to the remote instance of stix-shifter, the real connection attributes (data source type, host, and port contained in the options) are passed onto the local instance of stix-shifter running the proxy host. The host will then use the new connector and return results back to the remote stix-shifter instance.

# Requirements
1. stix-shifter-utils must be installed.
2. flask must be installed.
3. You need to be able to access the proxyhost_server_routing.py from your CLI.

# Running the tool

To start a flask server with the proxy host routing map you can run the following command.

```
flask --app 'proxyhost_server_routing:start_proxyhost_flask_server({"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "Bundle","identity_class": "events"})' run'
```

Running this command starts up the server on localhost and on port 5000.

To start the server up the same way as it was done previously (through the stix-shifter CLI)

```
flask --app 'proxyhost_server_routing:start_proxyhost_flask_server({"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "Bundle","identity_class": "events"})' run -h 127.0.0.1 -p 5001 --cert "/Users/StixShifter/stix-shifter/cert.pem" --key "/Users/StixShifter/stix-shifter/key.pem"
```

# Calling the proxy host

Each of the translate and transmit CLI commands outlined in the stix-shifter overview can be used to call the proxy host.

As an example:

```
python main.py transmit proxy '{"options": {"proxy_host": "127.0.0.1", "proxy_port": 5000, "destination": {"connection": {"options": {"result_limit": 10000, "time_range": 5, "timeout": 30}, "host": "<HOST>", "port": <PORT>, "type": "qradar"}, "configuration": {"auth": { "SEC": "<SEC TOKEN>"} } } }}' '{}' ping
```