from flexx import flx

from .binding import DataBinding

class DataManager(flx.JsComponent):

    bindings = flx.ListProp([], settable=True)

    def init(self):
        super().init()

    @flx.action
    def bind(self, model, key, field, prop):
        with self:
            bd = DataBinding(model, key, field, prop)
        self._mutate_bindings([bd], 'insert', len(self.bindings))

    @flx.action
    def clear(self):
        self._mutate_bindings([])

    def dispose(self):
        for entry in self.bindings:
            entry.dispose()
        self.bindings.clear()
        super().dispose()