import pygame
import sys, os
import random

import numpy as np
from copy import copy
from pygame.locals import *
from gridworld import grid_world
from policy import Inp, Crew




env=grid_world()
agent_pos1,agent_pos2,agent_pos3,agent_inp_pos=env.reset()

cr1=Crew()
cr2=Crew()
cr3=Crew()
inp=Inp()
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
    action1=cr1.forward(agent_pos1,agent_inp_pos)
    action2=cr2.forward(agent_pos2,agent_inp_pos)
    action3=cr3.forward(agent_pos3,agent_inp_pos)
    action_inp=inp.forward(agent_inp_pos,agent_pos1,agent_pos2,agent_pos3)
    agent_pos1,agent_pos2,agent_pos3,agent_inp_pos,done,data=env.step(action1,action2,action3,action_inp)

    """if i%30==0:
        print(action_inp)"""


    if done==True:
        agent_pos1,agent_pos2,agent_pos3,agent_inp_pos=env.reset()
        i=0
    i+=1




    pygame.display.flip()
