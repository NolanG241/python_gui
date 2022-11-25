from flexx import flx

class LabelField(flx.Label):
    
    data = flx.StringProp('')
    
    def init(self):
        super().init()
        self._mutate_data(self.text)

    @flx.action
    def set_data(self, value):
        self._mutate_data(value)

    @flx.reaction('text')
    def on_field(self, *events):
        self.set_data(self.text)

    @flx.reaction('data')
    def on_data(self, *events):
        self.set_text(self.data)

class LabelHtmlField(flx.Label):

    @flx.action
    def field_value(self, value):
        self.set_html(value)

    @flx.reaction('html')
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
            self.field1 = LabelField(text='Text')
            self.field2 = LabelHtmlField(html='Text')
            self.change_btn = flx.Button(text='Change')
    
    @flx.reaction('field1.data','field2.field_changed')
    def field_changed(self, *events):
        for ev in events:
            print(ev['old_value'])
            print(ev['new_value'])

    @flx.reaction('change_btn.pointer_click')
    def on_change_btn(self, *events):
        self.field1.set_data('Changed')
        self.field2.field_value('<b>Changed</b>')


if __name__ == '__main__':
    app = flx.App(TestApp)
    app.launch('browser')
    flx.start()