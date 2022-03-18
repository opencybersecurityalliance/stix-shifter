import json
import sys
from argparse import ArgumentParser
from stix2validator import validate_instance, print_results

def __main__():
    bundle_file = sys.argv[1]

    try:
        with open(bundle_file) as f:
            bundle = json.load(f)
        results = validate_instance(bundle)
        if results.is_valid:
            print_results(results)
            print("\n *** STIX bundle is valid but may contain warnings. Warnings marked as yellow [!] can be ignored but recommended to fix ***\n")
        else:
            print_results(results)
            print("\n *** Invalid STIX Objects found in the bundle. Please fix the error marked as Red[X]. Warnings marked as yellow [!] can be ignored but recommended to fix ***\n")
        
    except ValueError as ex:
        print("*** Malformed JSON in the STIX Bundle: " + str(ex))

if __name__ == "__main__":
    __main__()