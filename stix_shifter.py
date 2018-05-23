# Main module to be called
from src import base_module


def main():
    # In the case of converting a stix pattern to datasource query, arguments will take the form of...
    # <data_source> <input_format> <stix_pattern>
    # The data_source and input_format will determine what module and method gets called
    interface = base_module.TranslationInterface()
    input_arguments = ["some arguments that get passed in"]
    query = interface.stix_to_datasource_query(input_arguments)
    print(query)

    # Converting data from the data source to STIX objects
    qradar_events = ["some json array of events"]
    stix_observables = interface.datasource_to_stix(qradar_events)
    print(stix_observables)


if __name__ == "__main__":
    main()
