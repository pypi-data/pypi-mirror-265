import os
import re

import psycopg2
from dotenv import load_dotenv


def get_env_or_throw(env_var):
    env_val = os.environ.get(env_var, None)
    if env_val is None:
        raise ValueError(f"Env variable - `{env_var}` not found in .env file.")
    return env_val


def parse_exception_message(exception):
    exception_message = str(exception)
    pattern = r"Invalid identifier '(.*?)'"
    matches = re.findall(pattern, exception_message)
    return matches[0].replace("#", "")


def execute_query(cursor, all_dims, missing_dims, table):
    query = f"SELECT {' ,'.join(all_dims)} FROM {table['name']} LIMIT 0"
    try:
        cursor.execute(query)
        # If there's no error, return the final list of missing dimensions
        return missing_dims
    except psycopg2.Error as e:
        missing_columns = parse_exception_message(e)
        if missing_columns:
            # Add missing columns to the list
            missing_dims.append(missing_columns)

            # Try again with the updated set of dimensions
            remaining_dims = [dim for dim in all_dims if dim not in missing_dims]
            return execute_query(cursor, remaining_dims, missing_dims, table)
        else:
            # If the error is not due to missing columns, return the final list of missing dimensions
            return missing_dims


def schema_check(lens_meta):
    # check if env file exist or not
    curr_dir = os.getcwd()
    folder_name = os.path.basename(curr_dir)
    env_file = ".env"
    if os.path.exists(env_file) is False:
        raise FileNotFoundError(
            f"`.env` file not found in folder - `{folder_name}`. Create a `.env` file in folder - `{folder_name}`")

    # check if required env exist or not.
    load_dotenv('.env')
    required_envs = {'LENS2_LOCAL_PG_DB_NAME': None,
                     'LENS2_LOCAL_PG_HOST': None,
                     'LENS2_LOCAL_PG_PORT': None,
                     'LENS2_LOCAL_PG_PASSWORD': None,
                     'LENS2_LOCAL_PG_USER': None}
    for k in required_envs.keys():
        required_envs[k] = get_env_or_throw(k)

    connection = psycopg2.connect(
        dbname=required_envs['LENS2_LOCAL_PG_DB_NAME'],
        user=required_envs['LENS2_LOCAL_PG_USER'],
        password=required_envs['LENS2_LOCAL_PG_PASSWORD'],
        host=required_envs['LENS2_LOCAL_PG_HOST'],
        port=int(required_envs['LENS2_LOCAL_PG_PORT'])
    )
    cur = connection.cursor()

    for table in lens_meta.get('tables', []):
        if table['public']:
            all_dims = []
            for dim in table.get('dimensions', []):
                if dim['public']:
                    name = dim['name']
                    dim_name = name.split('.')[1] if '.' in name else name
                    all_dims.append(dim_name)
            missing_dims = []
            missing_sql_columns = execute_query(cur, all_dims, missing_dims, table)
            if missing_sql_columns:
                raise ValueError(f"Dimension - `{', '.join(missing_sql_columns)} "
                                 f"are not fulfilled by tables sql statement.")
            else:
                print(f"Schema check is completed, All dimensions are fulfilled by SQL statement for table - {table}.")
