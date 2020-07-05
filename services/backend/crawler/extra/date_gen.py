#!/usr/bin/env python3
# -*- coding: utf-8 -*-

while (True):
    x = input()
    a, b = x.split(",")[2].split("-")
    for i in range(int(a), int(b)+1):
        print(f"{x.split(',')[0]},{x.split(',')[1]},{i}")