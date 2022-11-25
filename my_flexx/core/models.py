'''
Created on 11.11.2022

@author: Nolan
'''
from remodel.models import Model

from . import db

from remodel.object_handler import ObjectHandler, ObjectSet


class TodoObjectHandler(ObjectHandler):

    def max(self):
        return ObjectSet(self, self.query.max({'index': 'nr'}))


class Todo(Model):

    object_handler = TodoObjectHandler

    pass
