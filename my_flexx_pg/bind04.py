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


class DataBinding(flx.JsComponent):

    model = flx.ComponentProp()
    field = flx.ComponentProp()
    key = flx.StringProp('', settable=True)
    on_done = flx.BoolProp(False, settable=True)

    def init(self, model, key, field, on_done=False):
        super().init()
        self._mutate_model(model)
        self._mutate_field(field)
        self._mutate_key(key)
        self._mutate_on_done(on_done)

    @flx.reaction('model.data')
    def on_model(self, *events):
        self.update_field()

    @flx.action
    def update_field(self):
        self.field.set_text(self.model.data[self.key])

    @flx.reaction('field.user_done')
    def on_field_done(self, *events):
        if self.on_done:
            self.update_model(events[-1]['new_value'])

    @flx.reaction('field.user_text')
    def on_field_text(self, *events):
        if not self.on_done:
            self.update_model(events[-1]['new_value'])

    @flx.action
    def update_model(self, value):
        data = {
            self.key: value,
        }
        self.model.update_data(data)

    def dispose(self):
        self.model = None
        self.field = None
        super().dispose()


class DataManager(flx.JsComponent):

    bindings = flx.ListProp([], settable=True)

    def init(self, model=None):
        super().init()
        # self._mutate_model(model)

    @flx.action
    def bind(self, model, key, field, on_done=False):
        bd = DataBinding(model, key, field, on_done)
        self._mutate_bindings([bd], 'insert', len(self.bindings))

    @flx.action
    def clear(self):
        self._mutate_bindings([])

    def dispose(self):
        for entry in self.bindings:
            entry.dispose()
        self.bindings.clear()
        super().dispose()


class Form(flx.Widget):

    model = flx.ComponentProp()
    bindings = flx.ListProp([], settable=True)

    def init(self):
        super().init()

        self._mutate_model(DataModel())

        with flx.FormLayout():
            self.form_no = flx.LineEdit(title='No.:')
            self.form_name = flx.LineEdit(title='Name:')
            self.form_desc = flx.MultiLineEdit(title='Description:')
            with flx.HBox():
                self.reset_btn = flx.Button(text='Reset')
                self.save_btn = flx.Button(text='Save')
            flx.Widget(flex=1)  # Add a spacer

        self.bind(self.model, 'no', self.form_no, True)
        self.bind(self.model, 'name', self.form_name, True)
        self.bind(self.model, 'desc', self.form_desc, True)

        data = {
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
        }

        self.model.update_data(data)

    @flx.action
    def bind(self, model, key, field, on_done=False):
        bd = DataBinding(model, key, field, on_done)
        self._mutate_bindings([bd], 'insert', len(self.bindings))

    @flx.reaction('reset_btn.pointer_click')
    def reset_form(self, *events):
        data = {
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
        }
        self.model.update_data(data)

    @flx.reaction('save_btn.pointer_click')
    def save_form(self, *events):
        print(repr(self.model.data))

    def dispose(self):
        for entry in self.bindings:
            entry.dispose()
        self.bindings.clear()
        super().dispose()


class UI(flx.Widget):

    def init(self):
        super().init()

        with flx.HBox():
            self.form = Form(flex=1)


class App(flx.PyComponent):

    def init(self):
        super().init()

        self.ui = UI()


if __name__ == '__main__':
    app = flx.App(App)
    app.launch('browser')
    flx.start()
