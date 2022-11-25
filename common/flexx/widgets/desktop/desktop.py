'''
Created on 16.11.2022

@author: Nolan
'''
from flexx import flx


class Desktop(flx.HBox):

    def init(self):
        super().init()

        flx.Label(text='Desktop')
