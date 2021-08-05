from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
import ast
from stix_shifter_utils.utils import logger
from stix_shifter_modules.virus_total.stix_transmission.loader import init_analyzer, load_analyzer_module
from stix_shifter_modules.virus_total.stix_transmission.constants import supportedCortexAnalyzerModules

ANALYZER_NAME = next(iter(supportedCortexAnalyzerModules))
log = logger.set_logger(__name__)

class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.connection = connection
        self.configuration = configuration
        auth_values = configuration.get('auth')
        log.info("Using {}".format(ANALYZER_NAME))
        self.config = self.get_config(auth_values)
        self.analyzer = None
        self.job_input = {}

        self.analyzer_module = load_analyzer_module(supportedCortexAnalyzerModules[ANALYZER_NAME]['path'], supportedCortexAnalyzerModules[ANALYZER_NAME]['name'])

    def ping_connection(self):
        if self.analyzer is None:
            self.job_input = self.get_job({"data":"", "dataType": "ip"})
            self.analyzer = init_analyzer(self.analyzer_module, self.job_input)

        log.info(f"Pinging {supportedCortexAnalyzerModules[ANALYZER_NAME]['name']}")
        self.analyzer.run() # Run VirusTotalAnalyzer

        result = self.analyzer.output_report if self.analyzer.output_error is None else self.analyzer.output_error
        self.analyzer = None

        return {"success": result['success'], "analyzer": ANALYZER_NAME}


    def create_results_connection(self, query_id, offset, length):
        # Return the search results. Results must be in JSON format before being translated into STIX
        if self.analyzer is None:
            self.job_input = self.get_job(ast.literal_eval(query_id))
            self.analyzer = init_analyzer(self.analyzer_module, self.job_input)

        log.info(f"Running {supportedCortexAnalyzerModules[ANALYZER_NAME]['name']}")
        self.analyzer.run() # Run VirusTotalAnalyzer

        if self.analyzer.output_error is None:
            result = self.analyzer.output_report
            return {"success": True, "data": [{"code": 200, "report": result, "data": self.job_input['data'], "dataType": self.job_input['dataType']}]}
        else:
            result = self.analyzer.output_error
            return {"code": 404, "report": result}

    @staticmethod
    def get_config(authentication_values):
        config = supportedCortexAnalyzerModules[ANALYZER_NAME]['config'] if ('config' in supportedCortexAnalyzerModules[ANALYZER_NAME]) else {}
        if authentication_values is None:
            return config
        for key, value in authentication_values.items():
            config[key] = value
        return config
    
    def get_job(self, data):
        job_input = {
            "config": self.config,
            "data": data['data'],
            "dataType": data['dataType']
        }
        return job_input
