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
df=pd.read_csv("captions.txt")
df["caption"]=df["caption"].astype(str).str.lower()
df["caption"]=df["caption"].str.replace(".","")
def preprocessing_sentences(sentence):
    clean_sentence=re.sub(r" '","'",sentence)
    clean_sentence=re.sub(r"' ","'",sentence)
    clean_sentence=re.sub(r"[^a-z\s']++","",clean_sentence)
    clean_sentence=re.sub(r"\s{2,}"," ",clean_sentence)
    return clean_sentence
def get_len(sentence):
    return int(len(sentence.split()))
df["caption"]=df["caption"].map(preprocessing_sentences)
df["length"]=df["caption"].map(get_len)

max_length=df["length"].max() +2 #Account for start and end tokens



sentences=df["caption"].values.tolist()
tokenized_sentence=[i.split() for i in sentences]
counter=Counter()
for i in tokenized_sentence:
    counter.update(i)




index_2_word=["<pad>","<unk>","<start>","<end>"]
count=0
for i in counter.most_common():
    index_2_word.append(i[0])
word_2_index={}
for idx,word in enumerate(index_2_word):
    word_2_index[word]=idx

def encode(sentence):
    sentence=sentence.split()
    encoded=np.zeros(max_length,dtype=np.int32)
    encoded[0]=word_2_index["<start>"]
    encoded[1:len(sentence)+1]=[word_2_index.get(i,word_2_index["<unk>"]) for i in sentence]
    encoded[len(sentence)+1]=word_2_index["<end>"]
    return encoded
def decode(sentence):
    decoded=[]
    for i in sentence:
        if index_2_word[i]=="<start>" or index_2_word[i]=="<pad>":
            continue
        elif index_2_word[i]=="<end>":
            break
        else:
            decoded.append(index_2_word[i])
    return " ".join(decoded)



df["references"]=pd.Series(df["caption"].values.reshape(-1,5)).dropna()

df["image"]=df[df["image"].duplicated()==False]["image"]
df=df.dropna()



class Dataset:
    def __init__(self,df):
        self.df=df
    def __getitem__(self, key):        
        image=self.df["image"].iloc[key]
        text=self.df["references"].iloc[key]
        encoded_text=[encode(i) for i in text]
        return {"image":image,"text":text,"encoded_text":encoded_text}
    def __len__(self):
        return self.df["references"].shape[0]
    
    




df_train,df_test=train_test_split(df,test_size=0.1,random_state=42)
df_train,df_val=train_test_split(df_train,test_size=0.1,random_state=42)
df_train=df_train.reset_index(drop=True)
df_test=df_test.reset_index(drop=True)

    
train_dataset=Dataset(df_train)
test_dataset=Dataset(df_test)
val_dataset=Dataset(df_val)
train_dataloader=DataLoader(train_dataset,batch_size=64,shuffle=True)
test_dataloader=DataLoader(test_dataset,batch_size=64,shuffle=False)
val_dataloader=DataLoader(val_dataset,batch_size=64,shuffle=False)

def get_dataloaders():
    return train_dataloader,val_dataloader,test_dataloader

def get_word_2_idx():
    return word_2_index
def get_idx_2_word():
    return index_2_word