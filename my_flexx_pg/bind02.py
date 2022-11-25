'''
Created on 14.11.2022

@author: Nolan
'''
from flexx import flx


class MyBinder(flx.JsComponent):

    def init(self, model, key, field):
        self.model = model
        self.field = field
        self.key = key

    @flx.reaction('field.user_done')
    def _field_changed(self, *events):
        data = {
            self.key: events[-1]['new_value']
        }
        self._update_model(data)

    @flx.reaction('model')
    def _model_changed(self, *events):
        self._update_field()

    @flx.action
    def _update_model(self, data):
        if data is None:
            return
        self._mutate(self.model, data, 'replace', -1)

    @flx.action
    def _update_field(self):
        self.field.set_text(self.model[self.key])


class MyForm(flx.Widget):

    data_model = flx.DictProp(
        {'no': '1', 'name': 'Test', 'desc': 'Desc', 'dyn': 'Dyn'})

    def init(self, data=None):
        super().init()

        with flx.FormLayout():
            self.form_no = flx.LineEdit(title='No.:')
            self.form_name = flx.LineEdit(title='Name:')
            self.form_desc = flx.MultiLineEdit(title='Description:')
            self.form_dyn = flx.LineEdit(title='Dynamic:')
            with flx.HBox():
                self.save_btn = flx.Button(text='Save')
            flx.Widget(flex=1)  # Add a spacer

        MyBinder(self.data_model, 'name', self.form_name)

        self.update_model(data)

    @flx.reaction('form_no.user_done')
    def update_no(self, *events):
        data = {
            'no': events[-1]['new_value']
        }
        self.update_model(data)

    @flx.action
    def update_model(self, data):
        if data is None:
            return
        self._mutate_data_model(data, 'replace', -1)

    @flx.action
    def model_to_form(self):
        self.form_no.set_text(self.data_model['no'])
        self.form_name.set_text(self.data_model['name'])
        self.form_desc.set_text(self.data_model['desc'])

    @flx.reaction('save_btn.pointer_click')
    def save_form(self, *events):
        print(repr(self.data_model))

    @flx.reaction('data_model')
    def print_model(self, *events):
        print(repr(self.data_model))
        self.model_to_form()


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
