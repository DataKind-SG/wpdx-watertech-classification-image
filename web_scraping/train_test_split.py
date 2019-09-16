#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:44:40 2019

@author: k
"""

import shutil
import os
import random

# directory of files
input_dir = 'data'
test_dir = 'test'
train_dir = 'train'

os.makedirs(test_dir, exist_ok=True)
os.makedirs(train_dir, exist_ok=True)

# delete images if it already exists
shutil.rmtree(test_dir)
shutil.rmtree(train_dir)

classes = os.listdir(input_dir)

test_ratio = 0.2

for x in classes:
    
    img_dir = input_dir + '/' + x
    
    os.makedirs(os.path.join(test_dir, x), exist_ok=True)
    
    num_imgs = len(os.listdir(img_dir))
    num_test_imgs = round(num_imgs * test_ratio)
    
    i = 0
    
    while i < num_test_imgs:
        
        file = random.choice(os.listdir(img_dir))
        shutil.move(os.path.join(img_dir, file),
                    os.path.join(test_dir, x, file))
        i += 1
    
    shutil.move(img_dir,
                os.path.join(train_dir))