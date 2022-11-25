'''
Created on 13.11.2022

@author: Nolan
'''
from flexx import flx


class MyTopBar(flx.HBox):

    title_text = flx.StringProp('', settable=True)

    def init(self, title=''):
        super().init()
        self.title_wgt = flx.Label(text=lambda: self.title_text, flex=1)
        self.close_btn = flx.Button(text='X', flex=0)

        self._mutate_title_text(title)

    @flx.reaction('close_btn.pointer_click')
    def on_close(self, *events):
        self.event_close()

    @flx.emitter
    def event_close(self):
        return dict()


class MyStatusBar(flx.HBox):

    status_text = flx.StringProp('', settable=True)

    def init(self):
        super().init()
        self.status_wgt = flx.Label(text=lambda: self.status_text, flex=0)
        flx.Widget(flex=1)  # spacer

    @flx.action
    def clear(self):
        self._mutate_status_text('')


class MyWindow(flx.VBox):

    def init(self, content, title=''):
        super().init()

        self.topbar = MyTopBar(title, flex=0)
        self.content = flx.HBox(flex=0)
        flx.Widget(flex=1)  # spacer
        self.statusbar = MyStatusBar(flex=0)

        content.set_parent(self.content)

    @flx.reaction('topbar.event_close')
    def handle_close(self, *events):
        self.statusbar.set_status_text('Closed.')

    @flx.action
    def clear_status(self):
        self.statusbar.clear()


class MyFormWindow(flx.Widget):

    def init(self, title=''):
        super().init()

        with flx.VBox() as content:
            self.clear_btn = flx.Button(text='Clear')

        self.base_window = MyWindow(content, title)

    @flx.reaction('clear_btn.pointer_click')
    def clear_status(self, *events):
        self.base_window.clear_status()


class MyUIOld(flx.Widget):

    def init(self):
        super().init()
        with flx.VBox(flex=0):
            self.topbar = MyTopBar('TopBar2', flex=0)
            with flx.HBox(flex=1):
                self.clear_btn = flx.Button(text='Clear')
            self.statusbar = MyStatusBar(flex=0)

    @flx.reaction('clear_btn.pointer_click')
    def clear_status(self, *events):
        self.statusbar.clear()

    @flx.reaction('topbar.event_close')
    def print_close(self, *events):
        self.statusbar.status('Closed.')


class MyUI(flx.Widget):

    def init(self):
        super().init()

        with flx.HBox():
            self.form_window1 = MyFormWindow('Form Window1', flex=1)
            self.form_window2 = MyFormWindow('Form Window2', flex=1)


class MyApp(flx.PyComponent):

    def init(self):
        self.ui = MyUI()


if __name__ == '__main__':
    app = flx.App(MyApp)
    app.launch('browser')
    flx.start()
