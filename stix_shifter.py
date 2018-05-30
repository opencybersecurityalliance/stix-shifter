# Main module to be called
from src import base_module
import sys


def main():

    # In the case of converting a stix pattern to datasource query, arguments will take the form of...
    # <data_source> <input_format> <stix_pattern>
    # The data_source and input_format will determine what module and method gets called
    interface = base_module.TranslationInterface()

    input_arguments = sys.argv[1:]
    data_source_module = input_arguments[0]
    input_data_model = input_arguments[1]

    if(input_data_model in interface.INPUT_DATA_MODELS):
        # Converting STIX pattern to datasource query
        query = interface.stix_to_datasource_query(input_arguments)
        print(query)
        exit()
    elif(input_data_model == 'qradar_events'):
        # Converting data from the data source to STIX objects
        # Not implemented yet. Only returning dummy data right now
        qradar_events = ["some json array of events"]
        stix_observables = interface.datasource_to_stix(qradar_events)
        print(stix_observables)
        exit()
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
