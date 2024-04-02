########################################
# Basic usufull functions for th API. ##
########################################

import torch


# Error map using mean
def emap_mean(x, y):
    return torch.mean(torch.square(x - y), (0))

# Error map using sum
def emap_sum(x, y):
    return torch.mean(torch.square(x - y), (0))



