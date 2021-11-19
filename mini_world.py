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
        agent_inp_path='images/agent_purple.png'
        self.img_agent = pygame.image.load(agent_img_path)
        self.img_agent = pygame.transform.smoothscale(self.img_agent,
                                         (self.grid_size, self.grid_size))
        self.img_inp = pygame.image.load(agent_inp_path)
        self.img_inp = pygame.transform.smoothscale(self.img_inp,
                                         (self.grid_size, self.grid_size))

        self.img_list=[self.img_agent,self.img_agent,self.img_agent,self.img_agent]


        self.img_bg = pygame.image.load(chip_path)


        self.agent_pos_1=np.array([8,8])
        self.agent_pos_2=np.array([8,8])
        self.agent_pos_3=np.array([8,8])
        self.agent_pos_4=np.array([8,8])

        self.agent1_live=True
        self.agent2_live=True
        self.agent3_live=True
        self.agent4_live=True

        self.map_data=self.get_map_data()
        self.done=[False,False,False,False]

        #is_inposter=random.randrange(4)
        self.is_inposter=random.randrange(4)
        self.img_list[self.is_inposter]=self.img_inp






    def get_map_data(self):


        map_data=[
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
                1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,
                1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,

                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            ]
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
                i = x + y*15
                c = self.map_data[i]
                self.screen.blit(self.img_bg,
                         (x * self.grid_size, y * self.grid_size),
                         (chip_list[c],(self.grid_size, self.grid_size)))


        self.screen.blit(self.img_list[0],
                (self.agent_pos_1[0]*self.grid_size,
                 self.agent_pos_1[1]*self.grid_size))

        self.screen.blit(self.img_list[1],
                (self.agent_pos_2[0]*self.grid_size,
                 self.agent_pos_2[1]*self.grid_size))

        self.screen.blit(self.img_list[2],
                (self.agent_pos_3[0]*self.grid_size,
                 self.agent_pos_3[1]*self.grid_size))


        self.screen.blit(self.img_list[3],
                (self.agent_pos_4[0]*self.grid_size,
                 self.agent_pos_4[1]*self.grid_size))






    def step(self,action_1,action_2,action_3,action_4):
        action_list=np.array([
            np.array([0,0]),
            np.array([0,-1]),
            np.array([0,1]),
            np.array([-1,0]),
            np.array([1,0])
            ])

        "上、下、左、右"


        done=False

        agent_action_1=action_list[action_1]
        agent_action_2=action_list[action_2]
        agent_action_3=action_list[action_3]
        agent_action_4=action_list[action_4]
        self.agent_pos_1=self.check(self.agent_pos_1,agent_action_1)
        self.agent_pos_2=self.check(self.agent_pos_2,agent_action_2)
        self.agent_pos_3=self.check(self.agent_pos_3,agent_action_3)
        self.agent_pos_4=self.check(self.agent_pos_4,agent_action_4)



        ma=deepcopy(self.map_data)



        self.deleate()
        if False not in self.done:
            done = True



        return self.agent_pos_1,self.agent_pos_2,self.agent_pos_3,self.agent_pos_4,done,self.done,ma

    def check(self,pos,action):
        init_pos=pos
        a_pos=pos
        a_pos=pos+action
        data=self.map_data[a_pos[0]+a_pos[1]*15]
        if data!=0:
            return init_pos
        else:
            return a_pos



    def deleate(self):
        d=[]
        agent_list=[self.agent_pos_1,self.agent_pos_2,self.agent_pos_3,self.agent_pos_4]
        a_list=list(range(4))

        inposter=agent_list.pop(self.is_inposter)
        a_list.pop(self.is_inposter)

        for i,agent in zip(a_list,agent_list):
            if np.linalg.norm(agent-inposter)<2:
                self.eliminate(i)


    def eliminate(self,i):
        if i==0:
            self.agent_pos_1=[1,28]
            self.done[0]=True
            print('player1 is killed')
        if i==1:
            self.agent_pos_2=[1,28]
            self.done[1]=True
            print('player2 is killed')
        if i==2:
            self.agent_pos_3=[1,28]
            self.done[2]=True
            print('player3 is killed')
        if i==3:
            self.agent_pos_4=[1,28]
            self.done[3]=True
            print('player4 is killed')



        """done=False
        for i,a in enumerate(a_pos):
            d.append((np.linalg.norm(a-self.agent_pos_4)<2))
        if d[0]:
            self.agent_pos_1=[1,28]
            self.done[0]=True
        if d[1]:
            self.agent_pos_2=[1,28]
            self.done[1]=True
        if d[2]:
            self.agent_pos_3=[1,28]
            self.done[2]=True"""





    def reset(self):
        self.agent_pos_1=np.array([1,3])
        self.agent_pos_2=np.array([8,1])
        self.agent_pos_3=np.array([1,8])
        self.agent_pos_4=np.array([13,13])
        self.done=[False,False,False,False]

        ma=deepcopy(self.map_data)
        ma[self.agent_pos_1[0]+self.agent_pos_1[1]*15]=2
        ma[self.agent_pos_2[0]+self.agent_pos_2[1]*15]=3
        ma[self.agent_pos_3[0]+self.agent_pos_3[1]*15]=4
        ma[self.agent_pos_4[0]+self.agent_pos_4[1]*15]=5

        return self.agent_pos_1,self.agent_pos_2,self.agent_pos_3,self.agent_pos_4,self.done,ma,self.is_inposter
