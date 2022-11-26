'''
Created on 16.11.2022

@author: Nolan
'''
from flexx import flx

class ShowHideMixin:

    hidden = flx.BoolProp(False)

    @flx.reaction('hidden')
    def __hidden_changed(self, *events):
        self.apply_style(f'display:{"none" if self.hidden else "unset"}')
    
    @flx.action
    def show(self):
        self._mutate_hidden(False)
    
    @flx.action
    def hide(self):
        self._mutate_hidden(True)


class ToolBar(flx.HBox):

    num_bars = flx.IntProp(1, settable=True)
    bar_list = flx.ListProp([], settable=True)

    def init(self):
        super().init()
        
        with self:
            bar = flx.HBox(flex=0)
            self._mutate('bar_list', [bar], 'insert', len(self.bar_list))
            flx.Widget(flex=1)

            for i in range(1, self.num_bars):
                if i > 1:
                    flx.Widget(flex=1)
                bar = flx.HBox(flex=0)
                self._mutate('bar_list', [bar], 'insert', len(self.bar_list))
    
    @flx.action
    def add_item(self, widget, idx=0):
        idx = min(max(idx, 0), len(self.bar_list)-1)
        widget.set_parent(self.bar_list[idx])
    
    @flx.action
    def remove_item(self, widget):
        for bar in self.bar_list:
            if widget in bar.children:
                widget.set_parent(None)
                break

class CaptionBar(flx.HBox):

    def init(self):
        super().init()

        with self:
            self.iconbar = flx.HBox(flex=0)
            self.titlebar = flx.HBox(flex=1)
            self.buttonbar = flx.HBox(flex=0)
    
    @flx.action
    def add_icon(self, widget):
        widget.set_parent(self.iconbar)
    
    @flx.action
    def add_title(self, widget):
        widget.set_parent(self.titlebar)
    
    @flx.action
    def add_button(self, widget):
        widget.set_parent(self.buttonbar)
    
    @flx.action
    def remove_item(self, widget):
        found_icon = widget in self.iconbar
        found_title = widget in self.titlebar
        found_button = widget in self.buttonbar
        if found_icon or found_title or found_button:
            widget.set_parent(None)



class Desktop(flx.PinboardLayout):

    def init(self):
        super().init()

    @flx.action
    def add_item(self, widget, left=None, top=None):
        if left is None:
            left = '50%'
        if top is None:
            top = '50%'
        widget.set_parent(self)
        widget.apply_style(f'left:{left};top:{top};')
    
    @flx.action
    def remove_item(self, widget):
        if widget in self.children:
            widget.set_parent(None)

class Window(flx.Widget):

    CSS = """
        .flx-Window {
            background-color: #ffffff;
        }
    """

    hidden = flx.BoolProp(True)

    DEFAULT_MIN_SIZE = 300, 0

    def init(self, content, title=''):
        super().init()

        with flx.VBox(flex=0):
            self.captionbar = CaptionBar(flex=0, style='border: 1px solid #ff0000;')
            self.contentpane = flx.HBox(flex=0)
            self.statusbar = ToolBar(num_bars=1, flex=0)
        
        self.caption_icon = flx.Button(text='I')
        self.caption_title = flx.Label(text=title, flex=1)
        self.close_btn = flx.Button(text='X')

        self.captionbar.add_icon(self.caption_icon)
        self.captionbar.add_title(self.caption_title)
        self.captionbar.add_button(self.close_btn)

        status = flx.Label(text='Status')
        self.statusbar.add_item(status)

        self.content = content
        self.content.set_parent(self.contentpane)
    
    @flx.reaction('close_btn.pointer_click')
    def on_close(self, *events):
        self.dispose()
    
    @flx.reaction('caption_title.pointer_down', 'caption_title.pointer_move')
    def on_move(self, *events):
        pos = events[-1]['page_pos']
        pos_x = pos[0] - self.size[0] // 2
        pos_y = pos[1] - self.captionbar.size[1] * 2
        self.apply_style(f'left:{pos_x}px;top:{pos_y}px;')
    
    @flx.reaction('hidden')
    def __hidden_changed(self, *events):
        self.apply_style(f'display:{"none" if self.hidden else "unset"};')
    
    @flx.action
    def show(self):
        self._mutate_hidden(False)
    
    @flx.action
    def hide(self):
        self._mutate_hidden(True)
    
    def dispose(self):
        self.content = None
        super().dispose()

class UI(flx.Widget):

    def init(self):
        super().init()

        with flx.VBox():
            self.toolbar = ToolBar(num_bars=3, flex=0)
            self.desktop = Desktop(flex=1)
            self.taskbar = ToolBar(flex=0)
        
        self.app1_btn = flx.Button(text='App 1')
        self.app2_btn = flx.Button(text='App 2')

        self.toolbar.add_item(self.app1_btn)
        self.toolbar.add_item(self.app2_btn)
        
        self.toolbar.add_item(flx.Label(text='Title'), 1)
        self.toolbar.add_item(flx.Button(text='Logout'), 2)

        self.taskbar.add_item(flx.Label(text='TaskBar'))

        #self.btn2 = flx.Button(text='2')
        #self.btn3 = flx.Button(text='3')
    
    @flx.reaction('app1_btn.pointer_click')
    def show_app1(self, *events):
        with self:
            content = flx.Label(text='Content 1')
            wdn = Window(content, 'App 1', flex=0, style='border: 1px solid #00ff00;')
        self.desktop.add_item(wdn)
        wdn.show()
    
    @flx.reaction('app2_btn.pointer_click')
    def show_app2(self, *events):
        with self:
            content = flx.Label(text='Content 2')
            wdn = Window(content, 'App 2', flex=0, style='border: 1px solid #0000ff;')
        self.desktop.add_item(wdn)
        wdn.show()


class App(flx.PyComponent):

    def init(self):
        super().init()

        self.ui = UI()
