# -*- coding: utf-8 -*-
"""
Transfer Learning Project

author: Hao Zhou

"""

import torch
from torch.utils.mobile_optimizer import optimize_for_mobile
from signTrans.Models import Transformer

device = torch.device('cpu')

inputsize = 30 * 256
outputsize = 7 * 256
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

out = model(x, y)

model.eval()


print(out.shape)

scripted_module = torch.jit.script(model)
optimized_scripted_module = optimize_for_mobile(scripted_module)

# Export full jit version model (not compatible with lite interpreter)
# scripted_module.save("deeplabv3_scripted.pt")
# print("pt: Success")
# # Export lite interpreter version model (compatible with lite interpreter)
# scripted_module._save_for_lite_interpreter("transformer.ptl")
# print("deeplabv3_scripted.ptl: Success")
# using optimized lite interpreter model makes inference about 60% faster than the non-optimized lite interpreter model, which is about 6% faster than the non-optimized full jit model

#
optimized_scripted_module._save_for_lite_interpreter("transformer.ptl")
print("deeplabv3_scripted_optimized.ptl: Success")

























