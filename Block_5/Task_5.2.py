from torchvision.datasets import ImageFolder
import torch
import torch.nn as nn
from torch.utils.data import DataLoader,random_split
from torchvision import transforms,models,datasets
import matplotlib.pyplot as plt
import numpy as np
from torch import optim
import os




preprocess=transforms.Compose(
    [
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
         mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
]
)

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dataset=ImageFolder(
    os.path.abspath("caltech101"),
    transform=preprocess,
)
total_size=len(dataset)
train_size=int(0.7*total_size)
val_size=int(0.15*total_size)
test_size=total_size-train_size-val_size

train_dataset,val_dataset,test_dataset=random_split(dataset,[train_size,val_size,test_size])
train_loader=DataLoader(train_dataset,batch_size=64,shuffle=True)
val_loader=DataLoader(val_dataset,batch_size=64,shuffle=False)
test_loader=DataLoader(test_dataset,batch_size=64,shuffle=False)

criterion=nn.CrossEntropyLoss()

model1=models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
model2=models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

num_classes=len(dataset.classes)
model1.fc=nn.Linear(model1.fc.in_features,num_classes)
print(model2.classifier)
model2.classifier[1]=nn.Linear(model2.classifier[1].in_features,num_classes)

model1=model1.to(device)
model2=model2.to(device)


for i in model1.parameters():
    i.requires_grad=False
for i in model1.fc.parameters():
    i.requires_grad=True


for i in model2.parameters():
    i.requires_grad=False
for i in model2.classifier[1].parameters():
    i.requires_grad=True

optimizer1=optim.Adam(model1.fc.parameters(),lr=0.03)
optimizer2=optim.SGD(model2.classifier[1].parameters(),lr=0.03)
epochs=10

for epoch in range(epochs):

    model1.train()
    running_loss1=0
    total=0
    running_loss2=0

    for images,labels in train_loader:
        images,labels=images.to(device),labels.to(device)
        optimizer1.zero_grad()
        output1=model1(images)
        loss1=criterion(output1,labels)
        loss1.backward()
        optimizer1.step()
        running_loss1+=loss1.item()*labels.size(0)
        total+=labels.size(0)
    print(f"Training Loss Model 1: {running_loss1/total}")
        
for epoch in range(epochs):

    model2.train()
    total=0
    running_loss2=0

    for images,labels in train_loader:
        images,labels=images.to(device),labels.to(device)
  
        optimizer2.zero_grad()
        output2=model2(images)
        loss2=criterion(output2,labels)
        loss2.backward()
        optimizer2.step()
        running_loss2+=loss2.item()*labels.size(0)
        total+=labels.size(0)
    print(f"Training Loss Model 2: {running_loss2/total}")
        