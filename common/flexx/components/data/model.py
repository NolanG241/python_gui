'''
Created on 14.11.2022

@author: Nolan
'''
from flexx import flx


class DataModel(flx.JsComponent):

    data = flx.DictProp({}, settable=True)

    def init(self):
        super().init()

    @flx.action
    def update_data(self, data):
        self._mutate_data(data, 'replace', -1)

    def dispose(self):
        self.data.clear()
        super().dispose()