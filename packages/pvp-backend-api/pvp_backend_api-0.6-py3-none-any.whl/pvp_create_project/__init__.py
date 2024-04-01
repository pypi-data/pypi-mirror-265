
import click
import os
from django.core.management import call_command


@click.command()
@click.option('--project_name', '-n', default='.', help='project name')
def cli(project_name):
    # Ensure project_name is a valid Python module name
    project_name_complete=project_name + '_' +'PVP'
    if not project_name_complete.isidentifier():
        raise ValueError("Invalid project name. Please provide a valid Python module name.")

    # Create the Django project directory
    os.makedirs(project_name_complete, exist_ok=True)
    # Call Django's startproject management command to create the project
    call_command('startproject', project_name_complete, directory=project_name_complete)
    # Change to the project directory
    os.chdir(project_name_complete)
    # Call Django's startapp management command to create the app
    call_command('startapp', 'application')
    # Make migrations


if __name__ == "__main__":
    cli()




