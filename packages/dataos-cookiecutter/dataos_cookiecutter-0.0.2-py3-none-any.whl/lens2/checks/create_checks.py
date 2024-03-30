import json
import os
import re

import yaml

from lens2.checks.schema_check import schema_check
from lens2.checks.soda_cl_sql_mappings import check_type_sql_mappings


def get_lens_meta(meta_path: str = None):
    try:
        # Check if meta_path is provided, otherwise try to get it from environment variable
        if meta_path is None:
            meta_path = ".meta/_"
            if not os.path.exists(meta_path):
                raise ValueError(f"Meta path - `{meta_path}` does not exist please run your lens.")

        # Open meta file using context manager
        with open(os.path.join(meta_path, "meta.json"), 'r') as f:
            meta = json.load(f)
    except Exception as e:
        # Handle exceptions and provide informative error messages
        raise ValueError(f"Error loading lens meta: {e}")

    return meta


def transformed_lens_meta_checks(meta):
    # column name, table name, check definition
    data = {}
    for table in meta.get('tables', []):
        if table.get('public'):
            table_name = table['name']
            data[table_name] = {}
            for d in table.get('dimensions', []):
                if d.get('meta', {}).get('checks') and d.get('public'):
                    data[table_name][d['name'].split('.')[1]] = d.get('meta', {}).get('checks')
    return data


def get_check_sql(check_type=None, check_sub_type=None, check_sub_type_value=None,
                  column_name=None, table_name=None, mappings=None):
    if check_type == "row_count":
        return mappings[check_type].format(column_name, table_name, column_name)
    elif check_type in ['max_length', 'min_length', 'max', 'min']:
        return mappings[check_type].format(column_name, column_name, table_name)
    elif check_type in ['missing_count']:
        return mappings[check_type].format(column_name, table_name, column_name, column_name)
    elif check_type in ['missing_percent']:
        return mappings[check_type].format(column_name, column_name, table_name, column_name)
    elif check_type in ['avg_length', 'sum', 'avg']:
        return mappings[check_type].format(column_name, column_name, table_name, column_name, column_name)
    elif check_type in ['duplicate_count', 'duplicate_percent']:
        return mappings[check_type].format(column_name, table_name, column_name, column_name, column_name)
    elif check_type == 'missing_checks':
        return mappings[check_type][check_sub_type].format(column_name, table_name, column_name, column_name,
                                                           check_sub_type_value)
    elif check_type == 'invalid_count':
        return mappings[check_type][check_sub_type].format(column_name, column_name, check_sub_type_value,
                                                           column_name, table_name)
    elif check_type == 'invalid_percent':
        return mappings[check_type][check_sub_type].format(column_name, column_name, check_sub_type_value,
                                                           column_name, table_name)
    elif check_type == 'freshness':
        return mappings[check_type].format(column_name, column_name, table_name)
    else:
        pass


def generate_soda_checks_yaml(transformed_meta):
    pattern = re.compile(
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*((?:>=|<=|!=|<>|<|>|=|between|not between)\s*[0-9]+(?:\s*and\s*[0-9]+)?|[0-9]+\s*[dDhHmM])')
    name_attribute_keys = ['name', 'attributes']
    for table_name, v in transformed_meta.items():
        soda_cl_checks = []
        if v:
            for col, checks in v.items():
                for check in checks:
                    if isinstance(check, dict):
                        for k, check_attr in check.items():
                            matches = pattern.findall(k)[0]
                            if 'invalid_count' in matches[0] or 'invalid_percent' in matches[0]:
                                check_name = f"{col}_{matches[0]}"
                                extra_attrs = {key: item for key, item in check_attr.items()
                                               if key in name_attribute_keys}

                                invalid_check_attrs = {" ".join(key.split()): item for key, item in check_attr.items()
                                                       if key not in name_attribute_keys and
                                                       (key.startswith('valid') or key.startswith('invalid'))}
                                if invalid_check_attrs:
                                    check_sub_type = next(iter(invalid_check_attrs))
                                    check_type = 'invalid_count' if 'invalid_count' in matches[0] else 'invalid_percent'
                                    if check_sub_type in ['valid values', 'invalid values']:
                                        if type(invalid_check_attrs[check_sub_type][0]) in [int, float]:
                                            check_sub_type_values = ", ".join(
                                                [str(value) for value in invalid_check_attrs[check_sub_type]])
                                        else:
                                            check_sub_type_values = ", ".join(
                                                [f"'{value}'" for value in invalid_check_attrs[check_sub_type]])

                                        check_sql = get_check_sql(check_type=check_type,
                                                                  check_sub_type=check_sub_type,
                                                                  check_sub_type_value=check_sub_type_values,
                                                                  column_name=col,
                                                                  table_name=table_name,
                                                                  mappings=check_type_sql_mappings)
                                        check_attr_values = {
                                            f"{check_name}_{check_sub_type.replace(' ', '_')} query": check_sql}
                                        check_attr_values.update(extra_attrs)
                                        soda_cl_checks.append({
                                            f"{check_name}_{check_sub_type.replace(' ', '_')} {matches[1]}": check_attr_values})
                                    elif check_sub_type in ['valid length', 'valid max length', 'valid min length',
                                                            'valid min', 'valid max']:
                                        check_sub_type_values = invalid_check_attrs[check_sub_type]
                                        check_sql = get_check_sql(check_type='invalid_count',
                                                                  check_sub_type=check_sub_type,
                                                                  check_sub_type_value=check_sub_type_values,
                                                                  column_name=col,
                                                                  table_name=table_name,
                                                                  mappings=check_type_sql_mappings)
                                        check_attr_values = {
                                            f"{check_name}_{check_sub_type.replace(' ', '_')} query": check_sql}
                                        check_attr_values.update(extra_attrs)
                                        soda_cl_checks.append({
                                            f"{check_name}_{check_sub_type.replace(' ', '_')} {matches[1]}": check_attr_values})
                            else:
                                check_name = f"{col}_{matches[0]}"
                                extra_attrs = {" ".join(key.split()): item for key, item in check_attr.items()
                                               if key in name_attribute_keys}
                                check_sql = get_check_sql(check_type=matches[0],
                                                          column_name=col,
                                                          table_name=table_name,
                                                          mappings=check_type_sql_mappings)
                                # Add extra attributes
                                check_attr_values = {f"{check_name} query": check_sql}
                                check_attr_values.update(extra_attrs)
                                soda_cl_checks.append(
                                    {f"{check_name} {matches[1]}": check_attr_values})
                    elif isinstance(check, str):
                        matches = re.findall(pattern, check)[0]
                        check_name = f"{col}_{matches[0]}"
                        check_sql = get_check_sql(check_type=matches[0],
                                                  column_name=col,
                                                  table_name=table_name,
                                                  mappings=check_type_sql_mappings)
                        soda_cl_checks.append({f"{check_name} {matches[1]}": {f"{check_name} query": check_sql}})
        if not os.path.exists('checks'):
            os.makedirs('checks')

        if soda_cl_checks:
            soda_cl_definition = {f"soda_checks for {table_name}": soda_cl_checks}
            for check_for, definition in soda_cl_definition.items():
                if os.path.exists(os.path.join('checks', f"{table_name}_checks.yaml")):
                    overwrite = input(
                        f"'{table_name}_checks.yaml' already exists. Do you want to overwrite it? (y/n): ").lower() or 'no'
                    if overwrite == 'y':
                        with open(os.path.join('checks', f"{table_name}_checks.yaml"), 'w') as file:
                            file.write(yaml.dump({check_for: definition}, default_flow_style=False, sort_keys=False))
                    else:
                        print("aborted")
                else:
                    with open(os.path.join('checks', f"{table_name}_checks.yaml"), 'w') as file:
                        file.write(yaml.dump({check_for: definition}, default_flow_style=False, sort_keys=False))


def add_subparser(subparsers):
    parser = subparsers.add_parser("checks")
    # Add arguments for the "checks" sub-command
    parser.add_argument("action", choices=["create", "schema-check"], help="Create checks yaml")


def execute_checks(args):
    lens_meta = get_lens_meta()
    if args.action == "create":
        transformed_lens_meta = transformed_lens_meta_checks(lens_meta)
        generate_soda_checks_yaml(transformed_lens_meta)
    elif args.action == "schema-check":
        schema_check(lens_meta)
