'''
Created on 11.11.2022

@author: Nolan
'''
from flexx import flx

from .frontend.app import App as Frontend

if __name__ == '__main__':
    app = flx.App(Frontend)
    app.launch('browser')
    flx.start()
