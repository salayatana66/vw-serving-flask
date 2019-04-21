"""
A simple templating tool for Dockerfiles
"""

import sys
import os

import click
import jinja2
import yaml


@click.group()
def cli():
    """ @Unimplemented """
    pass


@cli.command()
@click.argument("template", required=True, type=str)
@click.option("-y", "--yaml_file", required=True,
              help="Yaml file with keys for template",
              type=str)
def from_yaml(template, yaml_file):
    """
    Fills in template file fields using the
    yaml_file
    """

    temp_path = os.path.expanduser(
        os.path.expandvars(template))
    yml_path = os.path.expanduser(
        os.path.expandvars(yaml_file))

    with open(temp_path, 'r') as tfile:
        temp_jin = jinja2.Template(tfile.read())

    with open(yml_path, 'r') as yfile:
        yml_loaded = yaml.load(yfile, Loader=yaml.BaseLoader)

    temp_rend = temp_jin.render(**yml_loaded)

    sys.stdout.write(temp_rend)
    sys.stdout.flush()


cli.add_command(from_yaml)

if __name__ == '__main__':
    cli()
