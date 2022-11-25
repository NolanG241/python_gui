'''
Created on 11.11.2022

@author: Nolan
'''
import random

from flexx import flx


class MyDisplay(flx.Widget):

    def init(self):
        super().init()

        with flx.HBox():
            with flx.VBox():
                self.but1 = flx.Button(text='Center')

    @flx.reaction('but1.pointer_click')
    def but1_clicked(self, *events):
        self.root.database.set_command(self.but1.text)

    @flx.reaction('root.database.result')
    def get_result(self, *events):
        print(self.root.database.result)
        self.but1.set_text(str(self.root.database.result))


class MyDB(flx.PyComponent):
    # triggers the query
    command = flx.StringProp(settable=True)
    # result back to form
    result = flx.StringProp(settable=True)

    @flx.action
    def update_result(self, result):
        self._mutate_result(result)

    @flx.reaction('command')
    def do_query(self, *events):
        print(self.command)
        result = ''.join(random.choices(['A', 'B', 'C', 'D'], k=5))
        self.update_result(result)


class MyApp(flx.PyComponent):

    database = flx.ComponentProp()

    def init(self):
        self.ui = MyDisplay()
        self._mutate_database(MyDB())


if __name__ == '__main__':
    app = flx.App(MyApp)
    app.launch('browser')
    flx.start()
