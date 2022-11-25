'''
Created on 16.11.2022

@author: Nolan
'''
from flexx import flx

from .titlebar import TitleBar
from .statusbar import StatusBar

class Window(flx.VBox):

    def init(
            self, content, title='', can_close=True, can_minimize=False,
            can_maximize=False):
        super().init()

        self.titlebar = TitleBar(title, can_close, can_minimize, can_maximize, flex=0)
        self.content = flx.HBox(flex=0)
        flx.Widget(flex=1)  # spacer
        self.statusbar = StatusBar(flex=0)

        content.set_parent(self.content)

    @flx.reaction('titlebar.event_close')
    def on_close(self, *events):
        pass

    @flx.reaction('titlebar.event_minimize')
    def on_minimize(self, *events):
        pass

    @flx.reaction('titlebar.event_maximize')
    def on_maximize(self, *events):
        pass

    @flx.action
    def status_text(self, text):
        self.statusbar.set_status_text(text)

    @flx.action
    def clear_status(self):
        self.statusbar.clear()