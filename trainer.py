#!/usr/bin/python

import sys, time
import Xlib
import Image, ImageStat

import pygame
from pygame.locals import *

from Xlib import X, display, Xutil, Xcursorfont, protocol, error
from Xlib.protocol import request

mydisplay = display.Display()
root = mydisplay.screen().root

class Minecraft:

    def __init__(self):
        pass

    def find_window(self):

        # get list of all the windows
        window_ids = root.get_full_property(mydisplay.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType).value

        # find the one that named 'minecraft'
        for window_id in window_ids:
            
            window = mydisplay.create_resource_object('window', window_id)
            name = window.get_wm_name()
            pid = window.get_full_property(mydisplay.intern_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)

            if name.lower() == "minecraft":
                self.geom = window.get_geometry()
                return True 
        
        return False 

    def cross_hair_image(self, size=100):

        x = self.geom.x + (self.geom.width / 2) - (size / 2)
        y = self.geom.y + (self.geom.height / 2) - (size / 2)
        w = size
        h = size

        return self.get_image(x,y,w,h)

    def toolbar_image(self):

        toolbar_w = 9*40
        toolbar_h = 100

        x = self.geom.x + (self.geom.width / 2) - (toolbar_w / 2)
        y = self.geom.y + self.geom.height - toolbar_h
        w = toolbar_w
        h = toolbar_h
    
        return self.get_image(x,y,w,h)

    def get_image(self, x, y, w, h):

        ret = root.get_image(x, y, w, h, X.ZPixmap, 0xffffffff)
        if not ret:
            raise ValueError("Could not get_image! Returned %d" % ret)

        return Image.fromstring("RGBX", (w, h), ret.data, "raw", "BGRX").convert("RGB")

minecraft = Minecraft()

if not minecraft.find_window():
    print "Could not find minecraft window. Exiting"
    sys.exit()
else:
    print "Found minecraft window at (%s, %s) with size (%s, %s)" % (minecraft.geom.x, minecraft.geom.y, minecraft.geom.width, minecraft.geom.height)

pygame.init()
window = pygame.display.set_mode((500,500))
screen = pygame.display.get_surface()

while True:

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            print "quiting"
            sys.exit(0)            

    cross_img = minecraft.cross_hair_image()
    toolbar_img = minecraft.toolbar_image()

    cross_img_pg = pygame.image.frombuffer(cross_img.tostring(), cross_img.size, cross_img.mode)
    toolbar_img_pg = pygame.image.frombuffer(toolbar_img.tostring(), toolbar_img.size, toolbar_img.mode)
    
    screen.blit(cross_img_pg, (0,0))
    screen.blit(toolbar_img_pg, (0,100))

    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0 / 60))

    #mean = ImageStat.Stat(img).mean
    #color = map(int, mean)
    #time.sleep(.05)

