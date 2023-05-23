# SDG

Synthetic Data Generator is a framework for creating a pandas Data Frame based on a description given in the form of a Python class.

Solution of the 2 DataHack case.

## How to use
If you plan to use the project locally, then after downloading the repository, it is enough to start installing dependencies from requirements.txt 

``` pip3 install -r requirements.txt```

Currently, only generation by .py file is supported.

Create a file to use .py and describe the required table as presented in the next section.

After the table is described, to generate data, you need to call the library method and specify the file name, without .py

```
import sdg

dfs = sdg.generate_from_py("example", 1000)
# tables will be created according to the description from the file example.py and containing 1000 lines

```

## Table Description

The table is created based on the Python class, the class must start with the word Table.

Example:

```
from sdg import *


class TableExample:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True], alias="mask_alias")
    float = Float((1.25, 10.), alias="hello_world")
    integer = Integer((1, 10))
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
    date = Date(("2022-10-07", "2022-10-12"))
    timestep = TimeStamp(("2022-10-07 19:45:30", "2022-10-12 19:45:30"))
    alias = Alias("hello_world")
```

### Data Types

Below are descriptions of the data types available for use in the framework.

#### String
#### SetChoice
#### Mask
#### Float
#### Integer
#### WeighedChoice
#### Date
#### TimeStamp
#### Alias


