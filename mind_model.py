import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.fc = nn.Linear(288, 3)
        
        
    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
    
class network(nn.Module):
    def __init__(self):
        super(network, self).__init__()
        
        
        self.fc = nn.Linear(3, 1)
        
    def forward(self,x):
        x=self.fc(x)
        return x
    
    
class pychology_module(CNN):
    pass
    

class intention_module(network):
    pass
    
    
    
class mind_model():
    def __init__(self):
        self.pychology_module=pychology_module()
        self.intention_module=intention_module()
        
    def forward(self,input_data):

        pychology=self.pychology_module(input_data)
        intention=self.intention_module(pychology)
        
        return pychology, intention
        