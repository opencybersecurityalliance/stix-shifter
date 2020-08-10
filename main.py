from stix_shifter.scripts.stix_shifter import main
import sys


arguments = sys.argv
for i in range(len(arguments)-1):
    arguments[i-1] = arguments[i-1].replace("\\","")
if __name__ == "__main__":
    main()