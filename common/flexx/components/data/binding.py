from flexx import flx

class DataBinding(flx.JsComponent):

    model = flx.ComponentProp()
    model_key = flx.StringProp('', settable=True)
    
    field = flx.ComponentProp()
    field_prop = flx.StringProp('', settable=True)
    field_key = flx.StringProp('new_value', settable=True)
    
    def init(self, model, model_key, field, field_prop, field_key='new_value'):
        super().init()
        self._mutate_model(model)
        self._mutate_model_key(model_key)
        self._mutate_field(field)
        self._mutate_field_prop(field_prop)
        self._mutate_field_key(field_key)

    @flx.reaction('model.data')
    def on_model(self, *events):
        self.update_field()

    @flx.action
    def update_field(self):
        self.field._mutate(self.field_prop, self.model.data[self.model_key])

    @flx.reaction('!field.user_done', '!field.user_checked', '!field.user_color', '!field.user_selected', '!field.submit')
    def on_field(self, *events):
        self.update_model(events[-1][self.field_key])

    @flx.action
    def update_model(self, value):
        data = {
            self.model_key: value,
        }
        self.model.update_data(data)

    def dispose(self):
        self.model = None
        self.field = None
        super().dispose()