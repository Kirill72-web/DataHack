import inspect
import pandas as pd
import sys


def generate_from_py(file_name, row_count):
    __import__(file_name)

    tables = [(cls_name, cls_obj) for cls_name, cls_obj in inspect.getmembers(sys.modules[file_name]) if
              inspect.isclass(cls_obj) and "Table" in cls_name]

    output = {}

    for table_name, table in tables:
        fields = list(filter(lambda x: x[0] != "_", dir(table)))

        dataframe = pd.DataFrame(columns=fields, index=range(row_count))

        for field in fields:
            obj = getattr(table, field)
            dataframe[field] = obj.generate(row_count)

        output[table_name.replace("Table", "")] = dataframe

    return output
