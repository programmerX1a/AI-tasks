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
        total_tokens=0
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
                mask=label!=0
                correct_ans+=(prediction[mask]==label[mask]).sum().item()
             
                total_tokens+=mask.sum().item()
               


                loss_ref=criterion(logits.reshape(-1,logits.shape[-1]),label.reshape(-1))
                loss.append(loss_ref)
            batch_loss=torch.stack(loss).mean()
            optimizer.zero_grad()
            model.zero_grad()
            batch_loss.backward()
            optimizer.step()
            

            total_loss+=batch_loss.item()
            torch.save({"epoch": epoch,"model_state": model.state_dict(),"optimizer_state": optimizer.state_dict()}, "checkpoint.pth")
        print(total_loss/n_batches)
        print(correct_ans/total_tokens)
            
                

        








train_epochs(10)



model.eval()

for batch in test:
    with torch.no_grad():
        image=batch["image"]
        img_num=len(image)
        reference_to_predict=np.zeros((img_num,1))
        reference_to_predict[:,0]=word_2_idx.get("<start>")
        reference_to_predict=torch.tensor(reference_to_predict).to(device).long()
        logits=model.generate_caption(image,reference_to_predict,img_num)
        for i in range(img_num):
            plt.figure()
            plt.imshow(Image.open(os.path.abspath("Images/"+image[i])))
            plt.title(logits[i])

    
            
                    
      
        


        