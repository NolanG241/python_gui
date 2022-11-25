'''
Created on 11.11.2022

@author: Nolan
'''
from remodel.errors import OperationError

from flexx import flx

from .models import Todo


class TodoModel(flx.PyComponent):

    """
    def get_todo(self, nr):
        return Todo.get(nr=nr)

    def add_todo(self, name, nr=None):
        todo = None if nr is None else self.get_todo(nr)
        if todo is not None:
            return False
        last_todo = Todo.max()

    def del_todo(self, nr):
        todo = self.get_todo(nr)
        if todo is None:
            return False
        try:
            todo.delete()
        except OperationError:
            return False
        return True

    def upd_todo(self, nr, name=None):
        todo = self.get_todo(nr)
        if todo is None:
            return False
        if name is not None:
            todo['name'] = name
        try:
            todo.save()
        except OperationError:
            return False
        return True
    """

    def get_list(self):
        return Todo.all()


class Store(flx.PyComponent):
    pass


class Service(flx.PyComponent):

    store = flx.ComponentProp()

    def init(self):

        # Create our store instance
        self._mutate_store(Store())
