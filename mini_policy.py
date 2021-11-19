import pygame
import sys, os
import random

import numpy as np
import torch
from copy import copy
from pygame.locals import *
from gridworld import grid_world
from mind_model import mind_model

class agent:
    def __init__(self,data,inp_flag=False):
        self.inp_flag=inp_flag #自身がインポスターの時にTrueになるフラグ
        self.map=data #マップデータを取得
        self.mind_model=None #他者モデルを定義、実験時はエージェントの数だけ用意

    def action(self,a_pos,others_list,done,die=False):
        if die:
            return 0

        q_list=[0,0,0,0] #行動価値関数、敵から逃げて味方に接触するように価値を加算（インポスターの場合は捕まえるようにする）

        if self.inp_flag:
            act=self.inp_act(a_pos,others_list,q_list,done)

        else:
            act=self.crew_act(a_pos,others_list,q_list,done)

        return act+1

    def crew_act(self,a_pos,others_list,q_list,done):
        """
        like_inposter=[self.mind_model.forward(others) for others in others_list]
        """
        like_inposter=[0.1,0.1,0.1] #他エージェントに対するインポスターへの疑い度合い
        threshold=0.5 #他エージェントをインポスターであると疑う閾値

        pred_inposter=[like>threshold for like in like_inposter] #閾値以上ならインポスターとする

        distance_list=[a_pos-others for others in others_list]

        "価値を計算"
        for i,distance in enumerate(distance_list):
            if done[i]:
                continue
            q_list[1]+= int(distance[1]>1)*10 *((20-np.abs(distance[1]))/12) *like_inposter[i]
            q_list[0]+= int(distance[1]<1)*10 *((20-np.abs(distance[1]))/12) *like_inposter[i]
            q_list[3]+= int(distance[0]>1)*10 *((20-np.abs(distance[0]))/12) *like_inposter[i]
            q_list[2]+= int(distance[0]<1)*10 *((20-np.abs(distance[0]))/12) *like_inposter[i]

            q_list[0]+= int(distance[1]>2)*3 *((20-np.abs(distance[1]))/12) *(1-like_inposter[i])
            q_list[1]+= int(distance[1]<2)*3 *((20-np.abs(distance[1]))/12) *(1-like_inposter[i])
            q_list[2]+= int(distance[0]>2)*3 *((20-np.abs(distance[0]))/12) *(1-like_inposter[i])
            q_list[3]+= int(distance[0]<2)*3 *((20-np.abs(distance[0]))/12) *(1-like_inposter[i])

        q_list=self.check(a_pos,q_list) #遮蔽物に向かわないように価値をなくす
        #act=np.argmax(q_list)
        q_list=[q*int(q>0) for q in q_list]
        act=list(range(0,4))
        st=q_list/np.sum(q_list) #価値を確率の形に直す
        try:
            act=np.random.choice(act,p=st)
        except:
            act=np.random.choice(act)

        return act

    def inp_act(self,a_pos,others_list,q_list,done):
        like_inposter=[1,1,1] #他エージェントが自分をどれだけインポスターとして疑っているか
        distance_list=[a_pos-others for others in others_list]

        for i,distance in enumerate(distance_list):
            if done[i]:
                continue
            q_list[0]+= int(distance[1]>1)*10 *((10-np.abs(distance[1]))/12) *like_inposter[i]
            q_list[1]+= int(distance[1]<1)*10 *((10-np.abs(distance[1]))/12) *like_inposter[i]
            q_list[2]+= int(distance[0]>1)*10 *((10-np.abs(distance[0]))/12) *like_inposter[i]
            q_list[3]+= int(distance[0]<1)*10 *((10-np.abs(distance[0]))/12) *like_inposter[i]

        q_list=self.check(a_pos,q_list)
        #act=np.argmax(q_list)
        q_list=[q*int(q>0) for q in q_list]
        act=list(range(0,4))
        st=q_list/np.sum(q_list)
        try:
            act=np.random.choice(act,p=st)
        except:
            act=np.random.choice(act)


        return act



    def check(self,pos,q_list):
        init_pos=pos
        action_list=np.array([
            np.array([0,-1]),
            np.array([0,1]),
            np.array([-1,0]),
            np.array([1,0])
            ])
        a_pos=[pos+act for act in action_list]

        for i,a in enumerate(a_pos):

            data_list=self.map[a[0]+a[1]*15]
            if data_list!=0:
                q_list[i]=0
            else:
                continue

        return q_list
