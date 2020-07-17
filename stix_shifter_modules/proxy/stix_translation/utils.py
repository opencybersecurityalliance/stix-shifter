def unwrap_connection_options(self, connection):
    connection_options = connection.get('options', {})
    embedded_connection_options = connection_options.get('options', {})
    if embedded_connection_options and embedded_connection_options.get('host'):
        connection['host'] = embedded_connection_options.get('host')
        connection['port'] = embedded_connection_options.get('port')
        connection['type'] = embedded_connection_options.get('type')
        del connection['options']
        connection.update(connection_options)
    elif connection_options and connection_options.get('host'):
        del connection['options']
        connection.update(connection_options)
    return connection