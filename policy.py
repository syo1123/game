import pygame
import sys, os
import random

import numpy as np
import torch
from copy import copy
from pygame.locals import *
from gridworld import grid_world
from mind_model import mind_model



#-------------------------------------------------------------------------
class action:
    def __init__(self,inp_flag=False):
        self.inp_flag=inp_flag
        # 上,下,右,左
        self.map=np.vstack([np.array([0,1,1,0]),np.array([0,1,1,1]),np.array([0,1,0,1]),
                np.array([1,1,1,0]),np.array([1,1,1,1]),np.array([1,1,0,1]),
                np.array([1,0,1,0]),np.array([1,0,1,1]),np.array([1,0,0,1]),
                np.array([1,0,1,0]),np.array([1,0,1,1]),np.array([1,0,0,1])])

        self.field_ad=[[0,0],[1,0],[2,0],
                            [0,1],[1,1],[2,1],
                           [0,2],[1,2],[2,2],
                           [0,3],[1,3],[3,3]]

        self.pre_e_pos=[]
        self.pre_map=0
        self.pre_act=1

    def go_exit(self,a_argmin):
        act_list=[1,2,3,4]
        return act_list[a_argmin]

    def go_central(self,a_argmin):
        act_list=[2,1,4,3]
        return act_list[a_argmin]

    def relative_pos(self,a_pos,a_f):
        a_x=a_pos[0]-self.field_ad[a_f][0]*15
        a_y=a_pos[1]-self.field_ad[a_f][1]*15
        return np.array([a_x,a_y])

    def act_inp(self,a_argmin,e_argmin,argmin_exit,near_exit,cen):
        if argmin_exit:
            if near_exit:
                act=self.go_exit(e_argmin)
            else:
                act=self.go_central(a_argmin)
        else:
            if cen:
                act=self.go_exit(e_argmin)
            else:
                act=self.go_central(a_argmin)

        return act

    def act_crew(self,a_argmin,argmin_exit,near_exit):
        if argmin_exit:
            if near_exit:
                act=self.go_central(a_argmin)
            else:
                act=self.go_exit(a_argmin)
        else:
            act=self.go_exit(a_argmin)

        return act

    def distance(self,a_pos,e_pos,exit):
        e_pos_norm=[np.linalg.norm(e_pos-e) for e in exit]
        a_pos_norm=[np.linalg.norm(a_pos-e) for e in exit]

        e_min=np.min(e_pos_norm)
        a_min=np.min(a_pos_norm)

        e_argmin=np.argmin(e_pos_norm)
        a_argmin=np.argmin(a_pos_norm)

        return e_pos_norm,a_pos_norm,e_min,a_min,e_argmin,a_argmin

    def is_central(self,a_pos):
        cen_x=(a_pos[0]<=8 and a_pos[0]>=6)
        cen_y=(a_pos[1]<=8 and a_pos[1]>=6)
        central=(cen_x and cen_y)
        return central

    def softmax(self,map):
        return map/np.sum(map)



    def step(self,agent_pos,enemy_pos,a_f,e_f):
        self.exit=np.array([[7,0],[7,14],[14,7],[0,7]])
        field=(a_f==e_f)
        a_pos=self.relative_pos(agent_pos,a_f)
        map=copy(self.map[a_f])
        exit=copy(self.exit)
        pre_map=(self.pre_map!=a_f)
        self.pre_map=a_f
        cen=self.is_central(a_pos)

        for i,n in enumerate(map):
            if n==0: exit[i]+=100



        if pre_map:
            self.pre_e_pos=[]

        if field:
            e_pos=self.relative_pos(enemy_pos,e_f)

            e_pos_norm,a_pos_norm,e_min,a_min,e_argmin,a_argmin=self.distance(a_pos,e_pos,exit)
            argmin_exit=(e_argmin==a_argmin)
            near_exit=(e_min<=a_min)

            if self.inp_flag:
                act=self.act_inp(a_argmin,e_argmin,argmin_exit,near_exit,cen)

            else:
                act=self.act_crew(a_argmin,argmin_exit,near_exit)
            self.pre_e_pos=exit[e_argmin]


        else:
            if len(self.pre_e_pos)<=0:
                map_list=[10,1,0,3,2]
                m=copy(self.map[a_f])
                m[map_list[self.pre_act]]=0
                #map_act=self.softmax(self.map[a_f])
                map_act=self.softmax(m)

                e_pos=exit[np.random.choice(np.arange(4),p=map_act)]
                self.pre_e_pos=e_pos

            e_pos=self.pre_e_pos
            e_pos_norm,a_pos_norm,e_min,a_min,e_argmin,a_argmin=self.distance(a_pos,e_pos,exit)
            argmin_exit=(e_argmin==a_argmin)
            near_exit=(e_min<=a_min)


            act=self.act_inp(a_argmin,e_argmin,argmin_exit,near_exit,cen)
            self.pre_e_pos=e_pos

        self.pre_act=act

        return act






class Inp:
    def __init__(self):
        self.act=action(inp_flag=True)
        self.cycle=0
    def forward(self,agent_pos,crew_pos1,crew_pos2,crew_pos3):
        self.cycle=(self.cycle+1)%30
        if self.cycle==0:
            c_f1=crew_pos1[0]//15+3*(crew_pos1[1]//15)
            c_f2=crew_pos2[0]//15+3*(crew_pos2[1]//15)
            c_f3=crew_pos3[0]//15+3*(crew_pos3[1]//15)
            inp_f=agent_pos[0]//15+3*(agent_pos[1]//15)
            cf=[c_f1,c_f2,c_f3]
            crw=[crew_pos1,crew_pos2,crew_pos3]
            nearest=np.argmin([np.linalg.norm(agent_pos-c) for c in crw])
            crew_pos=crw[nearest]
            c_f=cf[nearest]

            a=self.act.step(agent_pos,crew_pos,inp_f,c_f)
        else:
            a=0

        return a

class Crew:
    def __init__(self):
        self.act=action()
        self.cycle=0
        self.others_model=mind_model()
    def forward(self,agent_pos,inp_pos,data):
        self.cycle=(self.cycle+1)%40
        if self.cycle==0:
            
            c_f=agent_pos[0]//15+3*(agent_pos[1]//15)
            inp_f=inp_pos[0]//15+3*(inp_pos[1]//15)
            data=torch.tensor(data[0][c_f].reshape(1,1,15,15)).float()
            x=self.others_model.forward(data)

            a=self.act.step(agent_pos,inp_pos,c_f,inp_f)
        else:
            a=0

        return a
