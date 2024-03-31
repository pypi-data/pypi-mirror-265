# baseopt

A simple package for parsing and managing CLI options/arguments from getopt.

## Install

```shell
pip install baseopt
```

## Usage

```python
import sys
from baseopt import BaseOption, BaseOptions

# Or you can just initialize the BaseOptions
options = BaseOptions([
    BaseOption(name="help", shortname="h", dtype=bool, default=False),
    BaseOption(name="file", shortname="f", dtype=str, doc="Path to the input file")
])

# Or you can create your own option classes
class Options(BaseOptions):
    def __init__(self):
    super().__init__()

    # Append available options
    self.add(name="help", shortname="h", dtype=bool, default=False)
    self.add(name="file", shortname="f", dtype=str, doc="Path to the input file")

options = Options()

# Parse command line arguments
options.parse(sys.argv[1:])

# Check if we should print a help message
if options["help"].value:
    options.help()
    sys.exit(1)

print(options["file"].value)
```

Executing the above script gives

```
Options:
  -h | --help
  -f | --file              Path to the input file
                           (def = "None")
```