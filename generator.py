import pandas as pd
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run generator')
    parser.add_argument("--file", '-f', required=True)
    parser.add_argument("--row", '-r', required=True)

    argv = parser.parse_args()

    row_count = int(argv.row)
    module = __import__(argv.file)
    table = module.Table()

    fields = list(filter(lambda x: x[0] != "_", dir(table)))
    output = pd.DataFrame(columns=fields, index=range(row_count))

    for field in fields:
        output[field] = getattr(table, field).generate(row_count)

    output.to_parquet(argv.file+".parquet")
    output.to_csv(argv.file+".csv")
