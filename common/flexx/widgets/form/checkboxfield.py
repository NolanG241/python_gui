from flexx import flx

class CheckBoxField(flx.CheckBox):

    @flx.action
    def field_value(self, value):
        self.set_checked(value)

    @flx.reaction('checked')
    def on_field(self, *events):
        for ev in events:
            self.field_changed(ev)

    @flx.emitter
    def field_changed(self, ev):
        return ev



class TestApp(flx.Widget):

    def init(self):
        super().init()

        with flx.VBox():
            self.field1 = CheckBoxField(text='Text')
            self.change_btn = flx.Button(text='Change')
    
    @flx.reaction('field1.field_changed')
    def field_changed(self, *events):
        for ev in events:
            print(ev['old_value'])
            print(ev['new_value'])

    @flx.reaction('change_btn.pointer_click')
    def on_change_btn(self, *events):
        self.field1.field_value(False)


if __name__ == '__main__':
    app = flx.App(TestApp)
    app.launch('browser')
    flx.start()        