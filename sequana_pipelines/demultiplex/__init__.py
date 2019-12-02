import pkg_resources
try:
    version = pkg_resources.require("sequana_demultiplex")[0].version
except:
    version = ">=0.8.0"

