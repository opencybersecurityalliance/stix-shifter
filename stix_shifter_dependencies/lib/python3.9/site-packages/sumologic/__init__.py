import sys
if sys.version_info.major >= 3:
    from sumologic.sumologic import *
else:
    from sumologic import *