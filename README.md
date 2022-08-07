# DataHack

Solution of case #2 of the Dotahack hackathon, on the development of a system for generating synthetic data.

## How to use
If you plan to use the project locally, then after downloading the repository, it is enough to start installing dependencies from requirements.txt 

``` pip3 install -r requirements.txt```

and work with the script generator.py.

```python3.9 generator.py -f file_name_without_.py [-r row_count] [-j path_to_json_file] [-p path_to_preset_data_in_csv/excel]```

If a docker scan is required, it is enough to download Dockerfile and run the docker build.

```docker build - < Dockerfile```

then launch the container 

```docker run -it image_id bash ```

and you will have the opportunity to work with the project in a stable environment. Further work is no different, all flags are generator.py are identical.

## Table Description

The table is created based on the Python class, where the class fields are the columns of the table, the values of the data type fields in the column.
It is mandatory that the class is called Table, then the file name will become the name of the future table.

Example:

```
from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True], alias="mask_alias")
    float = Float((1.25, 10.), alias="hello_world")
    integer = Integer((1, 10))
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
    date = Date(("2022-10-07", "2022-10-12"))
    timestep = TimeStep(("2022-10-07 19:45:30", "2022-10-12 19:45:30"))
    a = Alias("hello_world")
```
