import pandas as pd
import argparse
import json
from datahack import *
import pickle


def generate(file_name, row_count: int, json_path=None, preset_path=None, test_mode=False):
    ALIAS_LIST = init()

    if json_path is None:
        current_table = {}
    else:
        commands = json.load(open(json_path, 'r'))
        if file_name in commands:
            current_table = commands[file_name]
        else:
            current_table = {}

    module = __import__(file_name)
    table = module.Table()

    fields = list(filter(lambda x: x[0] != "_", dir(table)))
    output = pd.DataFrame(columns=fields, index=range(row_count))
    save = {}

    if preset_path:
        preset = pd.read_csv(preset_path) if ".csv" in preset_path else pd.read_excel(preset_path, engine='openpyxl')
        columns_preset = preset.columns
    else:
        columns_preset = {}

    print("=======Logging Info=======")
    for field in fields:
        if field in columns_preset:
            print(field, type(getattr(table, field)), getattr(table, field).default)
            output[field] = preset[field].copy()

        elif field in current_table:
            cmd = current_table[field]
            data_type = cmd[:cmd.find(" ")]
            argument = cmd[cmd.find(" ") + 1:]
            argument = eval(argument)

            if data_type == "float":
                print(field, type(Float("")), argument)
                if getattr(table, field).alias:
                    output[field] = Float(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = Float(default=argument).generate(row_count)

            elif data_type == "integer":
                print(field, type(Integer("")), argument)
                if getattr(table, field).alias:
                    output[field] = Integer(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = Integer(default=argument).generate(row_count)

            elif data_type == "string":
                print(field, type(String("")), argument)
                if getattr(table, field).alias:
                    output[field] = String(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = String(default=argument).generate(row_count)

            elif data_type == "set_choice":
                print(field, type(SetChoice("")), argument)
                if getattr(table, field).alias:
                    output[field] = SetChoice(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = SetChoice(default=argument).generate(row_count)

            elif data_type == "weight_choice":
                print(field, type(WeighedChoice("")), argument)
                if getattr(table, field).alias:
                    output[field] = WeighedChoice(default=argument, alias=getattr(table, field).alias).generate(
                        row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = WeighedChoice(default=argument).generate(row_count)

            elif data_type == "mask":
                print(field, type(Mask("")), argument)
                if getattr(table, field).alias:
                    output[field] = Mask(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = Mask(default=argument).generate(row_count)

            elif data_type == "date":
                print(field, type(Date("")), argument)
                if getattr(table, field).alias:
                    output[field] = Date(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = Date(default=argument).generate(row_count)

            elif data_type == "timestep":
                print(field, type(TimeStep("")), argument)
                if getattr(table, field).alias:
                    output[field] = TimeStep(default=argument, alias=getattr(table, field).alias).generate(row_count)
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()
                else:
                    output[field] = TimeStep(default=argument).generate(row_count)

            elif data_type == "alias":
                print(field, Alias, argument)
                save[field] = argument

        else:
            print(field, type(getattr(table, field)), getattr(table, field).default)
            if type(getattr(table, field)) == Alias:
                save[field] = getattr(table, field).default
            else:
                output[field] = getattr(table, field).generate(row_count)
                if not getattr(table, field).alias is None:
                    ALIAS_LIST[getattr(table, field).alias] = output[field].copy()

    for field in save.keys():
        output[field] = Alias(save[field]).generate(row_count)

    print("=======Logging Finished=======")
    with open("alias.pk", 'wb') as file:
        pickle.dump(ALIAS_LIST, file)

    if test_mode:
        all_field = {}
        for field in fields:
            all_field[field] = getattr(table, field)
        return all_field, output

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run generator')
    parser.add_argument("--file", '-f', required=True)
    parser.add_argument("--row", '-r', required=False, default=10000)
    parser.add_argument("--json", '-j', required=False)
    parser.add_argument("--preset", '-p', required=False)

    argv = parser.parse_args()
    output = generate(argv.file, int(argv.row), argv.json, argv.preset)
    output.to_parquet(argv.file + ".parquet", index=False)
