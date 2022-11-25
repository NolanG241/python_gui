from flexx import flx

class TextField(flx.LineEdit):

    @flx.action
    def field_value(self, value):
        self.set_text(value)

    @flx.reaction('user_done', 'submit')
    def on_field(self, *events):
        for ev in events:
            self.field_changed(ev)

    @flx.emitter
    def field_changed(self, ev):
        return ev


class TextAreaField(flx.MultiLineEdit):

    @flx.action
    def field_value(self, value):
        self.set_text(value)

    @flx.reaction('user_done')
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
            self.field1 = TextField(text='Text')
            self.field2 = TextAreaField(text='Text')
            self.change_btn = flx.Button(text='Change')
    
    @flx.reaction('field1.field_changed','field2.field_changed')
    def field_changed(self, *events):
        for ev in events:
            print(ev['old_value'])
            print(ev['new_value'])

    @flx.reaction('change_btn.pointer_click')
    def on_change_btn(self, *events):
        self.field1.field_value('Changed')
        self.field2.field_value('<b>Changed</b>')


if __name__ == '__main__':
    app = flx.App(TestApp)
    app.launch('browser')
    flx.start()