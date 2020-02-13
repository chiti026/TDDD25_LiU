#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:29:31 2020

@author: tingting
"""
#%%
import os

with open('lab0/db/fortune.db', 'r') as f:
    contents = f.read()

f.close()

lines = contents.strip().split('\n%\n')