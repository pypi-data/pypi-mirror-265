import json
import os
import subprocess

import yaml
from dotenv import load_dotenv
from lens2.checks.schema_check import get_env_or_throw
from sql_metadata import Parser


def get_rill_version():
    try:
        version_output = subprocess.check_output(['rill', 'version'], stderr=subprocess.STDOUT)
        rill_version = version_output.decode('utf-8')
    except FileNotFoundError as e:
        raise FileNotFoundError("rill not found  please install using command - `curl https://rill.sh | sh`")
    return rill_version


def get_lens_meta(meta_path: str = None):
    # Check if meta_path is provided, otherwise try to get it from environment variable
    if meta_path is None:
        try:
            meta_path = ".meta/_"
            if not os.path.exists(meta_path):
                raise ValueError(f"Meta path - `{meta_path}` does not exist please run your lens.")
        except Exception as e:
            raise ValueError(f"Meta path - `{meta_path}` does not exist please run your lens.")

    # Open meta file
    with open(os.path.join(meta_path, "meta.json"), 'r') as f:
        lens_meta = json.loads(f.read())
    return lens_meta


def measure_dimension_sqls(lens_meta):
    transformed_meta = {}
    for t in lens_meta['tables']:
        if t['type'] == 'table':
            for m in t['measures']:
                transformed_meta[m['name']] = {'sql': m['sql'],
                                               'info': m}
            for d in t['dimensions']:
                transformed_meta[d['name']] = {'sql': d['sql'],
                                               'info': d}
    return transformed_meta


def replace_with_dict(string, replacement_dict):
    for key, value in replacement_dict.items():
        string = string.replace(key, value)
    return string


def get_sql_expression(agg_type, sql, table_name, is_prefix):
    # SQL Manipulation
    cols = Parser(f"SELECT {sql}").columns
    cols = {col: f"{table_name}_{col}" for col in cols}
    if is_prefix:
        sql = replace_with_dict(sql, cols)

    if agg_type in ["countDistinct", "countDistinctApprox"]:
        return f"COUNT(DISTINCT {sql})"
    elif agg_type in ["count", "sum", "avg", "min", "max"]:
        return f"{agg_type}({sql})"
    elif agg_type in ["string", "time", "boolean", "number"]:
        return f"{sql}"


def create_rill_json():
    lens_meta = get_lens_meta()
    lens_name = lens_meta['name']
    transformed_lens_meta = measure_dimension_sqls(lens_meta)
    rill_data = {}
    for v in lens_meta['tables']:
        if v['type'] == 'view':
            print(f"Generating rill yaml for - {v['name']}")
            rill_data[v['name']] = {'sql': '',
                                    'dimensions': [],
                                    'measures': [],
                                    'timeseries': ''
                                    }
            existing_dimensions = []

            if len(v['dimensions']) == 0:
                print(f"No dimension found  for view - `{v['name']}`")

            for d in v['dimensions']:
                d_name = d['name'].split('.')[1]
                # check if dimension is type of time
                if d['type'] == 'time' and rill_data[v['name']]['timeseries'] == '':
                    rill_data[v['name']]['timeseries'] = d_name
                rill_data[v['name']]['dimensions'].append({
                    "label": d['shortTitle'],
                    "description": d.get('description', d['title']),
                    "name": d_name,
                    "property": d_name
                })
                existing_dimensions.append(d_name)
            for m in v['measures']:
                if m['public']:
                    m_name = m['name'].split('.')[1]
                    m_alias = m['aliasMember']
                    replace_chars = lambda s: s.replace('`', '').replace('TABLE.', '').replace('{', ''). \
                        replace('}', '').replace('$', '')
                    measure_sql = replace_chars(transformed_lens_meta[m_alias]['sql'])
                    measure_query = f"SELECT {measure_sql}"
                    m_dimension_columns = Parser(measure_query).columns  # measure sql columns
                    is_skip = False  # Assume we don't skip by default
                    is_prefix = True if m_alias.split('.')[0] in m_name else False
                    # Check if dimension exist or not.
                    for m_dim_name in m_dimension_columns:
                        if is_prefix:
                            m_dim_name_with_table = f"{m_alias.split('.')[0]}_{m_dim_name}"
                        else:
                            m_dim_name_with_table = m_dim_name
                        if m_dim_name_with_table not in existing_dimensions:
                            is_skip = True  # If any dimension is missing, we set to skip
                            print(
                                f"Skipping measure - `{m_name}`, its dependent dimension - `{m_dim_name}` is missing "
                                f"in view - `{v['name']}`")
                            break
                    if is_skip is False:
                        rill_data[v['name']]['measures'].append({
                            "label": m['shortTitle'],
                            "name": m_name,
                            "description": m.get('description', m['title']),
                            "expression": get_sql_expression(m['aggType'], measure_sql, m_alias.split('.')[0],
                                                             is_prefix)
                        })

            rill_data[v['name']]['sql'] = f"SELECT {', '.join([_['name'] for _ in rill_data[v['name']]['dimensions']])}" \
                                          f" FROM {v['name']}"
    # print('\n')
    return rill_data, lens_name


def dir_check(rill_path=None):
    if not os.path.exists(rill_path):
        os.makedirs(rill_path)
    # Check if sub folders 'dashboards', 'models', and 'sources' exist within 'rill' folder
    sub_folders_path = ['dashboards', 'models', 'sources']
    for sub_folder in sub_folders_path:
        sub_folder_path = os.path.join(rill_path, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)
    return rill_path


def create_rill_files(data, rill_path=None, lens_name=None, rill_version=None):
    curr_dir = os.getcwd()
    folder_name = os.path.basename(curr_dir)
    env_file = ".env"
    if os.path.exists(env_file) is False:
        raise FileNotFoundError(
            f"`.env` file not found in folder - `{folder_name}`. Create a `.env` file in folder - `{folder_name}`")

    # check if required env exist or not.
    load_dotenv('.env')
    required_envs = {'LENS2_LOCAL_PG_PASSWORD': None,
                     'LENS2_LOCAL_PG_USER': None}
    for k in required_envs.keys():
        required_envs[k] = get_env_or_throw(k)

    for k, v in data.items():
        rill_yaml_path = os.path.join(rill_path, f"rill.yaml")
        with open(rill_yaml_path, 'w') as file:
            rill_data = {"compiler": "rill",
                         "rill_version": rill_version,
                         "name": lens_name}
            file.write(yaml.dump(rill_data, default_flow_style=False, sort_keys=False))

        source_path = os.path.join(rill_path, f"sources/{k}.yaml")
        if os.path.exists(source_path):
            overwrite = input(f"The file `{source_path}` already exists. Do you want to overwrite it? (y/N): ")
            if overwrite.lower() != 'y':
                break
        with open(source_path, 'w') as file:
            source = {"type": "postgres",
                      "sql": v['sql'],
                      "database_url": f"postgres://{required_envs['LENS2_LOCAL_PG_USER']}:"
                                      f"{required_envs['LENS2_LOCAL_PG_PASSWORD']}@localhost:15432/db"}
            file.write(yaml.dump(source, default_flow_style=False, sort_keys=False))

        model_path = os.path.join(rill_path, f"models/{k}_model.sql")
        if os.path.exists(model_path):
            overwrite = input(f"The file `{model_path}` already exists. Do you want to overwrite it? (y/N): ")
            if overwrite.lower() != 'y':
                break
        with open(os.path.join(rill_path, f"models/{k}_model.sql"), 'w') as file:
            file.write(f"""SELECT * FROM {k}""")

        dashboard_path = os.path.join(rill_path, f"dashboards/{k}_dashboard.yaml")
        if os.path.exists(dashboard_path):
            overwrite = input(f"The file `{dashboard_path}` already exists. Do you want to overwrite it? (y/N): ")
            if overwrite.lower() != 'y':
                break
        with open(os.path.join(rill_path, f"dashboards/{k}_dashboard.yaml"), 'w') as file:
            dashboard = {
                "title": ' '.join([part.capitalize() for part in k.split('_')]),
                "model": f"{k}_model",
                "dimensions": v['dimensions'],
                "measures": v['measures'],
                "timeseries": v.get('timeseries', '')
            }
            file.write(yaml.dump(dashboard, default_flow_style=False, sort_keys=False))


def add_create_subparser(subparsers):
    subparsers.set_defaults(func=execute_create)


def execute_create():
    rill_version = get_rill_version()
    rill_path = 'rill'
    dir_check(rill_path)
    rill_data, lens_name = create_rill_json()
    create_rill_files(rill_data, rill_path=rill_path, lens_name=lens_name, rill_version=rill_version)
