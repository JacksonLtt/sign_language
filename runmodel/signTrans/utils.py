# -*- coding: utf-8 -*-
"""
Sign Language Recognition Project

author: Hao Zhou

"""

import yaml, os

# import math
# from collections import Counter
# from signTrans.Constants import (                       
#                             UNK_TOKEN,
#                             PAD_TOKEN,
#                             SOS_TOKEN,
#                             EOS_TOKEN,
#                             )
import numpy as np
import torch.nn as nn
import torch
# import torch.nn.functional as F
# from nltk.translate.bleu_score import sentence_bleu

def subsequent_mask(size: int):
    """
    Mask out subsequent positions (to prevent attending to future positions)
    Transformer helper function.
    :param size: size of mask (2nd and 3rd dim)
    :return: Tensor with 0s and 1s of shape (1, size, size)
    """
    mask = np.triu(np.ones((1, size, size)), k=1).astype("uint8")
    return torch.from_numpy(mask) == 0



def save_cfg(cfg, path: str = '..\\transferlearning\\configs\\cfg.yaml') -> None:
    
    # save cfg in 'path'
    
    import os
    if path != None:
        path = os.path.abspath(__file__)
        path = path.replace('signTrans', 'results')
        path = path.replace('utils.py', 'cfg.yaml')
    
    with open(path, 'w') as file:
        yaml.dump(cfg, file)

def load_cfg(path: str = '..\\transferlearning\\configs\\cfg.yaml') -> dict:
    """
    Loads and parses a YAML configuration file.
    :param path: path to YAML configuration file
    :return: configuration dictionary
    """
    
    import os
    if path != None:
        path = os.path.abspath(__file__)
        path = path.replace('signTrans', 'configs')
        # path = path.replace('utils', '')
        path = path.replace('utils.py', 'cfg.yaml')
    
    # path = '..\signlanguage\configs\cfg.yaml'

    with open(path, "r", encoding="utf-8") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        
    # print(cfg)
    return cfg


def findPad(seq, pad_dim):
    pad = torch.zeros(pad_dim).cuda()
    out = (seq != pad)

    # out = torch.where(out==True)
    # print(out)
    return out


def cal_loss(pred, target, cfg):


    out = findPad(target, cfg['dim_out']*cfg['seqlen'])

    # print(out.shape, pred.shape, target.shape)

    masked_pred = pred.where(out==torch.tensor(1,dtype=torch.bool).cuda(), torch.tensor(0.0).cuda())

    # TODO: here, still need to consider when length differ a lot, reduction is mean will decrease the loss


    # if cfg['loss_type'] == 'mse':
    #     loss = nn.MSELoss(reduction='sum')
    #     return loss(masked_pred, target) / out.sum()


    if cfg['loss_type'] == 'mse':
        loss = nn.MSELoss(reduction='mean')
        return loss(masked_pred, target) 
    elif cfg['loss_type'] == 'smoothl1':
        loss = nn.SmoothL1Loss()
        return loss(masked_pred, target)


# TODO: think about how to calculate angles error for each finger
# Right now: for each file, calculate a pct for each finger
# how about: for each file, record diff and combine them for all validate data, then find out pct


def cal_angles(pred, trg):

    assert pred.shape == trg.shape, "Unmatched dimension!!"

    # print(pred.shape, trg.shape)
    pcts = []

    for i in range(pred.shape[-1]):
        diff = np.sort(np.absolute(pred[:, i] - trg[:, i]))
        pct = [np.percentile(diff, 10), np.percentile(diff, 50), np.percentile(diff, 90)]
        pcts.append(pct)


    pcts = np.array(pcts)

    return pcts[:, 0], pcts[:, 1], pcts[:, 2]



def get_pct(results, opt):

    cut = int(results.shape[0] * opt['cut_ratio'])
    # results = results[:cut, :]
    
    pcts = []

    for i in range(results.shape[-1]):
        diff = np.sort(results[:, i])
        diff = diff[:cut]
        pct = [np.percentile(diff, 10), np.percentile(diff, 50), np.percentile(diff, 90)]
        pcts.append(pct)


    pcts = np.array(pcts)

    return pcts[:, 0], pcts[:, 1], pcts[:, 2]  

def cal_stats(pred, target, cfg):

    p10, p50, p90 = [], [], []

    pred_cpu = pred.cpu().detach().numpy()
    target_cpu = target.cpu().detach().numpy()

    # print(pred_cpu.shape, target_cpu.shape)


    for i in range(pred_cpu.shape[0]):
        p = pred_cpu[i]
        t = target_cpu[i]


        pad_dim = t.shape[-1]
        pad = np.zeros(pad_dim)
        out = (t != pad)[..., 0]

        # print(np.where(out==True)[0][-1])
        
        # TODO: padding at the end, need to double check here
        try:
            out = np.where(out==True)[0][-1] # [0] array [-1] the last non padding index 
        except:
            out = t.shape[0]-1

        # print(out)
        p = p[:out+1, :]
        t = t[:out+1, :]
        
        # reshape to (old_length, out_dim) was (:, seqlen * out_dim)
        p = p.reshape(-1, cfg['dim_out'])
        t = t.reshape(-1, cfg['dim_out'])

        # print(p.shape, t.shape)
        

        pct10, pct50, pct90 = cal_angles(p, t)
        p10.append(pct10)
        p50.append(pct50)
        p90.append(pct90)

    del pred_cpu
    del target_cpu

    p10 = np.array(p10)
    p50 = np.array(p50)
    p90 = np.array(p90)

    # a = np.median(p10, axis=0)
    # b = np.median(p50, axis=0)
    # c = np.median(p90, axis=0)
    # return a, b, c

    return p10,p50,p90




def cal_diff(p, t):
    # diff = []

    # for i in range(p.shape[-1]):
        
    #     # diff = np.sort(np.absolute(p - t))
    #     diff[i] = np.absolute(p[:,i] - t[:,i])
    #     # print(diff[i])

    # return np.array(diff)

    # print(p.shape, t.shape)

    diff = np.absolute(p - t)
    return diff



def cal_stats2(pred, target, cfg):

    pred_cpu = pred.cpu().detach().numpy()
    target_cpu = target.cpu().detach().numpy()

    # print(pred_cpu.shape, target_cpu.shape)

    diff_array = []


    for i in range(pred_cpu.shape[0]):
        p = pred_cpu[i]
        t = target_cpu[i]


        pad_dim = t.shape[-1]
        pad = np.zeros(pad_dim)
        out = (t != pad)[..., 0]

        # print(np.where(out==True)[0][-1])
        
        # TODO: padding at the end, need to double check here
        try:
            out = np.where(out==True)[0][-1] # [0] array [-1] the last non padding index 
        except:
            out = t.shape[0]-1

        # print(out)
        p = p[:out+1, :]
        t = t[:out+1, :]
        
        # reshape to (old_length, out_dim) was (:, seqlen * out_dim)
        p = p.reshape(-1, cfg['dim_out'])
        t = t.reshape(-1, cfg['dim_out'])

        # print(p.shape, t.shape)
        

        diff = cal_diff(p, t)

        # print(diff.shape)

        diff_array.append(diff)


    diff_array = np.concatenate(diff_array, axis=0)
    # print(diff_array.shape)

    return diff_array, None, None



def cal_cdf(pred, target, cfg=None):

    p10, p50, p90 = [], [], []

    pred_cpu = pred.cpu().detach().numpy()
    target_cpu = target.cpu().detach().numpy()


    p_all = []
    t_all = []


    for i in range(pred_cpu.shape[0]):
        p = pred_cpu[i]
        t = target_cpu[i]

        # print(p.shape, t.shape)

        pad_dim = t.shape[1]
        pad = np.zeros(pad_dim)
        out = (t != pad)[..., 0]

        try:
            out = np.where(out==True)[0][-1] # [0] array [-1] the last non padding index 
        except:
            out = t.shape[0]-1

        # # reshape to (old_length, out_dim) was (:, seqlen * out_dim)
        # p = p.reshape(-1, cfg['dim_out'])
        # t = t.reshape(-1, cfg['dim_out'])

        p_all.append(p[:out+1, :])
        t_all.append(t[:out+1, :])


    del pred_cpu
    del target_cpu

    p_all = np.concatenate(p_all)
    t_all = np.concatenate(t_all)

    return np.absolute(p_all - t_all)






if __name__ == '__main__':
    cfg = load_cfg()
    
    print(cfg)
    
    
    
    