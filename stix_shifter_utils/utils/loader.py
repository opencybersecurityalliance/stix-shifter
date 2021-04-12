import os
import sys
import json
import importlib
from cortexutils.analyzer import Analyzer
from stix_shifter_utils.utils import logger


logger = logger.set_logger(__name__)


"""
Overwriting the report and error methods of Analyzer class
"""


def custom_report(self, full_report, ensure_ascii=False):
    summary = {}
    try:
        summary = self.summary(full_report)
    except Exception:
        pass

    self.output_report = {
        "success": True,
        "summary": summary,
        "artifacts": self.artifacts(full_report),
        "full": full_report,
    }


def custom_error(self, message, ensure_ascii=False):
    analyzer_input = self._input
    if "password" in analyzer_input.get("config", {}):
        analyzer_input["config"]["password"] = "REMOVED"
    if "pwd" in analyzer_input.get("config", {}):
        analyzer_input["config"]["pwd"] = "REMOVED"
    if "key" in analyzer_input.get("config", {}):
        analyzer_input["config"]["key"] = "REMOVED"
    if "apikey" in analyzer_input.get("config", {}):
        analyzer_input["config"]["apikey"] = "REMOVED"
    if "api_key" in analyzer_input.get("config", {}):
        analyzer_input["config"]["api_key"] = "REMOVED"

    self.output_error = {
        "success": False,
        "input": analyzer_input,
        "errorMessage": message,
    }


Analyzer.error = custom_error
Analyzer.report = custom_report


"""
Dynamically load the specified analyzer module
"""


def load_analyzer_module(analyzer_path, class_name):
    dir_name = os.path.dirname(analyzer_path)
    module_name = os.path.basename(analyzer_path).split(".")[0]
    module_path = "./stix_shifter_modules/%s" % dir_name
    if module_path not in sys.path:
        sys.path.append(module_path)

    obj = importlib.import_module(module_name)
    analyzer_module = getattr(obj, class_name)
    if analyzer_module == None:
        logger.info("Couldn't find analyzer class in module %s" % module_name)
    return analyzer_module


"""
Initialize analyzer instance and redirect input
"""


def init_analyzer(analyzer_module, query):
    if analyzer_module is None:
        return ""

    read_fd, write_fd = os.pipe()
    os.write(write_fd, bytearray(json.dumps(query), "utf-8"))
    os.close(write_fd)
    temp_f = os.fdopen(read_fd)
    sys.stdin = temp_f
    analyzer = analyzer_module()
    sys.stdin = sys.__stdin__
    temp_f.close()
    analyzer.output_error = None
    analyzer.output_report = {}
    return analyzer