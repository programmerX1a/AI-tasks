from load import get_dataloaders,encode,decode,get_idx_2_word,get_word_2_idx
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torchvision
import matplotlib.pyplot as plt
import re
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
from collections import Counter
from torch.utils.data import DataLoader
from torchvision import models,transforms
from PIL import Image
import os

train,val,test=get_dataloaders()
word_2_idx=get_word_2_idx()
idx_2_word=get_idx_2_word()
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Encoder(nn.Module):
    def __init__(self,img_embed): #Choose 2048
        super().__init__()
        self.img_embed=img_embed
        self.cnn_model=models.inception_v3(models.Inception_V3_Weights.DEFAULT)
        self.cnn_model.fc=nn.Linear(self.cnn_model.fc.in_features,self.img_embed)
        self.cnn_model=self.cnn_model.to(device)
        self.dropout=nn.Dropout(0.4)
        self.relu=nn.ReLU()
        for i in self.cnn_model.parameters():
            i.requires_grad=False
        for i in self.cnn_model.fc.parameters():
            i.requires_grad=True
    
    def forward(self,paths):
        image_transform= transforms.Compose([
            transforms.Resize((299, 299)),       
            transforms.ToTensor(),                
            transforms.Normalize(                 
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            )
        ])

        

   

        imgs=[image_transform(Image.open(os.path.abspath("Images/"+i)).convert("RGB"))    for i in paths]
        imgs=torch.stack(imgs)
        imgs=imgs.to(device)
        output=self.cnn_model(imgs)
        if hasattr(output,"logits"):
            output=output.logits
        output=self.relu(output)
        output=self.dropout(output)
        return output




class Decoder(nn.Module):
    def __init__(self,text_embed_size,img_embed): #Choose embed=300
        super().__init__()
        self.vocab_size=len(idx_2_word)
        self.embed=nn.Embedding(self.vocab_size,text_embed_size,padding_idx=word_2_idx.get("<pad>"))
        self.lstm=nn.LSTM(text_embed_size,img_embed,batch_first=True)
        self.linear=nn.Linear(img_embed,self.vocab_size)
        self.dropout=nn.Dropout(0.4)
    def forward(self,caption,image):
        embedded_caption=self.dropout(self.embed(caption))
        output,(hidden,cell)=self.lstm(embedded_caption,(image.unsqueeze(0),image.unsqueeze(0)))
        output=self.linear(output)
        return output


class Model(nn.Module):
    def __init__(self,encoder,decoder):
        super().__init__()
        self.encoder=encoder
        self.decoder=decoder
    def forward(self,image,caption):
        return self.decoder(caption,self.encoder(image))



encoder=Encoder(512)
decoder=Decoder(300,512)
model=Model(encoder,decoder).to(device)


def get_model():
    return model




