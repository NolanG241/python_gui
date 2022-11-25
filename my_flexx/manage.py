'''
Created on 11.11.2022

@author: Nolan
'''
import click

from remodel.helpers import create_tables, create_indexes, drop_tables

from .core import models


@click.group()
def cli():
    pass


@cli.group()
def db():
    pass


@db.command('tables', help='Create database tables.')
def db_tables():
    # Creates all database tables defined by models
    create_tables()


@db.command('indexes', help='Create database indices.')
def db_indexes():
    # Creates all table indexes based on model relations
    create_indexes()


@db.command('init', help='Create database tables and indices.')
def db_init():
    db_tables()
    db_indexes()


@db.command('drop', help='Drop all database tables.')
def db_drop():
    drop_tables()


if __name__ == '__main__':
    cli()
