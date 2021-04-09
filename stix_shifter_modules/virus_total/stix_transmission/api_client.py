import json
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.loader import init_analyzer, load_analyzer_module
from stix_shifter_modules.virus_total.models.constants import supportedCortexAnalyzerModules

ANALYZER_NAME = next(iter(supportedCortexAnalyzerModules))
log = logger.set_logger(__name__)


class APIClient:

    def __init__(self, connection, configuration):

        auth_values = configuration.get('auth')
        log.info("Using {}".format(ANALYZER_NAME))

        self.config = self.get_config(auth_values)
        self.analyzer = None
        self.job_input = {}

        self.analyzer_module = load_analyzer_module(supportedCortexAnalyzerModules[ANALYZER_NAME]['path'], supportedCortexAnalyzerModules[ANALYZER_NAME]['name'])

    def ping_data_source(self):
        # Pings the data source

        if self.analyzer is None:
            self.job_input = self.get_job({"data":"", "dataType": "ip"})
            self.analyzer = init_analyzer(self.analyzer_module, self.job_input)

        log.info(f"Pinging {supportedCortexAnalyzerModules[ANALYZER_NAME]['name']}")
        self.analyzer.run() # Run VirusTotalAnalyzer

        result = self.analyzer.output_report if self.analyzer.output_error is None else self.analyzer.output_error
        self.analyzer = None

        return {"success": result['success'], "response": result}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        if self.analyzer is None:
            self.job_input = self.get_job(json.loads(search_id))
            self.analyzer = init_analyzer(self.analyzer_module, self.job_input)

        log.info(f"Running {supportedCortexAnalyzerModules[ANALYZER_NAME]['name']}")
        self.analyzer.run() # Run VirusTotalAnalyzer

        if self.analyzer.output_error is None:
            result = self.analyzer.output_report
            return {"code": 200, "data": result}
        else:
            result = self.analyzer.output_error
            return {"code": 404, "data": result}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

    @staticmethod
    def get_config(authentication_values):
        config = {"service": supportedCortexAnalyzerModules[ANALYZER_NAME]['service']}
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
