# -*- coding: utf-8 -*-
"""
Transfer Learning Project

author: Hao Zhou

"""

import numpy as np
import torch
from torch.utils.mobile_optimizer import optimize_for_mobile
from signTrans.Models import Transformer

    

device = torch.device('cpu')


inputsize = 30*256
outputsize = 7*256
model = Transformer(
        inputsize,
        outputsize,

        src_pad_idx=None,
        trg_pad_idx=None, 
        trg_emb_prj_weight_sharing=False,
        emb_src_trg_weight_sharing=False,
        
        d_k=64,
        d_v=64,
        
        d_model=512,
        d_word_vec=512,
        d_hidden=1024,
        
        n_layers=4,
        n_heads=8,
        dropout=0.5,
        scale_emb_or_prj='prj',
        
        n_position=512,
        
        src_is_text=False,
        ).to(device)


x = torch.rand(32, 4, inputsize)
y = torch.rand(32, 4, outputsize)

print("type:",x.shape)

out = model(x,y)
#
print(type(out))






# def reshapeToFourDimension(float[] arr,int size1,int size2,int size3){
#         float[][][] newArr = new float[size1][size2][size3];
#         int index=0;
#
#         for(int i=0; i<size1; i++){
#             for(int j=0; j<size2; j++){
#                 for(int k=0; k<size3; k++) {
#                     newArr[i][j][k] = arr[index];
#                     index++;
#                 }
#             }
#         }

def reshapeToThreeDimension(arr,size1,size2,size3):
        newarr = size1*[size2*[size3*[0]]]
        print(newarr)
        index = 0
        for i in range(size1):
            for j in range(size2):
                for k in range(size3):
                        print("i,j,k,index,value",i," ",j," ",k," ",index," ",arr[index])
                        newarr[i][j][k]=arr[index]
                        print(newarr)
                        index+=1

        return newarr



#
# randnums= np.random.randint(0,100,10)
# print(randnums)
# print(len(randnums))
#
# arr_2d = randnums.reshape((1,2, 5))
# newarr = reshapeToThreeDimension(randnums,1,2,5)
# print(newarr)
# print(arr_2d)























