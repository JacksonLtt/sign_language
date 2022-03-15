# -*- coding: utf-8 -*-
"""
Transfer Learning Project

author: Hao Zhou

"""


import torch

from signTrans.Models import Transformer

    

device = torch.device('cuda')


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


x = torch.rand(32, 4, inputsize).cuda()
y = torch.rand(32, 4, outputsize).cuda()

out = model(x,y)

print(out.shape)































