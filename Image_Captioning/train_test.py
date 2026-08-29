from load import get_dataloaders,encode,decode,get_idx_2_word,get_word_2_idx
from models import get_model
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
from torch import optim
import os

model=get_model()
word_2_idx=get_word_2_idx()
idx_2_word=get_idx_2_word()
criterion=nn.CrossEntropyLoss(ignore_index=word_2_idx.get("<pad>"))
train,val,test=get_dataloaders()
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer=optim.Adam(model.parameters(),lr=0.001)



def train_epochs(epochs):
    
    for epoch in range(epochs):
        model.train()
        n_batches=0
        total_loss=0
        correct_ans=0
        for batch in train:
            n_batches+=1
            image=batch["image"]
            loss=[]
            for reference in batch["encoded_text"]:
                reference=reference.to(device)
                reference=reference.long()
                reference_to_predict=reference[:,0:-1] #Take start token ignore end token
                label=reference[:,1:]
                label=label.long()

                
                logits=model(image,reference_to_predict)

                prediction=logits.argmax(dim=-1)
                mask=prediction!=0
                correct_ans+=(prediction[mask]==label[mask]).float().mean().item()


                loss_ref=criterion(logits.reshape(-1,logits.shape[-1]),label.reshape(-1))
                loss.append(loss_ref)
            batch_loss=torch.stack(loss).mean()
            optimizer.zero_grad()
            model.zero_grad()
            batch_loss.backward()
            optimizer.step()

            total_loss+=batch_loss.item()
        print(total_loss/n_batches)
        print(correct_ans/n_batches)
            
                

        


model.eval()
n_batches=0
total_loss=0
correct_ans=0
for batch in test:
    n_batches+=1
    image=batch["image"]
    loss=[]
    for reference in batch["encoded_text"]:
        with torch.no_grad():
            reference=reference.to(device)
            reference=reference.long()

            label=reference[:,1:]
            label=label.long()
            reference_to_predict=np.zeros(reference.shape)
            reference_to_predict[:,0]=word_2_idx.get("<start>")
            reference_to_predict[:,-1]=word_2_idx.get("<end>")
            reference_to_predict=torch.tensor(reference_to_predict[:,0:-1]).to(device).long()
            print(reference_to_predict)
            logits=model(image,reference_to_predict)

            prediction=logits.argmax(dim=-1)
            mask=prediction!=0
            correct_ans+=(prediction[mask]==label[mask]).float().mean().item()
            print(decode(prediction.cpu().detach().tolist()[0]))


            loss_ref=criterion(logits.reshape(-1,logits.shape[-1]),label.reshape(-1))
            loss.append(loss_ref)
        batch_loss=torch.stack(loss).mean()
        total_loss+=batch_loss.item()
print(total_loss/n_batches)
print(correct_ans/n_batches)
    
        



