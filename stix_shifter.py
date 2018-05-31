# Main module to be called
from src import base_module
#from src.modules.qradar.qradar_module import Translator
import sys
import importlib

DATASOURCES = ['qradar']
INPUT_DATA_MODELS = ['sco']


def main():

    # In the case of converting a stix pattern to datasource query, arguments will take the form of...
    # <data_source> <input_format> <stix_pattern>
    # The data_source and input_format will determine what module and method gets called

    #interface = base_module.TranslationInterface()

    input_arguments = sys.argv[1:]
    data_source_module = input_arguments[0]
    input_data_model = input_arguments[1]
    input_data = input_arguments[2]

    module = importlib.import_module(
        "src.modules." + data_source_module + "." + data_source_module + "_module")

    interface = module.Translator()

    # TODO: Figure out how we want to differentiate if we're translating TO or FROM stix. Seems like that should be the second variable instead of whatever input_data_models is for
    if(input_data_model in INPUT_DATA_MODELS):
        # Converting STIX pattern to datasource query
        query = interface.stix_to_datasource_query(input_data)
        # TODO: return query instead of print
        print(query)
        exit()
    elif(input_data_model == 'qradar_events'):
        # Converting data from the data source to STIX objects
        stix_observables = interface.datasource_results_to_stix(input_data)

        # TODO: return stix_observables instead of print
        print(stix_observables)
        exit()
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
