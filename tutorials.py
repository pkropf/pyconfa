#!/usr/bin/env python
# -*- coding: utf-8 -*-

fa = [' '.join(r.strip().split()).lower() for r in open('fa_names.txt.private', 'r').readlines()]
sp = [' '.join(r.strip().split()).lower() for r in open('tutorial_names.txt.private', 'r').readlines()]

for name in sp:
    if name in fa:
        print name
