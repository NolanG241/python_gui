'''
Created on 14.11.2022

@author: Nolan
'''
from flexx import flx


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
                self.update_btn = flx.Button(text='Update')
                self.save_btn = flx.Button(text='Save')
                self.change_btn = flx.Button(text='Change')
            flx.Widget(flex=1)  # Add a spacer

        self.bind_field(self.form_dyn, self.data_model, 'dyn')

        self.update_model(data)

    def bind_field(self, field, model, model_key):
        field_name = field.__name__
        model_name = model.__name__

        ftm_name = '_'+field_name+'_to_model'
        mtfa_name = '_model_to_'+field_name+'_action'
        mtf_name = '_model_to_'+field_name

        @flx.reaction(field_name+'.user_done')
        def ftm(self, *events):
            data = {
                model_key: events[-1]['new_value']
            }
            self.update_model(data)
        setattr(self, ftm_name, ftm)

        @flx.action
        def mtfa(self):
            field.set_text(model[model_key])
        setattr(self, mtfa_name, mtfa)

        @flx.reaction(model_name)
        def mtf(self, *events):
            getattr(self, mtfa_name, None)()
        setattr(self, mtf_name, mtf)

    @flx.reaction('form_no.user_done')
    def update_no(self, *events):
        data = {
            'no': events[-1]['new_value']
        }
        self.update_model(data)

    @flx.reaction('form_name.user_done')
    def update_name(self, *events):
        data = {
            'name': events[-1]['new_value']
        }
        self.update_model(data)

    @flx.reaction('form_desc.user_done')
    def update_desc(self, *events):
        data = {
            'desc': events[-1]['new_value']
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

    @flx.reaction('update_btn.pointer_click')
    def update_form(self, *events):
        self.model_to_form()

    @flx.reaction('change_btn.pointer_click')
    def change_model(self, *events):
        data = {
            'no': '4'
        }
        self.update_model(data)

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

        data = {
            'no': '123',
            'name': '123',
            'desc': '123',
        }

        with flx.HBox():
            self.form = MyForm(data, flex=1)


class MyApp(flx.PyComponent):

    def init(self):
        super().init()

        self.ui = MyUI()


if __name__ == '__main__':
    app = flx.App(MyApp)
    app.launch('browser')
    flx.start()
