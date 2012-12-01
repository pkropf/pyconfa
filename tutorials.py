#!/usr/bin/env python
# -*- coding: utf-8 -*-

fa = [r.strip() for r in open('fa_names.txt.private', 'r').readlines()]
sp = [r.strip() for r in open('tutorial_names.txt.private', 'r').readlines()]

for name in sp:
    if name in fa:
        print name
