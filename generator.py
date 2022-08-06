import pandas as pd
import argparse
import json
from datahack import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run generator')
    parser.add_argument("--file", '-f', required=True)
    parser.add_argument("--row", '-r', required=True)
    parser.add_argument("--json", '-j', required=False)

    argv = parser.parse_args()

    commands = json.load(open(argv.json, 'r'))
    current_table = commands[argv.file]
    row_count = int(argv.row)
    module = __import__(argv.file)
    table = module.Table()

    fields = list(filter(lambda x: x[0] != "_", dir(table)))
    output = pd.DataFrame(columns=fields, index=range(row_count))

    for field in fields:
        if field in current_table:
            cmd = current_table[field]
            data_type = cmd[:cmd.find(" ")]
            argument = cmd[cmd.find(" ")+1:]
            argument = eval(argument)
            if data_type == "number":
                output[field] = Number(default=argument).generate(row_count)
        else:
            output[field] = getattr(table, field).generate(row_count)

    output.to_parquet(argv.file+".parquet", index=False)
    output.to_csv(argv.file+".csv", index=False)
