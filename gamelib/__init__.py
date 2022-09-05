#!/usr/bin/env python
# coding: utf-8

import pyglet
from pyglet.gl import *

def load_texture(name):
    return pyglet.resource.texture(name)

class MyWindow(pyglet.window.Window):
    inited = False
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
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print("on_mouse_scroll" ,locals())

    def init(self):
        if self.inited:
            return
        self.inited = True
        #pyglet.resource.add_font('data/fonts/MeromSans-Regular.ttf')
        pyglet.font.add_file('data/fonts/MeromSans-Regular.ttf')


        pyglet.font.load('Merom Sans')
        self.backgroundTex = load_texture('data/statue.png')

        self.fps_label = pyglet.text.Label('FPS',
                          font_name='Merom Sans',
                          font_size=24)

        class Button:
            x=0
            y=0
            text = 0
            def __init__(self,x,y,text):
                self.label = pyglet.text.Label(text,
                          font_name='Merom Sans',
                          font_size=24)
                self.x=x
                self.y=y
                self.text=text
            def draw(self):
                self.label.x=self.x
                self.label.y=self.y
                self.label.text=self.text
                self.label.draw()

        class Menu:
            def draw(self):
                for i in dir(self):
                    if i.startswith('_'):
                        continue
                    print(i)
                    try:
                        if isinstance(getattr(self, i), Button):
                            getattr(self, i).draw()
                    except Exception as e:
                        print('error', e)
        x = 80
        y = 150
        dy = 34
        self.main_menu = Menu()
        self.main_menu.new_game = Button(x, y, 'New Game');        y -= dy
        self.main_menu.optinos = Button(x, y, 'Options');        y -= dy
        self.main_menu.about = Button(x, y, 'About');        y -= dy
        self.main_menu.exit = Button(x, y, 'Exit');        y -= dy

    def draw_background(self):

        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.backgroundTex.id)
        glBegin(GL_TRIANGLES)

        glTexCoord2f(0, 0)
        glVertex2f(0, 0)

        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0);

        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)

        glTexCoord2f(0, 0)
        glVertex2f(0, 0)

        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height);

        glTexCoord2f(0, 1)
        glVertex2f(0, self.height);

        glEnd()

    def update(self, dt):
        pass

    def on_draw(self):
        self.init()
        #print('on_draw')
        glClearColor(0.3, 0.7, 0.4, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_background()
        fps = pyglet.clock.get_fps()
        self.fps_label.x=20
        self.fps_label.y=self.height-20-24
        self.fps_label.text = "FPS:%.2f" % fps
        self.fps_label.draw()
        self.main_menu.draw()

        '''
        vertices = [0, 0,
            self.width, 0,
            self.width, self.height]
        vertices_gl_array = (GLfloat * len(vertices))(*vertices)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vertices_gl_array)
        glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)

        glDisableClientState(GL_VERTEX_ARRAY)
        return
'''

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
    w = MyWindow(caption="Pyweek34 by yarolig", resizable=True, vsync=True)
    pyglet.clock.schedule_interval(w.update, 1.0/30)
    pyglet.app.run()
    print("end.")