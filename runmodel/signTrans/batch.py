# -*- coding: utf-8 -*-
"""
Sign Language Recognition Project

author: Hao Zhou

"""

import torch



class Batch:
    """
    create a batch
    """

    def __init__(self,
                 batch,
                 src_dim: int = 512,
                 train: bool = True,
                 cuda: bool = False,
                 src_is_text: bool = True,
                 ):


        
        

        self.src, self.src_length = batch.src
        self.trg, self.trg_length = batch.trg
        
        # src_dim = self.src.shape[2]
        
        # self.src_mask = None # src task
        # self.trg_mask = None # 
        self.ids = None
        
        # if src_is_text == True:
        #     self.src_mask = (self.src != pad_index).unsqueeze(1)
        
        
        if src_is_text == False:
            self.ids = batch.id
        #     self.src_mask = (self.src != torch.zeros(src_dim))[..., 0].unsqueeze(1)

        # True if data valid
        # self.src_mask = (self.src != pad_index).unsqueeze(1)
        
        # cut the eos token?
        # self.trg_input = self.trg[:, :-1]

        # txt is used for loss computation, shifted by one since BOS
        # self.trg = self.trg[:, 1:]
        
        # True if data valid
        # self.trg_mask = (self.trg_input != pad_index).unsqueeze(1)
        
        # print(self.txt, self.txt.shape)
        
        if cuda:
            self.to_()
            
    def to_(self):

        self.src = self.src.cuda()
        self.trg = self.trg.cuda()
        # self.src_mask = self.src_mask.cuda()

        # if self.trg_input is not None:
        #     self.trg = self.trg.cuda()
        #     # self.trg_mask = self.trg_mask.cuda()
        #     self.trg_input = self.trg_input.cuda()