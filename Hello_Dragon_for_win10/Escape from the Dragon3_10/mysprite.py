# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *


class MySprite(pygame.sprite.Sprite):  # 继承pygame.sprite.Sprite
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)  # 拓展基本类
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    # X property
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self, value): self.rect.topleft = value
    position = property(_getpos, _setpos)

    def load(self, model, width, height, columns):
        # self.master_image = pygame.image.load(filename).convert_alpha()  # 漏打()会导致master_image不成对应类，get_rec()失败
        self.master_image = model
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width)*(rect.height // height) - 1

    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame)+","+str(self.first_frame)+","+str(self.last_frame)+","+str(self.frame_width)+","+str(self.frame_height)+","+str(self.columns)+","+str(self.rect)
