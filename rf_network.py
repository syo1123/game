import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable

class rf_agent(nn.Module):
    def __init__(self):
        super(rf_agent, self).__init__()
        
        self.layer1=nn.Sequential(nn.Conv2d(1,15,kernel_size=4,
        stride=2,padding=1),
        nn.ReLU(inplace=True))
        
        self.layer2=nn.Sequential(nn.Conv2d(15,30,kernel_size=2,
        stride=2,padding=0),
        nn.ReLU(inplace=True))
        
        self.layer3=nn.LSTM(270, 120,batch_first = True)
        
        self.last_layer=nn.Linear(120,4)
        
        self.reset()

        

    def forward(self, x):
        x=self.layer1(x)
        x=self.layer2(x)       
        x = x.view(1,x.size()[0], -1)
        x,self.hidden=self.layer3(x,self.hidden)
        
        x=self.last_layer(x)
        return x
    
    def reset(self):
        self.hidden = (Variable(torch.zeros(1, 1,120)),Variable(torch.zeros(1, 1,120)))