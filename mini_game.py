import pygame
import sys, os
import random

import numpy as np
from copy import copy
from pygame.locals import *
from mini_world import grid_world
from mini_policy import agent




env=grid_world()
agent_pos1,agent_pos2,agent_pos3,agent_pos4,done_list,data,is_inposter=env.reset()
inp=[False,False,False,False]
inp[is_inposter]=True
print(is_inposter)
agent_1=agent(data,inp_flag=inp[0])
agent_2=agent(data,inp_flag=inp[1])
agent_3=agent(data,inp_flag=inp[2])
agent_4=agent(data,inp_flag=inp[3])

action_inp=0
Start=False
i=0
while True:
    env.render()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            Start=True
    if Start==False:
        continue
    i+=1

    if i%30!=0:

        continue

    action1=agent_1.action(agent_pos1,[agent_pos2,agent_pos3,agent_pos4],done_list,die=done_list[0])
    action2=agent_2.action(agent_pos2,[agent_pos1,agent_pos3,agent_pos4],done_list,die=done_list[1])
    action3=agent_3.action(agent_pos3,[agent_pos1,agent_pos2,agent_pos4],done_list,die=done_list[2])
    action4=agent_4.action(agent_pos4,[agent_pos1,agent_pos2,agent_pos3],done_list,die=done_list[3])
    agent_pos1,agent_pos2,agent_pos3,agent_pos4,done,done_list,data=env.step(action1,action2,action3,action4)

    """if i%30==0:
        print(action_inp)"""


    if done==True:
        agent_pos1,agent_pos2,agent_pos3,agent_pos4,done,done_list,data,is_inposter=env.reset()
        i=0




    pygame.display.flip()
