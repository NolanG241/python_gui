'''
Created on 11.11.2022

@author: Nolan
'''
from remodel.connection import pool

pool.configure(
    host='localhost', port=28015, auth_key=None,
    user='admin', password='', db='todo')
