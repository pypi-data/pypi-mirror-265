from setuptools import setup, find_namespace_packages, find_packages

setup(
    name='lens2',
    version='0.0.2',
    install_requires=[
        'python-dotenv==1.0.1',
        'PyYAML==6.0.1',
        'psycopg2-binary==2.9.9',
        'sql_metadata==2.10.0'
    ],
    package_data={'lens2': ['lens/resources/*']},
    packages=find_namespace_packages(include=["lens2*"]),
)

