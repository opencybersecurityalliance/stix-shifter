
class TaniumConfig:
    
    def __init__(self, connection, configuration):
        self.connection = connection
        self.configuration = configuration
        
    def getHostname(self):
        return self.connection.get('hostname')
    
    def getPort(self):
        return self.connection.get('port')
   
    def getAccessToken(self):
        return self.connection.get('accessToken')
        
    def getResultLimit(self):
        return self.connection['options'].get('result_limit')
        
    def getRequestTimeout(self):
        return self.connection['options'].get('timeout')
