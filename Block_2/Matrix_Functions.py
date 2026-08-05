import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import math

def matrix_transpose(arr):

   try:
      transposed=[]
      length=len(arr[0])

      for i in range(1,len(arr)):
         if len(arr[i])!=length:
            print("Invalid Dimensions")
            return None
      for i in range(0,len(arr[0])):
         array=[]
         for j in range(0,len(arr)):
            array.append(arr[j][i])
         transposed.append(array)
      return transposed
   except TypeError:
      print("Input must be 2D Array")
      return None
def matrix_multiplication(arr1,arr2):
   try:
      result=[]
      length1=len(arr1[0])
      length2=len(arr2[0])
      for i in range(1,len(arr1)):
         if len(arr1[i])!=length1:
            print("Invalid Dimensions")
            return None
      for i in range(1,len(arr2)):
            if len(arr2[i])!=length2:
               print("Invalid Dimensions")
               return None
      row1=len(arr1)
      row2=len(arr2)
      col1=len(arr1[0])
      col2=len(arr2[0])
      if col1!=row2:
         print("First Array's Columns must equal Second Array's Rows")
         return None
      for i in range(0,row1):
         array=[]
         for j in range(0,col2):
            sum=0
            for k in range(0,row2):
               sum+=(arr1[i][k]*arr2[k][j])
            array.append(sum)
         result.append(array)
      return result
   except TypeError:
      print("Input must be 2D Array")
      return None

def standarize_data(arr):
      try:
         length=len(arr[0])
         result=[]
         for i in range(1,len(arr)):
            if len(arr[i])!=length:
               print("Invalid Dimensions")
               return None
         mean=[]
         for i in range(0,len(arr[0])):
            sum=0
            for j in range(0,len(arr)):
               sum+=arr[j][i]
            mean.append(sum/(len(arr)))
         variance=[]
         for i in range(0,len(arr[0])):
            sum=0
            for j in range(0,len(arr)):
               sum+=(arr[j][i]-mean[i])**2
            variance.append(sum/(len(arr)-1))
         std=[]
         for i in range(0,len(variance)):
            std.append(math.sqrt(variance[i]))
         for i in range(0,len(arr)):
            array=[]
            for j in range(0,len(arr[0])):
               try:
                  array.append((arr[i][j]-mean[j])/std[j])
               except ZeroDivisionError:
                  array.append(None)
            result.append(array)
         return result
      except TypeError:
         print("Input Must be 2D Array")
         return None
                
def covariance(arr):
   length=len(arr[0])
   result=[]
   for i in range(1,len(arr)):
      if len(arr[i])!=length:
         print("Invalid Dimensions")
         return None
   for i in range(0,len(arr[0])):
      array=[]
      for j in range(0,len(arr[0])):
         mean_x=0
         mean_y=0
         for m in range(0,len(arr)):
            mean_x+=arr[m][i]
            mean_y+=arr[m][j]
         mean_y/=len(arr)
         mean_x/=len(arr)
         sum=0
         for m in range(0,len(arr)):
            sum+=(arr[m][i]-mean_x)*(arr[m][j]-mean_y)
         sum/=len(arr)-1
         array.append(sum)
      result.append(array)
   return result

         
      


 
      

      


      

   