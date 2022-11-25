'''
Created on 14.11.2022

@author: Nolan
'''
from flexx import flx


class MyModelManager(flx.JsComponent):

    model = flx.DictProp({}, settable=True)
    fields = flx.ListProp([], settable=True)
    keys = flx.ListProp([], settable=True)
    reacts = flx.ListProp([], settable=True)

    def init(self, data=None):
        super().init()
        if data is not None:
            self.update_model(data)

    @flx.action
    def bind(self, field, key):
        index = len(self.fields)
        self._mutate_fields([field], 'insert', index)
        self._mutate_keys([key], 'insert', index)
        react = flx.reaction(field.user_done)
        print(repr(react))
        self._mutate_reacts([react], 'insert', index)

    @flx.action
    def update_key(self, key, value):
        data = {
            key: value,
        }
        self.update_model(data)

    @flx.action
    def update_model(self, data):
        self._mutate_model(data, 'replace', -1)

    @flx.action
    def update_fields(self):
        for i in range(len(self.fields)):
            self.fields[i].set_text(self.model[self.keys[i]])

    @flx.reaction('model')
    def changed_model(self, *events):
        self.update_fields()

    def dispose(self):
        self.model.clear()
        self.fields.clear()
        self.keys.clear()
        self.reacts.clear()
        super().dispose()


class MyForm(flx.Widget):

    manager = flx.ComponentProp()

    def init(self):
        super().init()

        self._mutate_manager(MyModelManager())

        with flx.FormLayout():
            self.form_no = flx.LineEdit(title='No.:')
            self.form_name = flx.LineEdit(title='Name:')
            self.form_desc = flx.MultiLineEdit(title='Description:')
            with flx.HBox():
                self.reset_btn = flx.Button(text='Reset')
                self.save_btn = flx.Button(text='Save')
            flx.Widget(flex=1)  # Add a spacer

        data = {
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
        }

        self.manager.bind(self.form_no, 'no')
        self.manager.bind(self.form_name, 'name')
        self.manager.bind(self.form_desc, 'desc')

        self.manager.update_model(data)

    @flx.reaction('reset_btn.pointer_click')
    def reset_form(self, *events):
        data = {
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
        }
        self.manager.update_model(data)

    @flx.reaction('save_btn.pointer_click')
    def save_form(self, *events):
        print(repr(self.manager.model))


class MyUI(flx.Widget):

    def init(self):
        super().init()

        with flx.HBox():
            self.form = MyForm(flex=1)


class MyApp(flx.PyComponent):

    def init(self):
        super().init()

        self.ui = MyUI()


if __name__ == '__main__':
    app = flx.App(MyApp)
    app.launch('browser')
    flx.start()
