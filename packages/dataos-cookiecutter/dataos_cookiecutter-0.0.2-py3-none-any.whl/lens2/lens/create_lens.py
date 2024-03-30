import os
import shutil

import pkg_resources

from lens2.lens.env_vars_mapping import env_var_mappings


def create_project_structure(args):
    # Extract folder names from command line arguments
    lens_name = args.name
    source_type = args.source_type
    parent_dir = args.parent_dir if args.parent_dir else os.getcwd()

    # Create main directory
    main_dir = os.path.join(parent_dir, lens_name)

    # Check if the directory already exists
    if os.path.exists(main_dir):
        overwrite = input(
            f"The directory '{main_dir}' already exists. Do you want to overwrite it? (Y/n): ").strip().lower() or 'n'
        if overwrite != 'y':
            print("Aborted.")
            return

        # Remove the existing directory and its contents
        try:
            shutil.rmtree(main_dir)
        except OSError as e:
            print(f"Error removing existing directory '{main_dir}': {e}")
            return

    try:
        os.makedirs(main_dir)
    except OSError as e:
        print(f"Error creating main directory '{main_dir}': {e}")
        return

    # Create model directory
    model_dir = os.path.join(main_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    # Create subdirectories within model directory
    subdirectories = ['sql', 'tables', 'views']
    for subdir in subdirectories:
        temp_path = os.path.join(model_dir, subdir)
        os.makedirs(temp_path, exist_ok=True)
        if subdir == 'sql':
            shutil.copyfile(pkg_resources.resource_filename('lens2', f'lens/resources/{subdir}_sample.sql'),
                            os.path.join(temp_path, f"{subdir}_sample.sql"))
        else:
            shutil.copyfile(pkg_resources.resource_filename('lens2', f'lens/resources/{subdir}_sample.yaml'),
                            os.path.join(temp_path, f"{subdir}_sample.yaml"))

    # Copy docker-compose.yaml file, makefile and env.env
    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/docker-compose.yaml'),
                    os.path.join(main_dir, 'docker-compose.yaml'))

    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/Makefile'),
                    os.path.join(main_dir, 'Makefile'))

    shutil.copyfile(pkg_resources.resource_filename('lens2', 'lens/resources/env.env'), os.path.join(main_dir, '.env'))

    if source_type in env_var_mappings.keys():
        env_vars = env_var_mappings[source_type.lower()]
        defaults = env_var_mappings['default']
        pg_configs = env_var_mappings['lens_pg_config']
        defaults['LENS2_NAME'] = lens_name
        env_vars.update(defaults)
        env_vars.update(pg_configs)

        with open(f"{main_dir}/.env", 'a+') as f:
            f.write("\n")
            for key, value in env_vars.items():
                if key == 'LENS2_NAME':
                    f.write(f"\n #Lens Configs\n")
                    f.write(f"{key}={value}\n")
                elif key == 'LENS2_LOCAL_PG_DB_NAME':
                    f.write(f"\n #Lens local postgres config\n")
                    f.write(f"{key}={value}\n")
                else:
                    f.write(f"{key}={value}\n")


def add_subparser(subparsers):
    parser = subparsers.add_parser("lens")
    parser.set_defaults(func=execute_lens)
    parser.add_argument("action", choices=["create"], help="Create lens yaml")
    parser.add_argument("-n", "--name", required=True, help="Name of the lens")
    parser.add_argument("-s", "--source-type", required=True, help="Type of the source (e.g., postgres, mysql)")
    parser.add_argument("-p", "--parent-dir", help="Parent directory where the lens directory will be created")


def execute_lens(args):
    if args.action == "create":
        create_project_structure(args)
