#!/usr/bin/env python
# coding: utf-8

import pyglet
from pyglet.gl import *


class MyWindow(pyglet.window.Window):
    def on_key_press(self, symbol, modifiers):
        sstr = pyglet.window.key.symbol_string(symbol)
        print("on_key_press", locals())
    def on_key_release(self, symbol, modifiers):
        sstr = pyglet.window.key.symbol_string(symbol)
        print("on_key_release", locals())
    def on_text(self, text):
        print("on_text", locals())
    def on_mouse_motion(self, x, y, dx, dy):
        print("on_mouse_motion", locals())
    def on_mouse_press(self, x, y, button, modifiers):
        print("on_mouse_press",locals())
    def on_mouse_release(self, x, y, button, modifiers):
        print("on_mouse_release",locals())
    def on_mouse_motion(self, x, y, dx, dy):
        print("on_mouse_motion" ,locals())

    def on_draw(self):
        glClearColor(0.3, 0.7, 0.4, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        return

def run():
    '''
                    width=None,
                     height=None,
                     caption=None,
                     resizable=False,
                     style=WINDOW_STYLE_DEFAULT,
                     fullscreen=False,
                     visible=True,
                     vsync=True,
                     file_drops=False,
                     display=None,
                     screen=None,
                     config=None,
                     context=None,
                     mode=None):
    '''
    w = MyWindow(caption="Pyweek34 by yarolig", resizable=True)
    pyglet.app.run()
    print("end.")