import math
import random
import numpy as np

# This is modified
epsilon = 1E-10

def normalize2(img): ## add
    norm_img = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        norm_img[:,:,i] = (img[:,:,i] - min)/(max-min)
    return norm_img

def std_norm(img): ## add
    std_norm = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        mean = np.mean(img[:,:,i])
        std = np.std(img[:,:,i])
        std_norm[:,:,i] = (img[:,:,i] - mean)/std
    return std_norm

def norm_img(img): ## max:1, min:-1 per image
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        x = 2.0 * (img[:,:,i] - min) / (max - min) - 1.0
    return x

def norm_0_1(img): ## max:1, min:0
    norm_img = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        norm_img[:,:,i] = (img[:,:,i] - min)/(max-min)
    return norm_img


def norm_band(img): ## max:1, min:-1 per band
    norm_img = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        norm_img[:,:,i] = 2.0 * (img[:,:,i] - min + epsilon) / (max - min + epsilon) - 1.0
    return norm_img

def norm_005(img): ## max:1, min:-1 per band + outlier removal
    norm_img = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        norm_img[:,:,i] = (img[:,:,i] - np.percentile(img[:,:,i],5))/ (np.percentile(img[:,:,i],95) - np.percentile(img[:,:,i],5))
    return norm_img

def norm_min_max(img, new_min=0, new_max=255):
    norm_img = np.zeros(np.shape(img))
    for i in range(np.shape(img)[2]):
        min = np.min(img[:,:,i])
        max = np.max(img[:,:,i])
        norm_img[:,:,i] = (img[:,:,i] - min + epsilon) / (max - min + epsilon) * (new_max - new_min + epsilon) + new_min
    return norm_img