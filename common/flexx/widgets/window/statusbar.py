'''
Created on 16.11.2022

@author: Nolan
'''
from flexx import flx

class StatusBar(flx.HBox):

    status_text = flx.StringProp('', settable=True)

    def init(self):
        super().init()

        self.status_wgt = flx.Label(text=lambda: self.status_text, flex=0)
        flx.Widget(flex=1)  # spacer

    @flx.action
    def clear(self):
        self._mutate_status_text('')