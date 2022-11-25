'''
Created on 11.11.2022

@author: Nolan
'''
from flexx import flx

from .model import DataModel
from .manager import DataManager

class App(flx.PyComponent):

    model = flx.ComponentProp()
    manager = flx.ComponentProp()

    def init(self):
        super().init()

        self._mutate_model(DataModel())
        self._mutate_manager(DataManager())

        with flx.FormLayout():
            self.form_label = flx.Label(title='Label:', text='Text')
            self.form_no = flx.LineEdit(title='No.:')
            self.form_text = flx.LineEdit(title='LineEdit:')
            self.form_area = flx.MultiLineEdit(title='MultiLineEdit:')
            self.form_check = flx.CheckBox(title='Checkbox:')
            self.form_combo = flx.ComboBox(title='Combo:', options=[('-1', 'Please select'),('0', 'First'),('1', 'Second')])
            self.form_slider = flx.Slider(title='Slider:', min=0, max=100)
            with flx.HBox():
                self.from_radio1 = flx.RadioButton(text='First')
                self.from_radio2 = flx.RadioButton(text='Second')


            with flx.HBox():
                self.reset_btn = flx.Button(text='Reset')
                self.save_btn = flx.Button(text='Save')
            flx.Widget(flex=1)  # Add a spacer
        
        self.manager.bind(self.model, 'label', self.form_label, 'text')
        self.manager.bind(self.model, 'no', self.form_no, 'text')
        self.manager.bind(self.model, 'name', self.form_text, 'text')
        self.manager.bind(self.model, 'desc', self.form_area, 'text')
        self.manager.bind(self.model, 'check', self.form_check, 'checked')
        self.manager.bind(self.model, 'combo', self.form_combo, 'selected_key')
        self.manager.bind(self.model, 'slider', self.form_slider, 'value')

        data = {
            'label': 'First Label',
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
            'check': True,
            'combo': '0',
            'slider': 10,
            'radio': 0,
        }

        self.model.update_data(data)
    
    @flx.reaction('reset_btn.pointer_click')
    def reset_form(self, *events):
        data = {
            'label': 'Label',
            'no': '1',
            'name': 'Name',
            'desc': 'Desc',
            'check': True,
            'combo': '0',
            'slider': 10,
            'radio': 0,
        }
        self.model.update_data(data)

    @flx.reaction('save_btn.pointer_click')
    def save_form(self, *events):
        print(repr(self.model.data))

    def dispose(self):
        self.model.dispose()
        self.manager.dispose()
        super().dispose()


if __name__ == '__main__':
    app = flx.App(App)
    app.launch('browser')
    flx.start()