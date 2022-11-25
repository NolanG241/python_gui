'''
Created on 16.11.2022

@author: Nolan
'''
from flexx import flx

class TitleBar(flx.HBox):

    title_text = flx.StringProp('', settable=True)

    can_close = flx.BoolProp(True, settable=True)
    can_minimize = flx.BoolProp(False, settable=True)
    can_maximize = flx.BoolProp(False, settable=True)

    @flx.emitter
    def event_close(self):
        return dict()

    @flx.emitter
    def event_minimize(self):
        return dict()

    @flx.emitter
    def event_maximize(self):
        return dict()

    def init(
            self, title='', can_close=True, can_minimize=False,
            can_maximize=False):
        super().init()

        self.title_wgt = flx.Label(text=lambda: self.title_text, flex=1)
        self.min_btn = flx.Button(text='v', flex=0)
        self.max_btn = flx.Button(text='^', flex=0)
        self.close_btn = flx.Button(text='X', flex=0)

        self._mutate_title_text(title)
        self._mutate_can_close(can_close)
        self._mutate_can_minimize(can_minimize)
        self._mutate_can_maximize(can_maximize)

    @flx.reaction('can_close')
    def on_can_close(self, *events):
        self.close_btn.set_disabled(not self.can_close)

    @flx.reaction('can_minimize')
    def on_can_minimize(self, *events):
        self.min_btn.set_disabled(not self.can_minimize)

    @flx.reaction('can_maximize')
    def on_can_maximize(self, *events):
        self.max_btn.set_disabled(not self.can_maximize)

    @flx.reaction('close_btn.pointer_click')
    def on_close(self, *events):
        self.event_close()

    @flx.reaction('min_btn.pointer_click')
    def on_minimize(self, *events):
        self.event_minimize()

    @flx.reaction('max_btn.pointer_click')
    def on_maximize(self, *events):
        self.event_maximize()