import pygame
import sys, os
import random

import numpy as np
from pygame.locals import *
from utils import im2col
from copy import deepcopy

class grid_world:
    def __init__(self):
        pygame.init()
        self.grid_size=32
        self.xlen=15
        self.ylen=15

        width=self.grid_size*15
        height=self.grid_size*15
        window_size = (width, height)
        self.screen = pygame.display.set_mode(window_size)

        agent_img_path='images/agent.png'
        chip_path='images/chip.png'
        self.img_agent = pygame.image.load(agent_img_path)
        self.img_agent = pygame.transform.smoothscale(self.img_agent,
                                         (self.grid_size, self.grid_size))


        self.img_bg = pygame.image.load(chip_path)


        self.agent_pos_1=np.array([8,8])
        self.agent_pos_2=np.array([8,8])
        self.agent_pos_3=np.array([8,8])
        self.agent_inp_pos=np.array([8,8])

        self.agent1_live=True
        self.agent2_live=True
        self.agent3_live=True

        self.map_data=self.get_map_data()
        self.field_1=4
        self.field_2=4
        self.field_3=4
        self.field_inp=0
        self.field_ad_rend=[[0,0],[1,0],[2,0],
                            [0,1],[1,1],[2,1],
                           [0,2],[1,2],[2,2]]
        self.done=[False,False,False]


    def get_map_data(self):


        map_data=np.array([

            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,


            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,


            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,

            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,



        ])


        return map_data


    def render(self):
        chip_list=[
            np.array((0,0)),
            np.array((32,0)),
            np.array((0,32)),
            np.array((32,32))
        ]
        chip_list=np.array(chip_list)
        for y in range(0, 15):
            for x in range(0, 15):
                i = (x+self.field_ad_rend[self.field_inp][0]*15) + (y+self.field_ad_rend[self.field_inp][1]*15)*45
                c = self.map_data[i]
                self.screen.blit(self.img_bg,
                         (x * self.grid_size, y * self.grid_size),
                         (chip_list[c],(self.grid_size, self.grid_size)))


        self.screen.blit(self.img_agent,
                ((self.agent_pos_1[0]-self.field_ad_rend[self.field_inp][0]*15)*self.grid_size,
                 ((self.agent_pos_1[1]-self.field_ad_rend[self.field_inp][1]*15))*self.grid_size))

        self.screen.blit(self.img_agent,
                ((self.agent_pos_2[0]-self.field_ad_rend[self.field_inp][0]*15)*self.grid_size,
                 ((self.agent_pos_2[1]-self.field_ad_rend[self.field_inp][1]*15))*self.grid_size))

        self.screen.blit(self.img_agent,
                ((self.agent_pos_3[0]-self.field_ad_rend[self.field_inp][0]*15)*self.grid_size,
                 ((self.agent_pos_3[1]-self.field_ad_rend[self.field_inp][1]*15))*self.grid_size))


        self.screen.blit(self.img_agent,
                ((self.agent_inp_pos[0]-self.field_ad_rend[self.field_inp][0]*15)*self.grid_size,
                 ((self.agent_inp_pos[1]-self.field_ad_rend[self.field_inp][1]*15))*self.grid_size))






    def step(self,action_1,action_2,action_3,action_inp):
        action_list=np.array([
            np.array([0,0]),
            np.array([0,-1]),
            np.array([0,1]),
            np.array([1,0]),
            np.array([-1,0])
            ])

        "?????????????????????"


        done=False

        agent_action_1=action_list[action_1]
        agent_action_2=action_list[action_2]
        agent_action_3=action_list[action_3]
        agent_inp_action=action_list[action_inp]
        self.agent_pos_1=self.check(self.agent_pos_1,agent_action_1)
        self.agent_pos_2=self.check(self.agent_pos_2,agent_action_2)
        self.agent_pos_3=self.check(self.agent_pos_3,agent_action_3)
        self.agent_inp_pos=self.check(self.agent_inp_pos,agent_inp_action)

        self.field_1=self.reload_field(self.agent_pos_1)
        self.field_2=self.reload_field(self.agent_pos_2)
        self.field_3=self.reload_field(self.agent_pos_3)
        self.field_inp=self.reload_field(self.agent_inp_pos)
        
        ma=deepcopy(self.map_data)
        ma[self.agent_pos_1[0]+self.agent_pos_1[1]*45]=2
        ma[self.agent_pos_2[0]+self.agent_pos_2[1]*45]=3
        ma[self.agent_pos_3[0]+self.agent_pos_3[1]*45]=4
        ma[self.agent_inp_pos[0]+self.agent_inp_pos[1]*45]=5
        ma=ma.reshape(1,1,45,60)
        ma=im2col(ma,15,15,15)

        self.deleate()
        if False not in self.done:
            done = True



        return self.agent_pos_1,self.agent_pos_2,self.agent_pos_3,self.agent_inp_pos,done,ma

    def check(self,pos,action):
        init_pos=pos
        a_pos=pos
        a_pos=pos+action
        data=self.map_data[(a_pos[0])+a_pos[1]*45]
        if data!=0:
            return init_pos
        else:
            return a_pos

    def reload_field(self,a_pos):
        loc=np.arange(12)
        loc_x=a_pos[0]//15
        loc_y=a_pos[1]//15
        f=loc[loc_x+loc_y*3]
        return f

    def deleate(self):
        a_pos=[self.agent_pos_1,self.agent_pos_2,self.agent_pos_3]
        d=[]
        done=False
        for i,a in enumerate(a_pos):
            d.append((np.linalg.norm(a-self.agent_inp_pos)<2))
        if d[0]:
            self.agent_pos_1=[0,52]
            self.done[0]=True
        if d[1]:
            self.agent_pos_2=[0,52]
            self.done[1]=True
        if d[2]:
            self.agent_pos_3=[0,52]
            self.done[2]=True





    def reset(self):
        self.agent_pos_1=np.array([7,7])
        self.agent_pos_2=np.array([37,7])
        self.agent_pos_3=np.array([7,37])
        self.agent_inp_pos=[22,22]
        self.done=[False,False,False]
        
        ma=deepcopy(self.map_data)
        ma[self.agent_pos_1[0]+self.agent_pos_1[1]*45]=2
        ma[self.agent_pos_2[0]+self.agent_pos_2[1]*45]=3
        ma[self.agent_pos_3[0]+self.agent_pos_3[1]*45]=4
        ma[self.agent_inp_pos[0]+self.agent_inp_pos[1]*45]=5

        return self.agent_pos_1,self.agent_pos_2,self.agent_pos_3,self.agent_inp_pos,ma
