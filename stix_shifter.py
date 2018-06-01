# Main module to be called
import sys
import importlib

MODULES = ['qradar', 'dummy']

RESULTS = 'results'
QUERY = 'query'


def main():

    # In the case of converting a stix pattern to datasource query, arguments will take the form of...
    # <module> <input_data_translation> <data>
    # The module and input_translation_type will determine what module and method gets called

    input_arguments = sys.argv[1:]

    module = input_arguments[0]
    input_translation_type = input_arguments[1]
    input_data = input_arguments[2]

    result = translate(module, input_translation_type, input_data)
    print(result)
    exit()


def translate(module, translation_type, data):
    if(module not in MODULES):
        raise NotImplementedError

    translator_module = importlib.import_module(
        "src.modules."+module+"."+module+"_translator")

    interface = translator_module.Translator()

    if(translation_type == QUERY):
        # Converting STIX pattern to datasource query
        return interface.transform_query(data)
    elif(translation_type == RESULTS):
        # Converting data from the data source to STIX objects
        return interface.translate_results(data)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
