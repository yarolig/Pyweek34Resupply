#!/usr/bin/env python
# coding: utf-8

import pyglet
from pyglet.gl import *
from math import sin, cos
def load_texture(name):
    return pyglet.resource.texture(name)

class LastMousePos:
    x = 0
    y = 0

class Array2D:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = [None for i in range(w*h)]

    def get(self, x, y):
        assert 0 <= x < self.w and 0 <= y < self.h
        return self.data[x+y*self.w]

    def enumcyx(self):
        for y in range(self.h):
            for x in range(self.h):
                yield self[[x, y]], y, x

    def __getitem__(self, item):
        x, y = item
        assert 0 <= x < self.w and 0 <= y < self.h

        return self.data[x + y * self.w]

    def __setitem__(self, key, value):
        x, y = key
        assert 0 <= x < self.w and 0 <= y < self.h

        self.data[x + y * self.w] = value


class HeightMap:
    CELL_SIZE = 1.0
    def __init__(self, w=64, h=64):
        self.xx = w
        self.yy = h
        self.heights = Array2D(w, h)
        for c, y, x in self.heights.enumcyx():
            self.heights[[x, y]] = sin(y*0.01) + sin(x*0.15) + sin(y*0.12) * sin(x*0.25)


    def draw(self):
        tex_scale = 0.33
        coords = []
        tex_coords = []
        normals = []

        for c, y, x in self.heights.enumcyx():
            coords.append(x*1.0)
            coords.append(y*1.0)
            coords.append(c*4.0)
            tex_coords.append(x * tex_scale)
            tex_coords.append(y * tex_scale)
            normals.append(0.0)
            normals.append(0.0)
            normals.append(1.0)

        indices = []
        for i in range(self.xx - 1):
            for j in range(self.yy - 1):
                ii = i + 1
                jj = j + 1
                indices.append(i + j * self.yy)
                indices.append(ii + j * self.yy)
                indices.append(ii + jj * self.yy)

                indices.append(ii + jj * self.yy)
                indices.append(i + jj * self.yy)
                indices.append(i + j * self.yy)


        pyglet.graphics.draw_indexed(
            len(coords) // 3,
            GL_TRIANGLES,
            indices,
            ('v3f', coords),
            ('t2f', tex_coords),
            ('n3f', normals),
        )

class CellBlock:
    def __init__(self):
        self.xx = 32
        self.yy = 32
        self.zz = 32



class Level:
    def __init__(self):
        self.x = 100
        self.y = 100

    def draw(self):
        pass


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
        LastMousePos.x=x
        LastMousePos.y=y
        print("on_mouse_motion", locals())
    def on_mouse_press(self, x, y, button, modifiers):
        LastMousePos.x=x
        LastMousePos.y=y
        print("on_mouse_press",locals())
    def on_mouse_release(self, x, y, button, modifiers):
        LastMousePos.x=x
        LastMousePos.y=y
        self.main_menu.on_click()
        print("on_mouse_release",locals())
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print("on_mouse_scroll" ,locals())
    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        #gluPerspective(90.0, width / float(height), .1, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        return pyglet.event.EVENT_HANDLED
        pass
    def init(self):
        if self.inited:
            return
        self.inited = True
        #pyglet.resource.add_font('data/fonts/MeromSans-Regular.ttf')
        pyglet.font.add_file('data/fonts/MeromSans-Regular.ttf')


        pyglet.font.load('Merom Sans')
        self.backgroundTex = load_texture('data/statue.png')
        self.groundTex = pyglet.image.load('data/ground.png').get_mipmapped_texture()

        self.fps_label = pyglet.text.Label('FPS',
                          font_name='Merom Sans',
                          font_size=24)
        self.frame = 0
        self.time_of_last_fps_redraw = 0
        self.min_fps = 1000

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
                self.click_handlers=[]

            def is_mouse_inside(self):
                return self.x <= LastMousePos.x <= self.x + 300 and self.y <= LastMousePos.y <= self.y + 30

            def click(self):
                if self.is_mouse_inside():
                    for f in self.click_handlers:
                        f()
            def draw(self):
                self.label.x=self.x
                self.label.y=self.y
                self.label.text=self.text
                if self.is_mouse_inside():
                    self.label.color = (255, 185, 185,255)
                else:
                    self.label.color = (255, 255, 255, 255)
                self.label.draw()

        class Menu:
            def buttons(self):
                for i in dir(self):
                    if i.startswith('_'):
                        continue
                    try:
                        ii = getattr(self, i)
                        if isinstance(ii, Button):
                            yield ii
                    except Exception as e:
                        print('error', e)

            def draw(self):
                for i in self.buttons():
                    i.draw()

            def on_click(self):
                for i in self.buttons():
                    i.click()

        x = 80
        y = 150
        dy = 34
        self.main_menu = Menu()
        self.main_menu.new_game = Button(x, y, 'New Game');        y -= dy
        self.main_menu.optinos = Button(x, y, 'Options');        y -= dy
        self.main_menu.about = Button(x, y, 'About');        y -= dy
        self.main_menu.exit = Button(x, y, 'Exit');        y -= dy
        self.main_menu.exit.click_handlers.append(lambda: pyglet.app.exit())



        self.heightmap = HeightMap()


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
        try:
            self.on_draw2()
        except Exception as e:
            import sys
            import traceback

            print(e, sys.exc_info()[2])
            traceback.print_tb(sys.exc_info()[2])
            pyglet.app.exit()
    def on_draw2(self):
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
        self.draw3d()


    def draw3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70.0, float(self.width) / self.height, 0.1, 10000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(-3+20,-4+20,5, 3+20,4+20,5, 0,0,1)


        self.setup_lights()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glEnable(self.groundTex.target)
        glBindTexture(self.groundTex.target, self.groundTex.id)

        self.heightmap.draw()


    def setup_lights(self):
        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat*4)(0.8, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat*4)(0.1, 0.1, 0.1, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(0.0,0.0, 1.0, 0.0))

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