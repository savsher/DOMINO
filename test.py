#!/usr/bin/env python3
# -*- coding: utf-8 -*-

x = list()
for i in range(7):
    for j in range(7):
        if j >= i:
            x.append((i,j))
x = [(i,j) for i in range(7) for j in range(7) if j >=i]
print(x)
print(type(x))
print(len(x))